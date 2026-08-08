# 9. Dashboard & Application

## 9.1 Introduction

The Patient Readmission prediction project consists of an analytical dashboard developed using **Streamlit**. The application combines predictive analytics with business intelligence, allowing healthcare professionals to explore several insights related to Patient & Hospital as well. It also possess a Prediction system to predict individual patient readmission through a unified interface.

The dashboard was designed with a focus on simplicity, consistency, and usability, ensuring that clinical and administrative users can interpret information with minimal effort.

---

# 9.2 Application Architecture

The application consists of three primary modules:

### 1. Home Page

Provides an overview of the project including:

- Platform introduction
- Model performance summary
- Technology stack
- Project highlights

---

### 2. Executive Dashboard

Provides interactive analytics covering:

- Key Performance Indicators (KPIs)
- Patient Demographics
- Hospital Operations
- Financial Insights
- Clinical Risk Factors
- Readmission Analytics

The dashboard enables users to understand trends and identify factors associated with hospital readmissions.

---

### 3. Patient Readmission Predictor

Allows users to:

- Enter patient information.
- Predict the probability of 30-day readmission.
- Provides recommendations based on Readmission Probability.
- Support clinical decision-making.

---

# 9.3 Dashboard Design Principles

The dashboard was designed using the following principles:

- Minimal and clean user interface.
- Consistent typography and spacing.
- Responsive layout for different screen sizes.
- Clinically meaningful color palette.
- Uniform styling across all pages.

---

# 9.4 Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Charts | Plotly |
| Styling | Custom CSS |
| Machine Learning | CatBoost |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib |


---

# 9.5 User Workflow

The typical workflow is as follows:

1. Open the application.
2. Review the project overview.
3. Explore hospital analytics through the dashboard.
4. Navigate to the prediction page.
5. Enter patient details.
6. Generate the readmission prediction.
7. Interpret the predicted risk.

---

# 9.6 Screenshots

## Home Page

<p align="center">
<img src="images/Dashboard_9.8.1.png" width="90%">
</p>

<p align="center">
<b>Figure 9.1:</b> Home Page
</p>

---

## Executive Dashboard

<p align="center">
<img src="images/Dashboard_9.8.2.png" width="90%">
</p>

<p align="center">
<b>Figure 9.2:</b> Executive Dashboard
</p>

---

## Patient Readmission Predictor

<p align="center">
<img src="images/Dashboard_9.8.3.png" width="90%">
</p>

<p align="center">
<b>Figure 9.3:</b> Patient Readmission Prediction Interface
</p>

---

# 9.7 Summary

The 
Patient Readmission Prediction Platform integrates machine learning with interactive business intelligence to provide a comprehensive decision support system for hospital administrators and clinicians.

The application demonstrates how predictive analytics can be combined with modern dashboard technologies to support evidence-based healthcare decision-making.