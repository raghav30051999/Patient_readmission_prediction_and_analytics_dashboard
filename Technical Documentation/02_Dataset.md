# 2. Dataset Description

## 2.1 Dataset Overview

The Patient Readmission Prediction Platform was developed using a publicly available hospital readmission dataset named "India Hospital Readmission Dataset (2015–2024)" from the Kaggle, containing demographic, clinical, laboratory, administrative, and hospitalization-related information for patients admitted to hospitals.

The dataset is designed for predicting whether a patient will be readmitted within **30 days** after discharge.

This is a **supervised binary classification problem**, where the target variable indicates whether the patient was readmitted within the specified time period.

---

# 2.2 Dataset Source

**Dataset Name**

India Hospital Readmission Dataset (2015–2024)

**Coverage Period**

2015 – 2024

**Domain**

Healthcare Analytics

**Problem Type**

Binary Classification

**Target Variable**

30-Day Hospital Readmission

---

# 2.3 Dataset Characteristics

The dataset contains a diverse set of variables describing different aspects of a patient's hospital encounter.

The major categories include:

- Patient Demographics
- Admission Information
- Clinical Conditions
- Laboratory Measurements
- Hospital Utilization
- Comorbidity Indicators
- Medication Information
- Financial Information
- Readmission Outcome

This diverse combination of features enables the development of robust machine learning models capable of learning complex relationships influencing hospital readmissions.

---

# 2.4 Target Variable

The objective of the project is to predict whether a patient will be readmitted within **30 days** after discharge.

| Value | Description |
|--------|-------------|
| 0 | Not Readmitted |
| 1 | Readmitted within 30 Days |

---

# 2.5 Feature Categories

The dataset contains features belonging to several healthcare domains.

## Demographic Features

Examples include:

- Age
- Gender
- Below Poverty Line (BPL)

---

## Clinical Features

Examples include:

- Admission Type
- Ward Type
- ICU Admission
- Length of Stay

---

## Admission Features

Examples include:

- Primary Diagnosis
- Secondary Diagnoses
- Charlson Comorbidity Index
- Number of Comorbidities
- Diabetes Status
- Hypertension
- Heart Disease

---

## Laboratory Features

Examples include:

- HbA1c
- Creatinine
- Hemoglobin
- Blood Glucose
- Other laboratory measurements

---

## Hospital Utilization

Examples include:

- Previous Admissions
- Emergency Visits
- Outpatient Visits
- Previous Procedures
- Medication Count

---

## Financial Features

Examples include:

- Hospitalization Cost
- Cost Category
- Insurance Status

---

# 2.6 Data Quality Assessment

Before model development, the dataset was carefully examined for potential quality issues.

The following aspects were evaluated:

- Missing values
- Duplicate records
- Inconsistent categorical values
- Invalid numerical values
- Data type inconsistencies
- Outlier distributions

Appropriate preprocessing techniques were applied wherever necessary to ensure reliable model training.

---

# 2.7 Data Challenges

Healthcare datasets are inherently complex and often contain several modelling challenges.

The primary challenges encountered in this project included:

- Mixed numerical and categorical variables
- Class imbalance
- High-cardinality categorical features
- Missing observations
- Clinical variability across patients
- Non-linear relationships between predictors and the target variable

These challenges guided the selection of preprocessing techniques and machine learning algorithms used in the project.

---

# 2.8 Feature Summary

The dataset includes variables describing the patient's demographic profile, admission characteristics, medical history, laboratory investigations, treatment information, hospital utilization, and financial burden.

Some important features used during model development include:

| Feature | Description |
|----------|-------------|
| age | Patient age |
| gender | Patient gender |
| admit_type | Type of hospital admission |
| ward_type | Hospital ward |
| los_days | Length of stay |
| charlson_index | Charlson Comorbidity Index |
| comorbidity_count | Number of comorbid conditions |
| diabetes | Diabetes status |
| hba1c | HbA1c level |
| total_cost_inr | Hospitalization cost |
| cost_category | Hospital cost category |
| readmitted_30d | Target variable |

---

# 2.9 Importance of the Dataset

The India Hospital Readmission Dataset provides a realistic representation of patient admissions across multiple years and enables the study of demographic, operational, clinical, and financial factors associated with hospital readmissions.

Its diverse feature set makes it well suited for developing predictive models as well as interactive business intelligence dashboards for healthcare decision support.

---

# 2.10 Chapter Summary

This chapter introduced the dataset used throughout the project and described its structure, feature categories, target variable, and overall characteristics.

The next chapter presents the Exploratory Data Analysis (EDA), where statistical summaries and visual analyses were performed to better understand patient demographics, admission patterns, clinical variables, and hospitalization trends before building the predictive model.