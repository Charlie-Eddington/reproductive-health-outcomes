# Data Quality Notes
## Synthea Synthetic Population — Reproductive Health Dataset

This document describes known data quality issues identified during analysis of the 
Synthea-generated reproductive health dataset. These observations are specific to 
this export and should be considered when interpreting any findings.

This dataset was generated using Synthea with seed `42` and is fully reproducible. 
However, the issues described below are characteristic of Synthea's synthetic 
generation model and are likely to appear in any comparable export.

---

## Summary

| Issue | Observed Rate | Real-World Benchmark | Source |
|-------|-------------|---------------------|--------|
| Pre-eclampsia | ~13% of pregnant | 5–7% | CDC, 2022 |
| Eclampsia | ~13% of pregnant | 0.016–0.1% | Fishel Bartal & Sibai, AJOG 2022 |
| Miscarriage (18-24) | 13.5% of pregnant | ~10% | ACOG, 2023 |
| Miscarriage (40-45) | 62.4% of pregnant | ~33–53% | Magnus et al., BMJ 2019 |
| Overall pregnancy rate | 78% of cohort | ~70% | CDC NSFG |
| IPV | 51% of cohort | 25–35% lifetime | CDC NISVS |

---

## Condition-Level Issues

### Eclampsia & Pre-Eclampsia
The most significant data quality issue in this dataset. Pre-eclampsia and eclampsia 
appear at nearly equal rates (~13% of pregnant patients each), which is a substantial 
departure from US population data:

- **Pre-eclampsia:** 5–7% of pregnancies (CDC, 2022)
- **Eclampsia:** 0.016–0.1% of deliveries in developed countries (Fishel Bartal & Sibai, AJOG 2022)

In a representative US dataset, pre-eclampsia should appear at roughly 100–400 times 
the rate of eclampsia. The near-equal rates in this export indicate a systematic 
over-generation of eclampsia diagnoses.

This is a known issue in the Synthea pregnancy module and is currently under review.

### Miscarriage
Miscarriage rates are elevated across all age groups compared to clinical benchmarks. 
The age-related trend is directionally correct — risk increases with age — but the 
absolute rates are higher than real-world estimates at every age band.

| Age Group | Observed | Benchmark | Source |
|-----------|----------|-----------|--------|
| 18–24 | 13.5% | ~10% | ACOG (2023) |
| 25–29 | 21.6% | ~11% | Magnus et al. (2019) |
| 30–34 | 33.6% | ~15% | Magnus et al. (2019) |
| 35–39 | 48.8% | ~25% | Magnus et al. (2019) |
| 40–45 | 62.4% | ~33–53% | ACOG (2023); Magnus et al. (2019) |

### Anemia
General anemia (`271737000`) is applied broadly across the Synthea population rather 
than exclusively in obstetric contexts. This inflates the obstetric complication rate 
(55% of pregnant patients) beyond what would be expected clinically. A more precise 
analysis would use obstetric-specific anemia codes only.

### Intimate Partner Violence (IPV)
51% of patients have an IPV-related code recorded, substantially higher than the 
real-world lifetime prevalence of 25–35% (CDC, National Intimate Partner and Sexual 
Violence Survey). The broad application of environmental violence codes in Synthea 
contributes to this inflation.

---

## Population-Level Issues

### Pregnancy Rate
78% of female patients aged 18–45 have at least one pregnancy recorded. This is 
higher than population-level estimates and reflects Synthea's tendency to generate 
pregnancies at a higher rate than observed in real-world data, without fully modeling 
variation in fertility intentions, contraceptive use, or infertility.

### Infertility
Only 1 case of female infertility was identified in the entire cohort. Synthea does 
not robustly model infertility as a standalone reproductive health condition.

### Induced Abortion
No induced abortion SNOMED codes were present in this export. Synthea does not 
currently model induced abortion as a clinical pathway.

---

## SDOH Limitations

Social determinant codes are applied relatively uniformly across the Synthea 
population and do not meaningfully correlate with health outcomes the way they 
do in real-world EHR and claims data.

In this dataset, SDOH factors show minimal differentiation between patients with 
and without obstetric complications. Real-world data consistently shows stronger 
associations between social determinants and obstetric outcomes, particularly for 
low-income and minority populations.

This limits the utility of SDOH analysis in synthetic data and should be considered 
when drawing conclusions from SDOH-outcome comparisons.

---

## Encounter-Level Issues

### Obstetric Emergency Encounters
Synthea routes a large proportion of deliveries through obstetric emergency encounter 
types (`183460006`) rather than dedicated delivery encounter codes. This makes it 
difficult to distinguish routine deliveries from true obstetric emergencies based on 
encounter class alone, and inflates apparent emergency rates in the population.

### Prenatal Visit Attendance
100% of pregnant patients in this dataset attended an initial prenatal visit. 
Real-world prenatal care initiation rates vary significantly by demographics, 
insurance status, and geography, and are not uniformly at 100%.

---

## Recommendations

- **Do not use eclampsia or pre-eclampsia rates from this dataset** for any 
  comparative or benchmarking analysis until the generation issue is resolved
- **Treat miscarriage rates as directionally correct** but quantitatively elevated
- **Use SDOH findings as illustrative only** — do not draw causal conclusions
- **Scope anemia analysis** to obstetric-specific codes where possible
- **Re-run analysis** after Synthea pregnancy module updates to validate corrected rates

---

## Sources

- CDC (2022). Preeclampsia, Genomics and Public Health. https://blogs.cdc.gov/genomics/2022/10/25/preeclampsia/
- WHO (2025). Pre-eclampsia Fact Sheet. https://www.who.int/news-room/fact-sheets/detail/pre-eclampsia
- Fishel Bartal M, Sibai BM. Eclampsia in the 21st century. *Am J Obstet Gynecol*. 2022. https://www.ajog.org/article/S0002-9378(20)31128-5/fulltext
- ACOG. Early Pregnancy Loss. https://www.acog.org/womens-health/faqs/early-pregnancy-loss
- Magnus MC, et al. Role of maternal age and pregnancy history in risk of miscarriage. *BMJ*. 2019. https://doi.org/10.1136/bmj.l869
- CDC. National Intimate Partner and Sexual Violence Survey (NISVS). https://www.cdc.gov/violenceprevention/nisvs/index.html
- CDC. National Survey of Family Growth (NSFG). https://www.cdc.gov/nchs/nsfg/index.htm