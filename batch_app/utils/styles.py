import streamlit as st

def load_css():
    """
    Loads custom CSS for the Hospital Readmission Dashboard.
    """

    st.markdown(
        """
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ==========================================================
   GLOBAL FONT
========================================================== */

html,
body,
.stApp,
[class*="css"],
[class*="st-"]{
    font-family: "Plus Jakarta Sans", sans-serif;
}

/* ==========================================================
   APP BACKGROUND
========================================================== */

.stApp{
    background: #F8FAFC;
}

.main .block-container{
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}

/* ==========================================================
   SIDEBAR — Dark Navy
========================================================== */

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: none;
    box-shadow: 4px 0 24px rgba(15,23,42,0.15);
    padding-top: 12px;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p {
    color: #FFFFFF;
}

section[data-testid="stSidebar"] .st-visually-hidden {
    display: none !important;
}

/* Hide Streamlit tooltips (like 'Keyboard shortcut' on buttons) */
div[data-baseweb="tooltip"] {
    display: none !important;
}

section[data-testid="stSidebar"] h1{
    font-size: 22px;
    font-weight: 700;
    color: #F8FAFC !important;
    margin-bottom: 20px;
}

/* Fix sidebar collapse button */
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button {
    font-size: 0 !important;
    background: transparent !important;
    border: 1.5px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    transition: all 0.2s ease !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button:hover {
    background: #FFFFFF !important;
    border-color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button svg,
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button span {
    display: none !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button::after {
    content: "Hide";
    font-size: 14px !important;
    font-weight: 600;
    color: #FFFFFF !important;
    letter-spacing: 0.5px;
    display: block;
    transition: color 0.2s ease !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button:hover::after {
    color: #000000 !important;
}

[data-testid="collapsedControl"] {
    color: #FFFFFF !important;
}
[data-testid="collapsedControl"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* Sidebar branded overrides */
section[data-testid="stSidebar"] .sidebar-brand-name{
    color: #F8FAFC !important;
}
section[data-testid="stSidebar"] .sidebar-brand-tag{
    color: #64748B !important;
}
section[data-testid="stSidebar"] .sidebar-version{
    color: #A5B4FC !important;
}

/* ==========================================================
   SIDEBAR NAVIGATION
========================================================== */

section[data-testid="stSidebar"] button{
    border-radius: 12px !important;
    border: none !important;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] button:hover{
    background: rgba(99,102,241,0.15) !important;
    color: #E0E7FF !important;
}

section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    color: #FFFFFF !important;
    border-radius: 10px !important;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] a:hover{
    background: rgba(99,102,241,0.12) !important;
    color: #E0E7FF !important;
}

section[data-testid="stSidebar"] a[aria-current="page"]{
    background: rgba(99,102,241,0.2) !important;
    color: #FFFFFF !important;
}

/* Highlight the "Try this" nav item (3rd item) */
ul[data-testid="stSidebarNavItems"] li:nth-child(3) a span {
    background: linear-gradient(90deg, #F43F5E, #F59E0B) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 800 !important;
    letter-spacing: 0.2px;
}

section[data-testid="stSidebar"] hr{
    border-color: rgba(148,163,184,0.2) !important;
}

/* ==========================================================
   KPI CARDS
========================================================== */

.kpi-card{
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04),
                0 4px 12px rgba(15,23,42,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card::before{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 16px 16px 0 0;
}

.kpi-card:hover{
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(15,23,42,0.08);
}

.kpi-card.accent-indigo::before{ background: linear-gradient(90deg,#6366F1,#818CF8); }
.kpi-card.accent-teal::before{   background: linear-gradient(90deg,#14B8A6,#2DD4BF); }
.kpi-card.accent-amber::before{  background: linear-gradient(90deg,#F59E0B,#FBBF24); }
.kpi-card.accent-coral::before{  background: linear-gradient(90deg,#F97316,#FB923C); }
.kpi-card.accent-emerald::before{background: linear-gradient(90deg,#10B981,#34D399); }
.kpi-card.accent-rose::before{   background: linear-gradient(90deg,#F43F5E,#FB7185); }
.kpi-card.accent-blue::before{   background: linear-gradient(90deg,#2563EB,#3B82F6); }
.kpi-card.accent-violet::before{ background: linear-gradient(90deg,#8B5CF6,#A78BFA); }

.kpi-title{
    color: #64748B;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

.kpi-value{
    color: #0F172A;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.2;
}

.kpi-desc{
    color: #94A3B8;
    font-size: 13px;
    margin-top: 8px;
    font-weight: 400;
}

/* ==========================================================
   PAGE TITLE
========================================================== */

.dashboard-title{
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}

.dashboard-subtitle{
    font-size: 16px;
    margin-bottom: 28px;
    font-weight: 400;
    line-height: 1.5;
}

/* ==========================================================
   SECTION HEADINGS (accent dot)
========================================================== */

.section-title{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.3px;
    margin-top: 14px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title::before{
    content: '';
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #6366F1;
    flex-shrink: 0;
}

.section-desc{
    font-size: 15px;
    line-height: 1.4;
    margin-bottom: 18px;
    padding-left: 18px;
}

/* ==========================================================
   SECTION GAP
========================================================== */

.section-gap{
    height: 40px;
}

/* ==========================================================
   PLOTLY CHART CONTAINER
========================================================== */

div[data-testid="stPlotlyChart"]{
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 16px;
    padding: 16px;
    margin-top: 8px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04),
                0 4px 12px rgba(15,23,42,0.03);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    overflow: hidden;
    position: relative;
}

div[data-testid="stPlotlyChart"]::before{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg,#6366F1,#14B8A6);
    border-radius: 16px 16px 0 0;
    z-index: 1;
}

div[data-testid="stPlotlyChart"]:hover{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(15,23,42,0.08);
}

/* ==========================================================
   STREAMLIT METRICS
========================================================== */

div[data-testid="stMetric"]{
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E8EDF5;
    padding: 18px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(15,23,42,0.06);
}

div[data-testid="stMetricLabel"]{
    font-weight: 600;
    color: #475569;
    font-size: 14px;
}

div[data-testid="stMetricValue"]{
    font-weight: 700;
    color: #0F172A;
}

/* ==========================================================
   LAST UPDATED CARD
========================================================== */

.update-card{
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 14px;
    padding: 14px 18px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
    position: relative;
    overflow: hidden;
}

.update-card::before{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg,#6366F1,#14B8A6);
}

.update-title{
    font-size: 12px;
    font-weight: 600;
    color: #64748B;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.update-date{
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
}

/* ==========================================================
   HIDE HEADER / FOOTER
========================================================== */

header{ visibility: hidden; }
footer{ visibility: hidden; }

/* ==========================================================
   REDUCE COLUMN GAP
========================================================== */

div[data-testid="stHorizontalBlock"]{
    gap: 1rem;
}

/* ==========================================================
   TABS
========================================================== */

div[data-testid="stTabs"] button[data-baseweb="tab"]{
    font-family: "Plus Jakarta Sans", sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: #64748B;
    border-bottom: 3px solid transparent;
    padding: 12px 24px;
    transition: all 0.2s ease;
}

div[data-testid="stTabs"] button[data-baseweb="tab"]:hover{
    color: #6366F1;
}

div[data-testid="stTabs"] button[aria-selected="true"]{
    color: #6366F1 !important;
    border-bottom-color: #6366F1 !important;
}

/* ==========================================================
   INPUT WIDGETS – uniform grey borders, white backgrounds
========================================================== */

/* Text & Number input wrappers – force white on ALL nested elements */
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="input"] > div,
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] div[data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    border-radius: 10px !important;
    border: 1px solid #E2E8F0 !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

/* The actual <input> element – transparent bg, dark text, NO inner border */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background-color: transparent !important;
    background: transparent !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    font-family: "Plus Jakarta Sans", sans-serif !important;
    border: none !important;
    box-shadow: none !important;
}

/* Number input step buttons */
div[data-testid="stNumberInput"] button {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #334155 !important;
    border-color: #E2E8F0 !important;
}

/* Focus state */
div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* Selectbox / Dropdown – opaque white, grey border */
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    border-radius: 10px !important;
    border: 1px solid #E2E8F0 !important;
    color: #0F172A !important;
    min-height: 42px !important;
}

/* Dropdown selected text – no overlap */
div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}

/* Dropdown arrow icon */
div[data-testid="stSelectbox"] svg {
    fill: #334155 !important;
}

/* Dropdown popup menu – opaque white */
div[data-baseweb="popover"],
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
ul[role="listbox"],
ul[role="listbox"] li {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #0F172A !important;
}

/* Dropdown menu hover */
div[data-baseweb="popover"] li:hover,
ul[role="listbox"] li:hover,
li[aria-selected="true"] {
    background-color: #EEF4FF !important;
}

/* Input labels */
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    color: #334155 !important;
    font-weight: 500 !important;
}

/* ==========================================================
   BUTTONS
========================================================== */

div.stButton > button{
    font-family: "Plus Jakarta Sans", sans-serif !important;
    font-weight: 600;
    border-radius: 12px;
    padding: 10px 24px;
    transition: all 0.2s ease;
    background: linear-gradient(135deg,#6366F1,#4F46E5) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.25);
}

div.stButton > button:hover{
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99,102,241,0.3) !important;
}

/* ==========================================================
   PROGRESS BAR
========================================================== */

div[data-testid="stProgress"] > div > div > div{
    background: linear-gradient(90deg,#14B8A6,#6366F1) !important;
    border-radius: 8px;
}

/* ==========================================================
   ALERT BOXES
========================================================== */

div[data-testid="stAlert"]{
    border-radius: 14px;
    font-weight: 500;
    border: 1px solid #E8EDF5;
}

/* ==========================================================
   SCROLLBAR
========================================================== */

::-webkit-scrollbar{ width: 6px; height: 6px; }
::-webkit-scrollbar-track{ background: transparent; }
::-webkit-scrollbar-thumb{ background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover{ background: #94A3B8; }

/* ==========================================================
   MODEL SUMMARY CARD
========================================================== */

.model-summary-card{
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04),
                0 4px 12px rgba(15,23,42,0.03);
    position: relative;
    overflow: hidden;
}

.model-summary-card::before{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg,#6366F1,#14B8A6,#F59E0B);
}

.model-summary-card .summary-item{
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #F1F5F9;
    gap: 12px;
}

.model-summary-card .summary-item:last-child{
    border-bottom: none;
}

.model-summary-card .summary-dot{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #6366F1;
    flex-shrink: 0;
}

.model-summary-card .summary-label{
    color: #64748B;
    font-size: 14px;
    font-weight: 500;
    min-width: 200px;
}

.model-summary-card .summary-value{
    color: #0F172A;
    font-size: 14px;
    font-weight: 600;
}

/* ==========================================================
   NAVIGATION BANNER
========================================================== */

.nav-banner{
    background: linear-gradient(135deg,#EEF2FF,#F0FDFA);
    border: 1px solid #E0E7FF;
    border-radius: 14px;
    padding: 18px 24px;
    margin-top: 12px;
    color: #4338CA;
    font-weight: 500;
    font-size: 15px;
}

/* ==========================================================
   SIDEBAR BRANDING
========================================================== */

.sidebar-brand{
    padding: 8px 0 20px 0;
    border-bottom: 1px solid rgba(148,163,184,0.2);
    margin-bottom: 16px;
}

.sidebar-brand-name{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin-bottom: 4px;
}

.sidebar-brand-tag{
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.3px;
}

.sidebar-version{
    display: inline-block;
    background: rgba(99,102,241,0.2);
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
    margin-top: 6px;
}

/* ==========================================================
   RESULT PANEL (Predict Page)
========================================================== */

.result-panel{
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04),
                0 4px 12px rgba(15,23,42,0.03);
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}

.result-panel::before{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
}

.result-panel.risk-low::before{      background: linear-gradient(90deg,#10B981,#34D399); }
.result-panel.risk-moderate::before{  background: linear-gradient(90deg,#F59E0B,#FBBF24); }
.result-panel.risk-high::before{      background: linear-gradient(90deg,#EF4444,#F87171); }

/* Probability display */
.prob-display{ text-align: center; padding: 20px; }

.prob-value{
    font-size: 56px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
}

.prob-value.risk-low{      color: #10B981; }
.prob-value.risk-moderate{  color: #F59E0B; }
.prob-value.risk-high{      color: #EF4444; }

.prob-label{
    font-size: 14px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Risk badge */
.risk-badge{
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.risk-badge.low{
    background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0;
}
.risk-badge.moderate{
    background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A;
}
.risk-badge.high{
    background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA;
}

/* Outcome card */
.outcome-card{
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px 24px;
    margin-top: 12px;
    border-left: 4px solid;
}

.outcome-card.risk-low{      border-left-color: #10B981; background: #F0FDF9; }
.outcome-card.risk-moderate{  border-left-color: #F59E0B; background: #FFFBEB; }
.outcome-card.risk-high{      border-left-color: #EF4444; background: #FEF2F2; }

.outcome-card p{
    margin: 0;
    color: #334155;
    font-size: 14px;
    line-height: 1.6;
}

/* ==========================================================
   RECOMMENDATION ITEMS
========================================================== */

.rec-item{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 18px;
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 4px solid;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.rec-item:hover{
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(15,23,42,0.06);
}

.rec-item.severity-high{     border-left-color: #EF4444; }
.rec-item.severity-moderate{  border-left-color: #F59E0B; }
.rec-item.severity-low{       border-left-color: #10B981; }
.rec-item.severity-info{      border-left-color: #6366F1; }

.rec-dot{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 5px;
}

.rec-dot.high{     background: #EF4444; }
.rec-dot.moderate{  background: #F59E0B; }
.rec-dot.low{       background: #10B981; }
.rec-dot.info{      background: #6366F1; }

.rec-text{
    color: #334155;
    font-size: 14px;
    font-weight: 500;
    line-height: 1.5;
}

/* ==========================================================
   FORM SECTION HEADER
========================================================== */

.form-section{
    font-size: 16px;
    font-weight: 700;
    margin-top: 8px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.form-section::before{
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #6366F1;
}

/* ==========================================================
   STYLED DIVIDER
========================================================== */

.styled-divider{
    height: 1px;
    background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
    margin: 24px 0;
    border: none;
}

</style>
        """,
        unsafe_allow_html=True
    )

