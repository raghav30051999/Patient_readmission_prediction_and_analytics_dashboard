import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

import dashboard_utils as du

from styles import load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Hospital Readmission Intelligence Platform",
    page_icon="🏥",
    layout="wide"
)

load_css()

# ==========================================================
# LOAD DATA
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "master_dataset_after_EDA_V1.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# ==========================================================
# HEADER
# ==========================================================

left, right = st.columns([4, 2])

with left:

    st.markdown(
        """
<div class='dashboard-title'>
Hospital Readmission Intelligence Platform
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class='dashboard-subtitle'>
Comprehensive analytics for monitoring 30-day hospital readmission trends and patient outcomes.
</div>
""",
        unsafe_allow_html=True
    )

with right:

        st.markdown(
            f"""
    <div class="update-card">

    <div class="update-title">
    Last Updated
    </div>

    <div class="update-date">
    {datetime.today().strftime("%d %b %Y")}
    </div>

    </div>
    """,
            unsafe_allow_html=True
        )

du.separator()

# ==========================================================
# EXECUTIVE KPIs
# ==========================================================

total_patients = len(df)

readmitted_patients = int(df["readmitted_30d"].sum())

readmission_rate = (
    readmitted_patients / total_patients
) * 100

avg_los = df["los_days"].mean()

avg_cost = df["total_cost_inr"].mean()

avg_age = df["age"].mean()

du.section_heading(
    "Executive Overview",
    "Key performance indicators summarizing patient admissions and readmission trends."
)

# ---------- Row 1 ----------

c1, c2, c3 = st.columns(3)

with c1:
    du.kpi_card(
        "Total Patients",
        f"{total_patients:,}",
        "Entire Dataset",
        accent="indigo"
    )

with c2:
    du.kpi_card(
        "Readmitted Patients",
        f"{readmitted_patients:,}",
        "Within 30 Days",
        accent="rose"
    )

with c3:
    du.kpi_card(
        "Readmission Rate",
        f"{readmission_rate:.2f}%",
        "Overall Readmission Rate",
        accent="coral"
    )

# ---------- Row 2 ----------

c4, c5, c6 = st.columns(3)

with c4:
    du.kpi_card(
        "Average Length of Stay",
        f"{avg_los:.1f} Days",
        "Across All Patients",
        accent="teal"
    )

with c5:
    du.kpi_card(
        "Average Hospital Cost",
        f"₹ {avg_cost:,.0f}",
        "Per Admission",
        accent="amber"
    )

with c6:
    du.kpi_card(
        "Average Patient Age",
        f"{avg_age:.1f} Years",
        "Entire Dataset",
        accent="blue"
    )

du.separator()

# ==========================================================
# PATIENT DEMOGRAPHICS
# ==========================================================

du.section_heading(
    "Patient Demographics",
    "Understand the distribution of patients by age and gender."
)

left, right = st.columns(2)

with left:

    age_labels = [
        "0-10",
        "11-20",
        "21-30",
        "31-40",
        "41-50",
        "51-60",
        "61-70",
        "71-80",
        "81-90",
        "91+"
    ]

    age_bins = [0,10,20,30,40,50,60,70,80,90,150]

    age_df = df.copy()

    age_df["Age Group"] = pd.cut(
        age_df["age"],
        bins=age_bins,
        labels=age_labels,
        include_lowest=True
    )

    du.histogram(
        df=age_df,
        column="Age Group",
        title="Age Distribution among all Patients",
        color="#6366F1",
        x_title="Age Group",
        y_title="Count of Patients"
    )

with right:

    du.donut_chart(
        df=df,
        column="gender",
        title="Gender Distribution among all Patients",
        colors=["#14B8A6", "#6366F1", "#F59E0B"]
    )

du.separator()

# ==========================================================
# HOSPITAL OPERATIONS
# ==========================================================

du.section_heading(
    "Hospital Operations",
    "Understand patient admission patterns and ward utilization."
)

left, right = st.columns(2)

with left:

    du.donut_chart(
        df=df,
        column="admit_type",
        title="Type of Admission among all Patients",
        colors=["#F59E0B", "#6366F1", "#14B8A6", "#F43F5E", "#8B5CF6"]
    )

with right:

    du.histogram(
        df=df,
        column="ward_type",
        title="Ward-wise Patient Distribution",
        color="#F59E0B",
        x_title="Ward Type",
        y_title="Count of Patients"
    )

du.separator()

# ==========================================================
# FINANCIAL INSIGHTS
# ==========================================================

du.section_heading(
    "Financial Insights",
    "Understand hospitalization costs and financial burden."
)

left, right = st.columns(2)

