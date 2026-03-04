# Women's Health Outcomes Analytics

An end-to-end clinical analytics portfolio project demonstrating SQL, Python, and data visualization skills using synthetic patient data.

## Project Overview

This project analyzes reproductive health outcomes in a synthetic population of 5,141 women aged 18–45, generated using Synthea™ (MITRE Corporation). The analysis focuses on pregnancy outcomes, obstetric complications, social determinants of health, and patient care journeys — directly relevant to women's health technology and public health contexts.

**Key skills demonstrated:**
- Synthetic EHR data generation and configuration (Synthea)
- Clinical data cleaning and filtering (SNOMED-CT)
- ETL pipeline design (Python, pandas, SQLite)
- SQL querying and cohort modeling
- Clinical outcomes analysis benchmarked against CDC/WHO/ACOG
- Interactive data visualization (Plotly)
- Patient journey analysis (Sankey diagram)
- Data quality documentation

---

## Repository Structure

```
womens-health-analytics/
├── README.md
├── requirements.txt
├── prompt.md                          # Synthea generation prompt reference
├── .gitignore
├── generate/
│   └── synthea_generate.py            # Interactive CLI to generate Synthea population
├── notebooks/
│   └── Clinical_Analysis.ipynb        # Main analysis notebook
├── docs/
│   ├── Reproductive_Health_Analysis_Synthetic_Population_Data.md
│   └── Data_Quality.md                # Data quality findings and limitations
├── Womens_Health_Analysis/
│   ├── synthea.properties             # Synthea configuration
│   ├── summary.txt                    # Generation summary
│   └── metadata/                      # Run metadata JSON
└── db/                                # SQLite database (gitignored)
```

---

## Data

Patient data was generated using **Synthea™**, an open-source synthetic patient generator developed by the MITRE Corporation. Synthea produces realistic but not real patient records using disease modules informed by CDC, NIH, and published clinical literature.

**Population parameters:**
| Parameter | Value |
|-----------|-------|
| Run ID | `559d1802-bd05-45a1-9cbd-2467068909dc` |
| Sample size | 5,141 patients |
| Gender | Female |
| Age range | 18–45 |
| State | Washington |
| Seed | `42` (fully reproducible) |
| Reference date | March 2, 2026 |
| Years of history | 10 |
| Synthea version | `0a934f8` |
| Java version | 17.0.18 |

**No real patient data is used in this project.** All records are fully synthetic and free of privacy restrictions.

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/womens-health-analytics.git
cd womens-health-analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Java 17 (required for Synthea)
Download from https://adoptium.net — select JDK 17, macOS, x64.

### 4. Generate the dataset
```bash
python generate/synthea_generate.py
```
Follow the prompts. Use these settings to reproduce the exact population used in this analysis:
- Sample size: 5000
- Gender: Female
- Age: 18–45
- State: Washington
- Seed: 42

### 5. Run the analysis notebook
```bash
jupyter notebook notebooks/Clinical_Analysis.ipynb
```

---

## Analysis Overview

### Notebook: `Clinical_Analysis.ipynb`

**Section 1 — Data Loading**
- Dynamically load all Synthea CSVs into SQLite
- Raw table creation with `raw_` prefix convention

**Section 2 — Patient Cohort Filter**
- Filter to female patients aged 18–45
- Derive age groups aligned to CDC 5-year reporting bands

**Section 3 — Condition Filtering**
- Filter to reproductive health SNOMED-CT codes
- Separate SDOH codes into equity variable layer
- Derive binary outcome flags per patient

**Section 4 — SQL Analysis**
- Pregnancy outcomes by age group
- Miscarriage rate benchmarked against CDC/ACOG
- Obstetric complication distribution
- SDOH factors in complicated vs normal pregnancies

**Section 5 — Visualizations**
- Pregnancy outcomes by age group (grouped bar)
- Condition distribution (horizontal bar)
- Miscarriage rate vs CDC/ACOG benchmarks (line chart)
- Eclampsia & pre-eclampsia vs CDC/WHO benchmarks (grouped bar)

**Section 6 — Pregnancy Care Journey**
- Patient journey reconstruction from encounter sequences
- Sankey diagram tracing prenatal care through delivery and loss outcomes

---

## Key Findings

- Complication rates rise steadily with age, from 32% in the 18–24 group to 69% in the 40–45 group — consistent with advanced maternal age literature
- Miscarriage rates are directionally correct (rising with age) but elevated across all age groups compared to CDC/ACOG benchmarks
- Eclampsia and pre-eclampsia appear at nearly equal rates (~13% each) — a known data quality issue in this Synthea export; real-world rates show eclampsia at 0.016–0.1% vs pre-eclampsia at 5–7%
- SDOH factors show minimal differentiation between complicated and normal pregnancies, reflecting Synthea's uniform SDOH code application
- 35% of pregnant patients experienced pregnancy loss; 58% delivered; 7% had no recorded outcome in the encounter data

---

## Data Quality

See [`docs/Data_Quality.md`](docs/Data_Quality.md) for full documentation of known limitations including:
- Eclampsia over-representation vs CDC/WHO benchmarks
- Miscarriage rate inflation across all age groups
- IPV code over-application
- SDOH uniformity across outcome groups
- Obstetric emergency encounter routing for routine deliveries

---

## Planned Enhancements

- [ ] Re-run analysis after Synthea pregnancy module updates to validate corrected rates
- [ ] Add dbt models for modular SQL transformations
- [ ] Population benchmark comparison — all condition rates vs CDC/WHO population statistics
- [ ] Replace Jupyter charts with Evidence.dev interactive dashboard

---

## References

1. Walonoski J, et al. Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record. *JAMIA*. 2018. doi:10.1093/jamia/ocx079
2. CDC (2022). Preeclampsia, Genomics and Public Health. https://blogs.cdc.gov/genomics/2022/10/25/preeclampsia/
3. WHO (2025). Pre-eclampsia Fact Sheet. https://www.who.int/news-room/fact-sheets/detail/pre-eclampsia
4. Fishel Bartal M, Sibai BM. Eclampsia in the 21st century. *Am J Obstet Gynecol*. 2022. https://www.ajog.org/article/S0002-9378(20)31128-5/fulltext
5. ACOG. Early Pregnancy Loss. https://www.acog.org/womens-health/faqs/early-pregnancy-loss
6. Magnus MC, et al. Role of maternal age and pregnancy history in risk of miscarriage. *BMJ*. 2019. https://doi.org/10.1136/bmj.l869
7. CDC. National Intimate Partner and Sexual Violence Survey (NISVS). https://www.cdc.gov/violenceprevention/nisvs/index.html

---

## License

This project is for portfolio and educational purposes. Synthea is licensed under Apache 2.0.