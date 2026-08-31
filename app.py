
import streamlit as st

st.set_page_config(
    page_title="Panama Infrastructure Delivery",
    page_icon="📊",
    layout="wide"
)

import pandas as pd
import os
from openai import OpenAI

# --------------------------------
# 1. CONFIGURACIÓN
# --------------------------------

st.set_page_config(
    page_title="Panama Infrastructure Delivery Control Tower",
    layout="wide"
)

archivo = "Panama_Infrastructure_Delivery_Portfolio_MVP.xlsx"

# --------------------------------
# 2. CARGAR DATOS
# --------------------------------

projects = pd.read_excel(archivo, sheet_name="Projects")
milestones = pd.read_excel(archivo, sheet_name="Milestones")
procurement = pd.read_excel(archivo, sheet_name="Procurement")
risks = pd.read_excel(archivo, sheet_name="Risks")
financials = pd.read_excel(archivo, sheet_name="Financials")


# --------------------------------
# 3. FUNCIÓN DE ANÁLISIS
# --------------------------------

def analyze_project(project_id):

    # Milestones
    project_milestones = milestones[
        milestones["Project ID"] == project_id
    ]

    overdue_milestones = project_milestones[
        project_milestones["Status"] == "Overdue"
    ]

    cantidad_overdue = len(overdue_milestones)

    if cantidad_overdue > 0:
        max_schedule_delay = overdue_milestones[
            "Days Variance / Overdue"
        ].max()
    else:
        max_schedule_delay = 0


    # Procurement
    project_procurement = procurement[
        procurement["Project ID"] == project_id
    ]

    red_procurement = project_procurement[
        project_procurement["RAG"] == "Red"
    ]

    cantidad_red_procurement = len(red_procurement)

    if len(project_procurement) > 0:
        max_procurement_delay = project_procurement[
            "Days vs Plan"
        ].max()
    else:
        max_procurement_delay = 0


    # Risks
    project_risks = risks[
        risks["Project ID"] == project_id
    ]

    if len(project_risks) > 0:
        max_risk_score = project_risks[
            "Residual Score"
        ].max()
    else:
        max_risk_score = 0


    # Financials
    project_financials = financials[
        financials["Project ID"] == project_id
    ]

    if len(project_financials) > 0:
        variance_pct = project_financials[
            "Variance %"
        ].iloc[0]
    else:
        variance_pct = 0


    # Management Attention
    attention_points = 0

    if cantidad_overdue > 0:
        attention_points += 1

    if cantidad_red_procurement > 0:
        attention_points += 1

    if variance_pct > 0.05:
        attention_points += 1

    if max_risk_score >= 15:
        attention_points += 1


    if attention_points >= 3:
        attention_level = "HIGH"
    elif attention_points == 2:
        attention_level = "MODERATE"
    else:
        attention_level = "LOW"


    return {
        "project_id": project_id,
        "attention_level": attention_level,
        "overdue_milestones": cantidad_overdue,
        "max_schedule_delay": max_schedule_delay,
        "red_procurement_packages": cantidad_red_procurement,
        "max_procurement_delay": max_procurement_delay,
        "financial_variance_pct": round(variance_pct * 100, 2),
        "max_risk_score": max_risk_score
    }


# --------------------------------
# 4. INTERFAZ
# --------------------------------

st.markdown("""
<div style="margin-bottom: 1.5rem;">
<p style="font-size:13px; font-weight:700; letter-spacing:2px; color:#94A3B8; margin:0 0 8px 0;">
PANAMA INFRASTRUCTURE DELIVERY
</p>
<h1 style="font-size:38px; font-weight:700; line-height:1.15; margin:0 0 8px 0;">
Project Controls & AI Decision Support
</h1>
<p style="font-size:15px; color:#94A3B8; margin:0;">
Portfolio Demonstration · Simulated Data
</p>
</div>
""", unsafe_allow_html=True)

project_options = {
    f'{row["Project ID"]} · {row["Project Name"]}': row["Project ID"]
    for _, row in projects.iterrows()
}

selected_project = st.selectbox(
    "Project Selection",
    list(project_options.keys())
)

project_id = project_options[selected_project]

resultado = analyze_project(project_id)

project_name = projects.loc[
    projects["Project ID"] == project_id,
    "Project Name"
].iloc[0]

st.subheader(project_name)


# --------------------------------

# --------------------------------
# 5. KPIs - EXECUTIVE DASHBOARD
# --------------------------------

