import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def section_heading(title, description):
    """
    Displays a section title and description.
    """

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="section-desc">{description}</div>',
        unsafe_allow_html=True
    )



def kpi_card(title, value, description, accent="indigo"):
    """
    Renders a styled KPI card with a colour-coded top accent strip.
    Supported accents: indigo, teal, amber, coral, emerald, rose, blue, violet.
    """
    card = f"""
<div class="kpi-card accent-{accent}">
    <div class="kpi-title">{title}</div>
    <div class="kpi-value">{value}</div>
    <div class="kpi-desc">{description}</div>
</div>
"""

    st.markdown(card, unsafe_allow_html=True)

def apply_common_layout(fig, title, x_title="", y_title=""):
    """
    Applies a consistent layout across all Plotly charts.
    """

    fig.update_layout(

        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(
                family="Plus Jakarta Sans",
                size=17,
                color="#0F172A"
            )
        ),

        height=550,

        plot_bgcolor="#FFFFFF",

        paper_bgcolor="#FFFFFF",

        font=dict(
            family="Plus Jakarta Sans",
            size=13,
            color="#334155"
        ),

        margin=dict(
            l=20,
            r=40,
            t=50,
            b=80
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0F172A"
            )
        ),
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=False

    )

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor="#E2E8F0",
        ticks="outside",
        tickfont=dict(
            family="Plus Jakarta Sans",
            size=12
        )
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F1F5F9",
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor="#E2E8F0",
        ticks="outside",
        tickfont=dict(
            family="Plus Jakarta Sans",
            size=12
        )

    )

    return fig

def histogram(
    df,
    column,
    title,
    bins=20,
    color="#6366F1",
    x_title="",
    y_title="Count of Patients",
    y_dtick=None
):
    """
    Creates a histogram or categorical bar chart.
    """

    if str(df[column].dtype) == "category" or df[column].dtype == object:

        chart_df = (
            df[column]
            .value_counts(sort=False)
            .reset_index()
        )

        chart_df.columns = [column, "Count"]

        fig = px.bar(
            chart_df,
            x=column,
            y="Count",
            color_discrete_sequence=[color]
        )

    else:

        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            color_discrete_sequence=[color]
        )

    fig.update_traces(
        marker_line_width=0
    )

    fig = apply_common_layout(
        fig,
        title,
        x_title=x_title,
        y_title=y_title
    )

    if y_dtick is not None:
        fig.update_yaxes(dtick=y_dtick)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

def box_plot(
    df,
    x,
    y,
    title,
    color="#6366F1"
):
    """
    Creates a box plot.
    """

    fig = px.box(
        df,
        x=x,
        y=y,
        color_discrete_sequence=[color],
        points="outliers",
        height=550
    )

    fig = apply_common_layout(
    fig,
    title
    )

    fig.update_layout(
        margin=dict(
            l=20,
            r=40,
            t=40,
            b=10
        )

    )
    
    fig.update_yaxes(
        automargin=False,
        fixedrange=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


def donut_chart(
    df,
    column,
    title,
    hole=0.55,
    colors=None,
    
):
    """
    Creates a donut chart with a centre annotation showing total count.
    """

    if colors is None:
        colors = [
            "#6366F1",
            "#14B8A6",
            "#F59E0B",
            "#F43F5E",
            "#8B5CF6"
        ]

    chart_df = (
        df[column]
        .value_counts()
        .reset_index()
    )

    chart_df.columns = [
        column,
        "Count"
    ]

    total = chart_df["Count"].sum()

    fig = px.pie(
        chart_df,
        names=column,
        values="Count",
        hole=hole,
        color_discrete_sequence=colors

    )

    fig.update_traces(
        textfont_size=14,
        marker=dict(
            line=dict(
                color="white",
                width=2
            )
        )
    )

    fig.update_layout(

        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(
                family="Plus Jakarta Sans",
                size=17,
                color="#0F172A"
            )
        ),

        height=550,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=80
        ),

        font=dict(
            family="Plus Jakarta Sans",
            size=13,
            color="#334155"
        ),

        legend=dict(
            orientation="h",
            y=-0.15,
            yanchor="top",
            x=0.5,
            xanchor="center",
            font=dict(size=13)
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(
            family="Plus Jakarta Sans",
            size=13,
            color="#0F172A"
            )
        ),

        annotations=[
            dict(
                text=f"<b>{total:,}</b><br><span style='font-size:11px;color:#94A3B8'>Total</span>",
                x=0.5,
                y=0.5,
                font=dict(
                    family="Plus Jakarta Sans",
                    size=20,
                    color="#0F172A"
                ),
                showarrow=False
            )
        ]

    )

    fig.update_traces(
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

def separator():
    st.markdown(
        """
<div class="section-gap"></div>
""",
        unsafe_allow_html=True
    )