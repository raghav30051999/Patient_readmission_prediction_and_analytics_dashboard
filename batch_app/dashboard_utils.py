import streamlit as st


def separator():
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)


def section_heading(title, description=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

    if description:
        st.markdown(f'<div class="section-desc">{description}</div>', unsafe_allow_html=True)


def kpi_card(title, value, description=None, accent="indigo"):
    desc_html = f'<div class="kpi-desc">{description}</div>' if description else ""

    st.markdown(
        f"""
        <div class="kpi-card accent-{accent}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            {desc_html}
        </div>
        """,
        unsafe_allow_html=True
    )