# Color según Management Attention
attention_colors = {
    "HIGH": ("#FEE2E2", "#B91C1C", "#EF4444"),
    "MODERATE": ("#FEF3C7", "#92400E", "#F59E0B"),
    "LOW": ("#DCFCE7", "#166534", "#22C55E")
}

badge_bg, badge_text, badge_dot = attention_colors[
    resultado["attention_level"]
]

# Estilos visuales
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.executive-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #64748B;
    margin-bottom: 0.35rem;
}

.attention-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 1.4rem;
}

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px 22px;
    min-height: 145px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}

.kpi-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #64748B;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.1;
}

.kpi-subtitle {
    font-size: 0.85rem;
    color: #64748B;
    margin-top: 9px;
}

</style>
""", unsafe_allow_html=True)


# Management Attention
st.markdown(
    f"""
    <div class="executive-label">PROJECT HEALTH</div>
    <div class="attention-badge"
         style="background:{badge_bg}; color:{badge_text};">
        <span style="
            width:9px;
            height:9px;
            border-radius:50%;
            background:{badge_dot};
            display:inline-block;">
        </span>
        {resultado["attention_level"]} MANAGEMENT ATTENTION
    </div>
    """,
    unsafe_allow_html=True
)


# Cuatro tarjetas ejecutivas
col_schedule, col_procurement, col_financial, col_risk = st.columns(4)

with col_schedule:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">SCHEDULE</div>
            <div class="kpi-value">{resultado["max_schedule_delay"]} days</div>
            <div class="kpi-subtitle">
                {resultado["overdue_milestones"]} overdue milestone(s)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_procurement:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">PROCUREMENT</div>
            <div class="kpi-value">{resultado["red_procurement_packages"]} Red</div>
            <div class="kpi-subtitle">
                {resultado["max_procurement_delay"]} days maximum delay
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_financial:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">FINANCIAL</div>
            <div class="kpi-value">{resultado["financial_variance_pct"]}%</div>
            <div class="kpi-subtitle">
                Forecast variance
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_risk:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">RISK</div>
            <div class="kpi-value">{resultado["max_risk_score"]}</div>
            <div class="kpi-subtitle">
                Maximum residual risk score
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()



# --------------------------------
# 6. AI EXECUTIVE BRIEF
# --------------------------------

st.markdown("""
<div style="margin-top:0.5rem;">
<p style="font-size:12px; font-weight:700; letter-spacing:1.6px; color:#64748B; margin:0 0 6px 0;">
AI-ASSISTED MANAGEMENT ANALYSIS
</p>
<h2 style="margin:0 0 6px 0;">
Executive Project Brief
</h2>
<p style="color:#94A3B8; font-size:14px; margin:0 0 18px 0;">
Generate a management-oriented interpretation using the project indicators above.
</p>
</div>
""", unsafe_allow_html=True)


if st.button(
    "✦ Generate Executive Brief",
    type="primary"
):

    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
    )

    prompt = f"""
You are a Project Controls Assistant supporting executive decision-making.

Analyze the following infrastructure project using ONLY
the project evidence provided below.

Project ID: {resultado["project_id"]}
Project Name: {project_name}
Management Attention: {resultado["attention_level"]}
Overdue Milestones: {resultado["overdue_milestones"]}
Maximum Schedule Delay: {resultado["max_schedule_delay"]} days
Red Procurement Packages: {resultado["red_procurement_packages"]}
Maximum Procurement Delay: {resultado["max_procurement_delay"]} days
Financial Variance: {resultado["financial_variance_pct"]}%
Maximum Residual Risk Score: {resultado["max_risk_score"]}

Provide exactly these sections:

## 1. Executive Summary

## 2. Evidence from the Data

## 3. Management Interpretation

## 4. Recommended Actions

Requirements:
- Use only the facts provided as project evidence.
- Do not invent causes, contractual conditions, supplier issues,
  technical impacts, or project circumstances not supported by the data.
- Clearly distinguish facts from interpretation.
- Recommendations may be proposed but must not be presented as facts.
- Keep the response concise and executive-oriented.
"""

    with st.spinner(
        "Analyzing schedule, procurement, financial and risk indicators..."
    ):

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

    st.markdown("")

    with st.container(border=True):

        st.markdown(
            """
            **AI-GENERATED MANAGEMENT BRIEF**

            *Based on calculated project indicators and simulated portfolio data.*
            """
        )

        st.divider()

        st.markdown(response.output_text)


st.markdown("""
<div style="
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #334155;
    color: #64748B;
    font-size: 12px;
">
Portfolio Demonstration · Simulated Data · Python · Pandas · Streamlit · OpenAI API
</div>
""", unsafe_allow_html=True)
