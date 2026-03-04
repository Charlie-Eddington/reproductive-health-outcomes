"""
synthea_generate.py
-------------------
Interactive CLI to configure and run Synthea population generation.
Requires: Java 11+ installed, synthea-with-dependencies.jar in ./lib/

Usage:
    python synthea_generate.py
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

JAR_PATH = Path("./lib/synthea-with-dependencies.jar")

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

KEY_TABLES = ["patients", "conditions", "medications", "encounters"]

# ─────────────────────────────────────────────
# HELPERS — UI
# ─────────────────────────────────────────────

def print_header():
    print("\n" + "="*55)
    print("        Synthea Population Generator")
    print("="*55 + "\n")

def ask(prompt, valid=None, default=None):
    """Prompt user for input with optional validation."""
    while True:
        suffix = f" [{default}]" if default else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        if not raw:
            print("  ✗ This field is required.\n")
            continue
        if valid and raw not in valid:
            print(f"  ✗ Please enter one of: {', '.join(valid)}\n")
            continue
        return raw

def ask_int(prompt, min_val, max_val, default=None):
    """Prompt user for an integer within a range."""
    while True:
        suffix = f" [{default}]" if default else ""
        raw = input(f"{prompt} ({min_val}–{max_val}){suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  ✗ Must be between {min_val} and {max_val}.\n")
        except ValueError:
            print("  ✗ Please enter a whole number.\n")

def ask_output_dir():
    """Ask user for output folder — accepts name or full path."""
    print("\n  Where should the dataset be saved?")
    print("  You can enter a folder name (e.g. 'my_population')")
    print("  or a full path (e.g. '/Users/me/projects/my_population')\n")
    while True:
        raw = input("  Output folder: ").strip()
        if not raw:
            print("  ✗ Required.\n")
            continue
        path = Path(raw).expanduser().resolve()
        if path.exists():
            overwrite = ask(
                f"  '{path}' already exists. Overwrite?",
                valid=["yes", "no"], default="no"
            )
            if overwrite == "no":
                continue
        return path

def ask_state():
    """Let user pick a US state with partial match support."""
    print("\n  Type a state name (partial match supported):")
    while True:
        raw = input("  State: ").strip().title()
        if not raw:
            print("  ✗ Required.\n")
            continue
        matches = [s for s in US_STATES if raw.lower() in s.lower()]
        if len(matches) == 1:
            print(f"  ✓ Selected: {matches[0]}")
            return matches[0]
        elif len(matches) > 1:
            print(f"  Multiple matches: {', '.join(matches)}")
            print("  Please be more specific.\n")
        else:
            print(f"  ✗ No state matching '{raw}'. Try again.\n")

# ─────────────────────────────────────────────
# HELPERS — SETUP
# ─────────────────────────────────────────────

def verify_java():
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        version_line = (result.stderr or result.stdout).splitlines()[0]
        print(f"  ✓ Java: {version_line}")
    except FileNotFoundError:
        print("  ✗ Java not found. Please install JDK 17.")
        sys.exit(1)

def verify_jar():
    if not JAR_PATH.exists():
        print(f"\n  ✗ Synthea JAR not found at {JAR_PATH}")
        print("  Download it with:\n")
        print("  mkdir -p lib && curl -L -o lib/synthea-with-dependencies.jar \\")
        print("  https://github.com/synthetichealth/synthea/releases/download/"
              "master-branch-latest/synthea-with-dependencies.jar\n")
        sys.exit(1)
    print(f"  ✓ Synthea JAR found")

def write_properties(output_dir):
    props_path = output_dir / "synthea.properties"
    props_path.write_text(
        "exporter.csv.export = true\n"
        "exporter.fhir.export = false\n"
        f"exporter.baseDirectory = {output_dir}/\n"
    )
    return props_path

# ─────────────────────────────────────────────
# HELPERS — COMMAND + SUMMARY
# ─────────────────────────────────────────────

def build_command(config, props_path):
    cmd = [
        "java", "-jar", str(JAR_PATH),
        "-c", str(props_path),
        "-p", str(config["population"]),
        "-s", str(config["seed"]),
        "-a", f"{config['min_age']}-{config['max_age']}",
    ]
    if config["gender"] != "Both":
        cmd += ["-g", config["gender"][0]]
    cmd.append(config["state"])
    return cmd

def print_run_summary(config, cmd):
    print("\n" + "-"*55)
    print("  Run Configuration")
    print("-"*55)
    print(f"  Population : {config['population']:,} patients")
    print(f"  Gender     : {config['gender']}")
    print(f"  Age range  : {config['min_age']}–{config['max_age']}")
    print(f"  State      : {config['state']}")
    print(f"  Seed       : {config['seed']}  (reproducible)")
    print(f"  Output     : {config['output_dir']}")
    print("-"*55)
    print(f"\n  Command:\n  {' '.join(cmd)}\n")

# ─────────────────────────────────────────────
# DESCRIPTIVE STATS
# ─────────────────────────────────────────────

def compute_stats(csv_dir, config):
    """Compute and return descriptive stats for key tables."""
    lines = []
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("="*55)
    lines.append("  Dataset Summary Report")
    lines.append("="*55)
    lines.append(f"  Generated    : {generated_at}")
    lines.append(f"  State        : {config['state']}")
    lines.append(f"  Gender       : {config['gender']}")
    lines.append(f"  Age Range    : {config['min_age']}–{config['max_age']}")
    lines.append(f"  Seed         : {config['seed']}")
    lines.append(f"  Output folder: {config['output_dir']}")
    lines.append("")

    for table in KEY_TABLES:
        fpath = csv_dir / f"{table}.csv"
        if not fpath.exists():
            lines.append(f"  [{table}.csv] — not found, skipping")
            continue

        df = pd.read_csv(fpath, low_memory=False)
        lines.append("-"*55)
        lines.append(f"  {table.upper()}.CSV")
        lines.append("-"*55)
        lines.append(f"  Rows         : {len(df):,}")
        lines.append(f"  Columns      : {len(df.columns)}")
        lines.append(f"  Column names : {', '.join(df.columns.tolist())}")
        lines.append("")

        # Numeric columns — avg, min, max
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if num_cols:
            lines.append("  Numeric columns:")
            for col in num_cols:
                s = df[col].dropna()
                if len(s) == 0:
                    continue
                lines.append(
                    f"    {col:<30} "
                    f"count={len(s):>6,}  "
                    f"avg={s.mean():>10.2f}  "
                    f"min={s.min():>10.2f}  "
                    f"max={s.max():>10.2f}"
                )
            lines.append("")

        # Categorical columns — top value counts
        cat_cols = df.select_dtypes(include="object").columns.tolist()
        # Limit to meaningful categoricals (low cardinality)
        cat_cols = [c for c in cat_cols if df[c].nunique() <= 20]
        if cat_cols:
            lines.append("  Categorical columns (top values):")
            for col in cat_cols[:5]:  # cap at 5 to keep output clean
                top = df[col].value_counts().head(3)
                top_str = ", ".join([f"{v} ({n:,})" for v, n in top.items()])
                lines.append(f"    {col:<30} {top_str}")
            lines.append("")

    lines.append("="*55)
    lines.append("  Generated with Synthea™ (MITRE Corporation)")
    lines.append("  https://github.com/synthetichealth/synthea")
    lines.append("="*55)
    return "\n".join(lines)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print_header()

    # Pre-flight checks
    print("Checking environment...")
    verify_java()
    verify_jar()

    # Interactive configuration
    print("\nConfigure your population:\n")

    output_dir = ask_output_dir()

    population = ask_int(
        "  Sample size",
        min_val=100, max_val=50000,
        default=5000
    )

    gender = ask(
        "  Gender",
        valid=["Female", "Male", "Both"],
        default="Female"
    )

    min_age = ask_int(
        "  Minimum age",
        min_val=0, max_val=100,
        default=18
    )

    max_age = ask_int(
        "  Maximum age",
        min_val=min_age, max_val=100,
        default=45
    )

    state = ask_state()

    seed = ask_int(
        "  Random seed (for reproducibility)",
        min_val=1, max_val=999999,
        default=42
    )

    config = {
        "population": population,
        "gender": gender,
        "min_age": min_age,
        "max_age": max_age,
        "state": state,
        "seed": seed,
        "output_dir": output_dir,
    }

    # Setup output folder + properties
    output_dir.mkdir(parents=True, exist_ok=True)
    props_path = write_properties(output_dir)

    # Build + confirm
    cmd = build_command(config, props_path)
    print_run_summary(config, cmd)

    confirm = ask("  Run generation? (yes/no)", valid=["yes", "no"], default="yes")
    if confirm != "yes":
        print("\n  Cancelled.\n")
        sys.exit(0)

    # Run Synthea
    print("\n  Starting Synthea... (this may take 3–10 minutes)\n")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n  ✗ Synthea failed: {e}\n")
        sys.exit(1)

    # Descriptive stats
    csv_dir = output_dir / "csv"
    print("\n  Computing descriptive statistics...")
    summary = compute_stats(csv_dir, config)

    # Print to terminal
    print("\n" + summary)

    # Save to file
    summary_path = output_dir / "summary.txt"
    summary_path.write_text(summary)
    print(f"\n  ✓ Summary saved to: {summary_path}\n")


if __name__ == "__main__":
    main()