import streamlit as st
import pandas as pd
import numpy as np

from utils import (
    load_model,
    load_threshold,
    load_feature_order,
    predict
)


from feature_engineering import create_engineered_features

from recommendations import generate_recommendations

from styles import load_css

def format_indian(number):

    number = int(round(number))

    s = str(number)

    if len(s) <= 3:
        return s

    last3 = s[-3:]
    remaining = s[:-3]

    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return ",".join(parts + [last3])


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Predict Patient",
    page_icon="🏥",
    layout="wide"
)

load_css()

# ==========================================
# Page Header
# ==========================================

st.markdown("""
<div class="dashboard-title">Predict Hospital Readmission</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-subtitle">
Enter the patient details below to estimate the probability of 30-day hospital readmission.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

# ==========================================
# Prediction Mode
# ==========================================

tab1, tab2 = st.tabs(
    ["Single Patient", "Batch Prediction"]
)

# ===========================================================
# TAB 1
# ===========================================================

with tab1:

    st.markdown('<div class="form-section">Patient Demographics</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        patient_id = st.text_input(
            "Patient ID",
            value="P001"
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=50
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        los_days = st.number_input(
            "Length of Stay (Days)",
            min_value=0,
            value=5
        )

        num_procedures = st.number_input(
            "Number of Procedures",
            min_value=0,
            value=1
        )

        prev_admissions = st.number_input(
            "Previous Admissions",
            min_value=0,
            value=0
        )

    with col2:

        charlson_index = st.number_input(
            "Charlson Index",
            min_value=0,
            value=1
        )

        comorbidity_count = st.number_input(
            "Comorbidity Count",
            min_value=0,
            value=1
        )

        bpl_card = st.selectbox(
            "Below Poverty Line (BPL) Card",
            ["No", "Yes"]
        )

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section">Clinical Indicators</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        hba1c = st.number_input(
            "HbA1c",
            min_value=0.0,
            value=6.5
        )

        creatinine = st.number_input(
            "Creatinine",
            min_value=0.0,
            value=1.0
        )

    with col2:

        haemoglobin = st.number_input(
            "Haemoglobin",
            min_value=0.0,
            value=13.0
        )

        systolic_bp = st.number_input(
            "Systolic Blood Pressure",
            min_value=0,
            value=120
        )

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section">Financial Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        total_cost = st.number_input(
            "Total Cost (INR)",
            min_value=0.0,
            value=10000.0
        )

        govt_subsidy = st.number_input(
            "Government Subsidy (INR)",
            min_value=0.0,
            value=5000.0
        )

    with col2:

        # Automatically calculate Out-of-Pocket Cost

        oop = max(0.0, total_cost - govt_subsidy)

        st.number_input(
            "Out-of-Pocket Cost (INR)",
            value=float(oop),
            disabled=True
        )

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section">Hospital Information</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:

        beds = st.number_input(
            "Hospital Beds",
            min_value=0,
            value=300
        )

        admit_type = st.selectbox(
            "Admission Type",
            [
                "Emergency",
                "Elective",
                "OPD"
            ]
        )

    with c2:

        teaching = st.selectbox(
            "Teaching Hospital",
            ["No", "Yes"]
        )

        ward = st.selectbox(
            "Ward Type",
            [
                "General",
                "ICU",
                "HDU",
                "NICU"
            ]
        )

    with c3:

        insurance = st.selectbox(
            "Insurance",
            [
                "Ayushman",
                "ESI",
                "Private",
                "No Insurance"
            ]
        )

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    predict_btn = st.button(
        "Predict Readmission",
        use_container_width=True
    )

# ===========================================================
# TAB 2
# ===========================================================

with tab2:

    st.markdown(
        """
<div style="
padding:40px;
border-radius:18px;
background:#FFFFFF;
border:1px solid #E5E7EB;
text-align:center;
margin-top:20px;
">

<h2 style="color:#0F172A;">
🚧 Batch Prediction
</h2>

<p style="
font-size:18px;
color:#64748B;
margin-top:10px;
">

This feature is currently under development.

</p>

<p style="
color:#94A3B8;
font-size:15px;
max-width:650px;
margin:auto;
line-height:1.8;
">

Batch Prediction will allow healthcare professionals to upload a CSV file
containing multiple patient records and generate readmission predictions
for all patients in a single click.

This feature will be available in a future release.

</p>

</div>
""",
        unsafe_allow_html=True
    )
# ==========================================================
# LOAD MODEL
# ==========================================================

model = load_model()

threshold = load_threshold()

feature_order = load_feature_order()


# ==========================================================
# SINGLE PATIENT PREDICTION
# ==========================================================

if predict_btn:

    # ----------------------------------------
    # Create dataframe with all model features
    # ----------------------------------------

    patient = pd.DataFrame(
        np.zeros((1, len(feature_order))),
        columns=feature_order
    )

    # ----------------------------------------
    # Numerical Features
    # ----------------------------------------

    patient.loc[0, "age"] = age
    patient.loc[0, "los_days"] = los_days
    patient.loc[0, "num_procedures"] = num_procedures
    patient.loc[0, "prev_admissions"] = prev_admissions
    patient.loc[0, "charlson_index"] = charlson_index
    patient.loc[0, "comorbidity_count"] = comorbidity_count

    patient.loc[0, "hba1c"] = hba1c
    patient.loc[0, "creatinine"] = creatinine
    patient.loc[0, "haemoglobin"] = haemoglobin
    patient.loc[0, "systolic_bp"] = systolic_bp

    patient.loc[0, "total_cost_inr"] = total_cost
    patient.loc[0, "govt_subsidy_inr"] = govt_subsidy
    patient.loc[0, "out_of_pocket_inr"] = oop

    patient.loc[0, "beds"] = beds

    # ----------------------------------------
    # Binary Features
    # ----------------------------------------

    patient.loc[0, "teaching"] = 1 if teaching == "Yes" else 0

    patient.loc[0, "bpl_card"] = 1 if bpl_card == "Yes" else 0

    # ----------------------------------------
    # Gender
    # ----------------------------------------

    if gender == "Male":
        patient.loc[0, "gender_M"] = 1

    elif gender == "Female":
        patient.loc[0, "gender_F"] = 1

    else:
        patient.loc[0, "gender_Other"] = 1

    # ----------------------------------------
    # Admission Type
    # ----------------------------------------

    patient.loc[
        0,
        f"admit_type_{admit_type}"
    ] = 1

    # ----------------------------------------
    # Ward
    # ----------------------------------------

    patient.loc[
        0,
        f"ward_type_{ward}"
    ] = 1

    # ----------------------------------------
    # Insurance
    # ----------------------------------------

    patient.loc[
        0,
        f"insurance_type_{insurance}"
    ] = 1

    # ----------------------------------------
    # Derived Features
    # ----------------------------------------

    patient = create_engineered_features(patient)

    # ----------------------------------------
    # Ensure feature order
    # ----------------------------------------

    patient = patient[feature_order]

    # ----------------------------------------
    # Predict
    # ----------------------------------------

    prediction, probability = predict(
        model,
        patient,
        threshold
    )

    probability = probability[0]
    prediction = prediction[0]

    # ----------------------------------------
    # Prepare data for recommendations
    # ----------------------------------------

    patient_info = {

        "Probability": probability,

        "age": age,

        "los_days": los_days,

        "prev_admissions": prev_admissions,

        "charlson_index": charlson_index,

        "hba1c": hba1c,

        "creatinine": creatinine,

        "haemoglobin": haemoglobin

    }

    recommendations = generate_recommendations(patient_info)

    # ==========================================================
    # DISPLAY RESULTS
    # ==========================================================

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Risk Level based on MODEL THRESHOLD
    # ----------------------------------------------------------

    if probability < threshold:
        risk_class = "low"
        risk_label = "Low Risk"
    elif probability < 0.40:
        risk_class = "moderate"
        risk_label = "Moderate Risk"
    else:
        risk_class = "high"
        risk_label = "High Risk"

    prediction_text = (
        "Likely to be Readmitted"
        if prediction == 1
        else
        "Unlikely to be Readmitted"
    )

    # ----------------------------------------------------------
    # Result Panel
    # ----------------------------------------------------------

    st.markdown(f'''
    <div class="result-panel risk-{risk_class}">
        <div style="display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; gap: 24px; padding: 8px 0;">
            <div class="prob-display">
                <div class="prob-value risk-{risk_class}">{probability*100:.1f}%</div>
                <div class="prob-label">Readmission Probability</div>
            </div>
            <div style="text-align: center;">
                <div class="risk-badge {risk_class}">{risk_label}</div>
                <div style="margin-top: 14px; color: #64748B; font-size: 13px; font-weight: 500;">
                    Decision Threshold: {threshold*100:.1f}%
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 20px; font-weight: 700; color: #0F172A;">{prediction_text}</div>
                <div style="color: #64748B; font-size: 13px; margin-top: 6px; font-weight: 500;">Model Prediction</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Interpretation
    # ----------------------------------------------------------

    if prediction == 1:

        st.markdown(f'''
        <div class="outcome-card risk-{risk_class}">
            <p>The estimated probability of 30-day readmission is
            <strong>{probability*100:.2f}%</strong>, which is above the
            decision threshold of <strong>{threshold*100:.2f}%</strong>.
            The model predicts this patient as <strong>likely to be readmitted</strong>.</p>
        </div>
        ''', unsafe_allow_html=True)

    else:

        st.markdown(f'''
        <div class="outcome-card risk-{risk_class}">
            <p>The estimated probability of 30-day readmission is
            <strong>{probability*100:.2f}%</strong>, which is below the
            decision threshold of <strong>{threshold*100:.2f}%</strong>.
            The model predicts this patient as <strong>unlikely to be readmitted</strong>.</p>
        </div>
        ''', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Recommendations
    # ----------------------------------------------------------

    st.markdown(
        '<div class="section-title" style="margin-top: 28px;">Recommended Actions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">Based on the patient\'s clinical profile and predicted risk level.</div>',
        unsafe_allow_html=True
    )

    for severity, text in recommendations:

        st.markdown(f'''
        <div class="rec-item severity-{severity}">
            <div class="rec-dot {severity}"></div>
            <div class="rec-text">{text}</div>
        </div>
        ''', unsafe_allow_html=True)
