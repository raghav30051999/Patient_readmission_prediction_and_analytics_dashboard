# 🏥 Patient Readmission Prediction using Machine Learning (ML) along with Analytics Dashboard

> An end-to-end Machine Learning and Business Intelligence platform for predicting 30-day hospital readmissions along with recommendations and also provides Analytics Dashboard with Impactful Insights.

---

## 📌 Project Overview

Hospital readmissions are one of the biggest challenges faced by healthcare providers worldwide. Unplanned readmissions increase treatment costs, occupy hospital resources, and often indicate poor continuity of patient care.

The **Patient Readmission Prediction** is a ML prediction along with recommendations, clinical decision support system designed to:

- Predict whether a patient is likely to be readmitted within **30 days**.
- Help clinicians identify **high-risk patients** before discharge.
- Provide interactive dashboards for hospital administrators.
- Improve operational and financial decision-making using analytics.

---

## 🎯 Objectives

- Predict 30-day hospital readmissions using Machine Learning.
- Assist clinicians in identifying high-risk patients.
- Improve hospital resource planning.
- Reduce unnecessary healthcare expenditure.
- Provide an intuitive dashboard for healthcare analytics.

---

## 🚀 Key Features

### 📊 Executive Analytics Dashboard

- Executive KPI Dashboard
- Patient Demographics
- Hospital Operations
- Financial Insights
- Clinical Risk Analysis
- Readmission Analytics

---

### 🩺 Patient Readmission Prediction

- Individual Patient Risk Prediction
- Readmission Probability Score
- Risk Classification
- Recommendations based on Readmission Probability

---

## 🧠 Machine Learning Pipeline

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Feature Selection
- Class Imbalance Handling
- Hyperparameter Tuning
- Threshold Optimization
- Model Evaluation
- Model Explainability

---

## 🤖 Final Model

| Item | Value |
|------|------|
| Algorithm | CatBoost Classifier |
| Target | 30-Day Readmission |
| Threshold | Optimized (0.18) |
| Explainability | SHAP |
| Calibration | Yes |

---

## 📁 Project Structure

```text
Hospital_Readmission_Intelligence_Platform/

│
├── app.py
├── dashboard_utils.py
├── styles.py
├── requirements.txt
├── README.md
├── TECHNICAL_DOCUMENTATION.md
│
├── data/
│
├── models/
│
├── pages/
│   ├── dashboard.py
│   └── patient_prediction.py
│
└── assets/
```

---

## 🛠 Technology Stack

### Programming

- Python

### Machine Learning

- Random Forest
- Balanced Random Forest
- GradientBoost
- CatBoost (Finally preferred this algo for its overall balance in recall and precision)
- SHAP

### Data Analysis

- Pandas
- NumPy

### Visualization

- Plotly
- Streamlit

### Deployment

- Streamlit Community Cloud

---

## 📈 Dashboard Preview

> Link for Patient Readmission Prediction App : .

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/hospital-readmission-intelligence-platform.git
```

Navigate to the project

```bash
cd hospital-readmission-intelligence-platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📚 Documentation

Detailed project documentation is available in:

**TECHNICAL_DOCUMENTATION.md**

---

## 📌 Future Enhancements

- **Batch-wise patient readmission prediction**
- **Continuous learning and adaptation to evolving trends upon dataset updates.**
- Real-time prediction APIs
- Physician recommendation engine
- LLM-based recommendations
  

---

## 👨‍💻 Author

**Sri Raghavendra Puvvula**

Machine Learning | Data Science |

---

## ⭐ If you found this project useful, consider giving it a Star!
