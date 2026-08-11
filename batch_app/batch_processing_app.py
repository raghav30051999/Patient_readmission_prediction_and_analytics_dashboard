import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from styles import load_css
import dashboard_utils as du

from agent_pipeline.schema_validator import load_schema, validate_batch
from agent_pipeline.batch_agent import run_agent_pipeline

BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_PATH = BASE_DIR / "templates" / "batch_template.csv"
REFERENCE_PATH = BASE_DIR / "templates" / "batch_reference.csv"
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="Hospital Batch Processing",
    page_icon="🏥",
    layout="wide"
)

load_css()


def format_metric(value):
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def format_percentage(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


# ==========================================================
# SIDEBAR BRANDING
# ==========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-name">🏥 Hospital Readmission Intelligence Platform</div>
            <div class="sidebar-brand-tag">Batch Processing Module</div>
            <span class="sidebar-version">v2.0</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# HEADER
# ==========================================================

left, right = st.columns([4, 2])

with left:
    st.markdown(
        '<div class="dashboard-title">Patient Data Batch Processing</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="dashboard-subtitle">
        Upload patient admission data in batch format. The pipeline will
        validate, clean, predict, and evaluate the batch automatically.
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        f"""
        <div class="update-card">
            <div class="update-title">Last Updated</div>
            <div class="update-date">{datetime.today().strftime("%d %b %Y")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

du.separator()

# ==========================================================
# SECTION 1: DOWNLOAD TEMPLATES
# ==========================================================

du.section_heading(
    "Download Templates",
    "Download the batch template and reference guide before uploading."
)

col1, col2 = st.columns(2)

with col1:
    if TEMPLATE_PATH.exists():
        with open(TEMPLATE_PATH, "rb") as f:
            st.download_button(
                label="📥 Download Batch Template",
                data=f.read(),
                file_name="batch_template.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.error("batch_template.csv not found.")

with col2:
    if REFERENCE_PATH.exists():
        with open(REFERENCE_PATH, "rb") as f:
            st.download_button(
                label="📥 Download Reference Guide",
                data=f.read(),
                file_name="batch_reference.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.error("batch_reference.csv not found.")

du.separator()

# ==========================================================
# SECTION 2: UPLOAD FILE
# ==========================================================

du.section_heading(
    "Upload Filled Batch File",
    "Upload the completed CSV file for automated processing."
)

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"],
    label_visibility="collapsed",
    key="batch_csv_uploader"
)

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Unable to read file: {e}")
        st.stop()

    st.success(f"File loaded successfully. Rows found: {len(df)}")

    with st.expander("Preview Uploaded Data", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

    du.separator()

    # ======================================================
    # SECTION 3: SCHEMA VALIDATION
    # ======================================================

    du.section_heading(
        "Schema Validation",
        "Automated checks for required columns, data types, ranges, and allowed values."
    )

    schema = load_schema()
    validation_report = validate_batch(df, schema)

    v1, v2, v3 = st.columns(3)

    with v1:
        du.kpi_card("Rows", validation_report["row_count"], "Uploaded Records", accent="indigo")
    with v2:
        du.kpi_card("Errors", validation_report["error_count"], "Schema Violations", accent="rose")
    with v3:
        du.kpi_card("Warnings", validation_report["warning_count"], "Non-blocking Issues", accent="amber")

    if validation_report["status"] == "failed":

        st.error("Validation failed. Please fix the errors below.")

        for error in validation_report["errors"]:
            st.error(error)

        for warning in validation_report["warnings"]:
            st.warning(warning)

        st.stop()

    st.success("Validation passed.")

    for warning in validation_report["warnings"]:
        st.warning(warning)

    save_path = UPLOAD_DIR / uploaded_file.name

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info(f"Uploaded file saved to: {save_path}")

    du.separator()

    # ======================================================
    # SECTION 4: AGENTIC PROCESSING PIPELINE
    # ======================================================

    du.section_heading(
        "Automated Processing Pipeline",
        "The pipeline autonomously executes cleaning, prediction, and evaluation stages."
    )

    with st.spinner("Running pipeline: Cleaning → Prediction → Evaluation"):
        final_df, agent_report = run_agent_pipeline(df)

    a1, a2, a3 = st.columns(3)

    with a1:
        du.kpi_card("Agent Status", agent_report["status"], "Pipeline Outcome", accent="emerald")
    with a2:
        du.kpi_card("Stages Completed", len(agent_report["stages_completed"]), "Autonomous Stages", accent="teal")
    with a3:
        du.kpi_card("Rows Processed", len(final_df), "Total Records", accent="blue")

    if agent_report["status"] == "failed":
        for message in agent_report["messages"]:
            st.error(message)
        st.stop()

    for message in agent_report["messages"]:
        st.info(message)

    # ======================================================
    # RESULT TABS
    # ======================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Cleaning Report",
            "Prediction Report",
            "Evaluation Report",
            "Processed Data"
        ]
    )

    # ------------------------------------------------------
    # TAB 1: CLEANING
    # ------------------------------------------------------

    with tab1:
        cleaning_report = agent_report.get("cleaning_report", {})

        if cleaning_report:
            st.markdown('<div class="form-section">Cleaning Changes</div>', unsafe_allow_html=True)

            if cleaning_report.get("changes"):
                for change in cleaning_report["changes"]:
                    st.info(change)
            else:
                st.write("No cleaning changes were required.")

            st.markdown('<div class="form-section">Cleaning Warnings</div>', unsafe_allow_html=True)

            if cleaning_report.get("warnings"):
                for warning in cleaning_report["warnings"]:
                    st.warning(warning)
            else:
                st.write("No cleaning warnings found.")

    # ------------------------------------------------------
    # TAB 2: PREDICTION
    # ------------------------------------------------------

    with tab2:
        prediction_report = agent_report.get("prediction_report", {})

        if prediction_report:

            p1, p2, p3, p4 = st.columns(4)

            with p1:
                du.kpi_card(
                    "Rows With Actual Outcome",
                    format_metric(prediction_report.get("rows_with_actual_outcome")),
                    "Used for Evaluation",
                    accent="indigo"
                )
            with p2:
                du.kpi_card(
                    "Rows Predicted",
                    format_metric(prediction_report.get("rows_predicted")),
                    "Blank Outcome Rows",
                    accent="teal"
                )
            with p3:
                du.kpi_card(
                    "High Risk Predicted",
                    format_metric(prediction_report.get("high_risk_predicted")),
                    "Above Threshold",
                    accent="rose"
                )
            with p4:
                du.kpi_card(
                    "Threshold",
                    format_metric(prediction_report.get("threshold")),
                    "Decision Cutoff",
                    accent="amber"
                )

            for message in prediction_report.get("messages", []):
                st.info(message)

            predicted_rows = final_df[final_df["prediction_status"] == "predicted"]

            if not predicted_rows.empty:
                st.markdown('<div class="form-section">Predicted Rows</div>', unsafe_allow_html=True)

                display_columns = [
                    "admission_id",
                    "patient_id",
                    "predicted_probability",
                    "predicted_readmission_30d",
                    "prediction_status"
                ]

                available_columns = [
                    col for col in display_columns if col in predicted_rows.columns
                ]

                st.dataframe(predicted_rows[available_columns], use_container_width=True)

    # ------------------------------------------------------
    # TAB 3: EVALUATION
    # ------------------------------------------------------

    with tab3:
        evaluation_report = agent_report.get("evaluation_report", {})

        if evaluation_report:

            if evaluation_report.get("rows_evaluated", 0) == 0:
                st.info("No rows with actual outcomes were available for evaluation.")

            else:

                e1, e2, e3, e4 = st.columns(4)

                with e1:
                    du.kpi_card("Rows Evaluated", format_metric(evaluation_report.get("rows_evaluated")), "With Actual Outcomes", accent="indigo")
                with e2:
                    du.kpi_card("Actual Readmission Rate", format_percentage(evaluation_report.get("actual_readmission_rate")), "Observed Rate", accent="rose")
                with e3:
                    du.kpi_card("Mean Predicted Probability", format_percentage(evaluation_report.get("mean_predicted_probability")), "Model Average", accent="teal")
                with e4:
                    du.kpi_card("Threshold", format_metric(evaluation_report.get("threshold")), "Decision Cutoff", accent="amber")

                st.markdown('<div class="form-section">Model Performance</div>', unsafe_allow_html=True)

                m1, m2, m3, m4 = st.columns(4)

                with m1:
                    du.kpi_card("Accuracy", format_metric(evaluation_report.get("accuracy")), accent="blue")
                with m2:
                    du.kpi_card("Precision", format_metric(evaluation_report.get("precision")), accent="violet")
                with m3:
                    du.kpi_card("Recall", format_metric(evaluation_report.get("recall")), accent="coral")
                with m4:
                    du.kpi_card("Specificity", format_metric(evaluation_report.get("specificity")), accent="emerald")

                m5, m6, m7, m8 = st.columns(4)

                with m5:
                    du.kpi_card("F1 Score", format_metric(evaluation_report.get("f1_score")), accent="indigo")
                with m6:
                    du.kpi_card("AUROC", format_metric(evaluation_report.get("auroc")), accent="teal")
                with m7:
                    du.kpi_card("PR-AUC", format_metric(evaluation_report.get("pr_auc")), accent="amber")
                with m8:
                    du.kpi_card("Brier Score", format_metric(evaluation_report.get("brier_score")), accent="rose")

                st.markdown('<div class="form-section">Confusion Matrix</div>', unsafe_allow_html=True)

                confusion = evaluation_report.get("confusion_matrix", {})

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    du.kpi_card("True Positive", format_metric(confusion.get("true_positive")), accent="emerald")
                with c2:
                    du.kpi_card("False Positive", format_metric(confusion.get("false_positive")), accent="amber")
                with c3:
                    du.kpi_card("True Negative", format_metric(confusion.get("true_negative")), accent="blue")
                with c4:
                    du.kpi_card("False Negative", format_metric(confusion.get("false_negative")), accent="rose")

                for message in evaluation_report.get("messages", []):
                    st.info(message)

    # ------------------------------------------------------
    # TAB 4: PROCESSED DATA
    # ------------------------------------------------------

    with tab4:
        st.markdown('<div class="form-section">Processed Batch Output</div>', unsafe_allow_html=True)

        st.dataframe(final_df.head(100), use_container_width=True)

        csv_data = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Processed Batch",
            data=csv_data,
            file_name="processed_batch.csv",
            mime="text/csv",
            use_container_width=True
        )