with left:

    # ==========================================================
    # Hospitalization Cost Buckets
    # ==========================================================

    cost_df = df.copy()

    cost_bins = [
        0,
        50_000,
        1_00_000,
        1_50_000,
        2_00_000,
        2_50_000,
        3_00_000,
        float("inf")
    ]

    cost_labels = [
        "0-50K",
        "50K-1L",
        "1L-1.5L",
        "1.5L-2L",
        "2L-2.5L",
        "2.5L-3L",
        ">3L"
    ]

    cost_df["Cost Bucket"] = pd.cut(
        cost_df["total_cost_inr"],
        bins=cost_bins,
        labels=cost_labels,
        include_lowest=True
    )

    bucket_counts = (
        cost_df["Cost Bucket"]
        .value_counts(sort=False)
        .reset_index()
    )

    bucket_counts.columns = [
        "Cost Bucket",
        "Patients"
    ]

    import plotly.express as px

    fig = px.bar(
        bucket_counts,
        x="Cost Bucket",
        y="Patients",
        title="Hospitalization Cost Distribution",
        text="Patients"
    )

    fig.update_traces(
        marker_color="#F97316",
        width=0.7,
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Hospitalization Cost",
        yaxis_title="Patients",
        height=550,
        margin=dict(
            l=20,
            r=80,
            t=45,
            b=80
        ),
        font=dict(
            family="Plus Jakarta Sans",
            size=17,
            color="#0F172A"
        ),
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(
                family="Plus Jakarta Sans",
                size=17,
                color="#0F172A"
            )
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0F172A"
            )
        )

    )

    fig.update_yaxes(
        range=[0, 76000],   # Just above the tallest bar (74,364)
        dtick=25000
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with right:

    du.donut_chart(
        df=df,
        column="cost_category",
        title="Hospital Cost Category Distribution",
        colors=["#F97316", "#14B8A6", "#6366F1", "#F43F5E", "#F59E0B"]
    )

du.separator()

# ==========================================================
# CLINICAL RISK FACTORS
# ==========================================================

du.section_heading(
    "Clinical Risk Factors",
    "Compare clinical indicators between readmitted and non-readmitted patients."
)

left, right = st.columns(2)

with left:

    # ==========================================================
    # Charlson Index vs Readmission Rate
    # ==========================================================

    charlson_df = df.copy()

    # Create Charlson Groups
    charlson_bins = [-1, 2, 4, 6, 8, 100]

    charlson_labels = [
        "0-2",
        "3-4",
        "5-6",
        "7-8",
        "9+"
    ]

    charlson_df["Charlson Group"] = pd.cut(
        charlson_df["charlson_index"],
        bins=charlson_bins,
        labels=charlson_labels
    )

    # Calculate Readmission Rate
    chart_df = (
        charlson_df
        .groupby("Charlson Group", observed=False)["readmitted_30d"]
        .mean()
        .reset_index()
    )

    chart_df["Readmission Rate"] = (
        chart_df["readmitted_30d"] * 100
    )

    # Plot
    fig = px.bar(
        chart_df,
        x="Charlson Group",
        y="Readmission Rate",
        text=chart_df["Readmission Rate"].round(1),
        title="Readmission Rate by Charlson Index",
        color_discrete_sequence=["#2563EB"]
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(

        height=600,

        plot_bgcolor="white",

        paper_bgcolor="white",

        margin=dict(
            l=20,
            r=80,
            t=45,
            b=80
        ),
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(
                family="Plus Jakarta Sans",
                size=17,
                color="#0F172A"
            )
        ),

        xaxis_title="Charlson Index",

        yaxis_title="Readmission Rate (%)",

        showlegend=False,
        font=dict(
            family="Plus Jakarta Sans",
            size=17,
            color="#0F172A"
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0F172A"
            )
        )

    )

    # Keep the same card height, just make the axis cleaner
    fig.update_yaxes(
        tickmode="array",
        tickvals=[0, 10, 20, 30],
        range=[0, 30]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with right:

    # ==========================================================
    # Length of Stay vs Readmission Rate
    # ==========================================================

    los_df = df.copy()

    los_bins = [
        0,
        3,
        7,
        14,
        21,
        100
    ]

    los_labels = [
        "1-3",
        "4-7",
        "8-14",
        "15-21",
        ">21"
    ]

    los_df["LOS Group"] = pd.cut(
        los_df["los_days"],
        bins=los_bins,
        labels=los_labels,
        include_lowest=True
    )

    chart_df = (
        los_df
        .groupby("LOS Group", observed=False)["readmitted_30d"]
        .mean()
        .reset_index()
    )

    chart_df["Readmission Rate"] = (
        chart_df["readmitted_30d"] * 100
    )

    fig = px.bar(

        chart_df,

        x="LOS Group",

        y="Readmission Rate",

        text=chart_df["Readmission Rate"].round(1),

        title="Readmission Rate by Length of Stay",

        color_discrete_sequence=["#8B5CF6"]

    )

    fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside",

        cliponaxis=False

    )

    fig.update_layout(

        height=600,

        plot_bgcolor="white",

        paper_bgcolor="white",

        margin=dict(
            l=20,
            r=80,
            t=45,
            b=80
        ),

        xaxis_title="Length of Stay (Days)",

        yaxis_title="Readmission Rate (%)",

        showlegend=False,

        font=dict(
            family="Plus Jakarta Sans",
            size=17,
            color="#0F172A"
        ),

        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(
                family="Plus Jakarta Sans",
                size=17,
                color="#0F172A"
            )
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0F172A"
            )
        )

    )

    fig.update_yaxes(

        range=[0,30],

        dtick=10

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

du.separator()

# ==========================================================
# READMISSION INSIGHTS
# ==========================================================

du.section_heading(
    "Readmission Insights",
    "Compare readmission rate across age groups and comorbidity counts."
)

left, right = st.columns(2)

with left:

    # ==========================================================
    # Readmission Rate by Age Group
    # ==========================================================

    age_df = df.copy()

    age_bins = [
        0,
        20,
        40,
        60,
        80,
        120
    ]

    age_labels = [
        "0-20",
        "21-40",
        "41-60",
        "61-80",
        "80+"
    ]

    age_df["Age Group"] = pd.cut(
        age_df["age"],
        bins=age_bins,
        labels=age_labels,
        include_lowest=True
    )

    chart_df = (
        age_df
        .groupby("Age Group", observed=False)["readmitted_30d"]
        .mean()
        .reset_index()
    )

    chart_df["Readmission Rate"] = (
        chart_df["readmitted_30d"] * 100
    )

    fig = px.bar(

        chart_df,

        x="Age Group",

        y="Readmission Rate",

        text=chart_df["Readmission Rate"].round(1),

        title="Readmission Rate by Age Group",

        color_discrete_sequence=["#10B981"],

        )


    fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside",

        cliponaxis=False

    )

    fig.update_layout(

        height=600,

        plot_bgcolor="white",

        paper_bgcolor="white",

        margin=dict(
            l=20,
            r=80,
            t=45,
            b=80
        ),

        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(
                family="Plus Jakarta Sans",
                size=17,
                color="#0F172A"
            )
        ),

        xaxis_title="Age Group",

        yaxis_title="Readmission Rate (%)",

        showlegend=False,

        font=dict(
            family="Plus Jakarta Sans",
            size=17,
            color="#0F172A"
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0F172A"
            )
        )

    )

    fig.update_yaxes(

        range=[0,30],

        dtick=10

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with right:

    # ==========================================================
    # Readmission Rate by Comorbidity Count
    # ==========================================================

    comorb_df = df.copy()

    comorb_bins = [
        -1,
        1,
        3,
        5,
        100
    ]

    comorb_labels = [
        "0-1",
        "2-3",
        "4-5",
        "6+"
    ]

    comorb_df["Comorbidity Group"] = pd.cut(
        comorb_df["comorbidity_count"],
        bins=comorb_bins,
        labels=comorb_labels
    )

    chart_df = (
        comorb_df
        .groupby("Comorbidity Group", observed=False)["readmitted_30d"]
        .mean()
        .reset_index()
    )

    chart_df["Readmission Rate"] = (
        chart_df["readmitted_30d"] * 100
    )

    fig = px.bar(

        chart_df,

        x="Comorbidity Group",

        y="Readmission Rate",

        text=chart_df["Readmission Rate"].round(1),

        title="Readmission Rate by Comorbidity (Diseases) Count",

        color_discrete_sequence=["#F43F5E"]

    )

    fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside",

        cliponaxis=False

    )

    fig.update_layout(

        height=600,

        plot_bgcolor="white",

        paper_bgcolor="white",

        margin=dict(
            l=20,
            r=80,
            t=45,
            b=80
        ),
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(
                family="Plus Jakarta Sans",
                size=17,
                color="#0F172A"
            )
        ),

        xaxis_title="Comorbidity Count",

        yaxis_title="Readmission Rate (%)",

        showlegend=False,

        font=dict(
            family="Plus Jakarta Sans",
            size=17,
            color="#0F172A"
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0F172A"
            )
        )

    )

    fig.update_yaxes(

        range=[0, 30],

        dtick=10

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

du.separator()