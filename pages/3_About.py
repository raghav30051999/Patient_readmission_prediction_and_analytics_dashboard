import streamlit as st
from styles import load_css

st.set_page_config(
    page_title="About the Project",
    page_icon="ℹ️",
    layout="wide"
)

load_css()

st.markdown("""
<div class="dashboard-title">About the Project</div>
<div class="dashboard-subtitle">Project Introduction and Developer Details</div>
<div class="styled-divider"></div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: justify; line-height: 1.6;">

### Project Intro
This Hospital Readmission Intelligence Platform is designed to predict the likelihood of 30-day hospital readmissions for patients. By leveraging machine learning (CatBoost), it assists healthcare providers in identifying high-risk patients and taking proactive measures to improve patient outcomes and reduce hospital costs.

### Dataset Details
**Attribution:** Kaggle India Diabetes dataset 2015-2024.  
The model is trained on this comprehensive dataset, which includes demographic, clinical, and financial features to accurately assess readmission risks.

### Developer Details
* **Developer Name:** P.Sri Raghavendra
* **Phone Number:** 9912525797
* **Email ID:** raghavnaveen111@gmail.com

### Project Documentation
* **GitHub Repository:** [https://github.com/raghav30051999/Patient_readmission_prediction_and_analytics_dashboard/tree/main/Technical%20Documentation](#)

</div>
""", unsafe_allow_html=True)
