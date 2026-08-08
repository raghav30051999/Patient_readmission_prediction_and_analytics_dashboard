import streamlit as st
import joblib

from styles import load_css
from dashboard_utils import kpi_card

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Hospital Readmission Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Load Styles
# -----------------------------
load_css()

# -----------------------------
# Load Model Information
# -----------------------------
model_info = joblib.load("model_info.pkl")

# -----------------------------
# Sidebar Branding
# -----------------------------
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-name">HRIP</div>
    <div class="sidebar-brand-tag">Hospital Readmission<br>Intelligence Platform</div>
    <div class="sidebar-version">v1.0</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Main Title
# -----------------------------
st.markdown("""
<div class="dashboard-title">Hospital Readmission Intelligence Platform</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-subtitle">
Predict the likelihood of <strong>30-day hospital readmission</strong> using an explainable
Machine Learning model developed with CatBoost.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        "Best Model",
        model_info["Algorithm"],
        "Classification Algorithm",
        accent="indigo"
    )

with col2:
    kpi_card(
        "ROC-AUC",
        str(round(model_info["ROC_AUC"], 3)),
        "Area Under ROC Curve",
        accent="teal"
    )

with col3:
    kpi_card(
        "F1 Score",
        str(round(model_info["F1_Score"], 3)),
        "Harmonic Mean of Precision & Recall",
        accent="amber"
    )

with col4:
    kpi_card(
        "Threshold",
        str(model_info["Threshold"]),
        "Optimized Decision Boundary",
        accent="coral"
    )

st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

# -----------------------------
# Dataset Overview
# -----------------------------
st.markdown('<div class="section-title">Dataset Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Key statistics from the training dataset.</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    kpi_card("Total Patients", "96,048", "Records in Dataset", accent="blue")

with c2:
    kpi_card("Readmission Rate", "11.84%", "30-Day Readmission", accent="rose")

with c3:
    kpi_card("Features Used", "93", "After Feature Engineering", accent="violet")

st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

# -----------------------------
# Model Summary
# -----------------------------
st.markdown('<div class="section-title">Model Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Technical specifications of the trained model.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="model-summary-card">
    <div class="summary-item">
        <div class="summary-dot"></div>
        <div class="summary-label">Algorithm</div>
        <div class="summary-value">CatBoost Classifier</div>
    </div>
    <div class="summary-item">
        <div class="summary-dot"></div>
        <div class="summary-label">Target Variable</div>
        <div class="summary-value">Predict 30-Day Hospital Readmission</div>
    </div>
    <div class="summary-item">
        <div class="summary-dot"></div>
        <div class="summary-label">Evaluation Metric</div>
        <div class="summary-value">ROC-AUC & F1 Score</div>
    </div>
    <div class="summary-item">
        <div class="summary-dot"></div>
        <div class="summary-label">Explainability</div>
        <div class="summary-value">SHAP (SHapley Additive exPlanations)</div>
    </div>
    <div class="summary-item">
        <div class="summary-dot"></div>
        <div class="summary-label">Threshold Optimization</div>
        <div class="summary-value">Yes</div>
    </div>
    <div class="summary-item">
        <div class="summary-dot"></div>
        <div class="summary-label">Feature Engineering</div>
        <div class="summary-value">Yes</div>
    </div>
    <div class="summary-item">
        <div class="summary-dot"></div>
        <div class="summary-label">Feature Ablation</div>
        <div class="summary-value">Yes</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-size: 13px; color: #64748B; margin-top: 16px; margin-bottom: 24px; text-align: center;">
    <strong>Attribution:</strong> Kaggle India Diabetes dataset 2015-2024
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav-banner">
    Use the navigation menu on the left to explore predictions, analytics, and model explainability.
</div>
""", unsafe_allow_html=True)