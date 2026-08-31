
import streamlit as st
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

archivo = "/content/Panama_Infrastructure_Delivery_Portfolio_MVP.xlsx"

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

st.title("Panama Infrastructure Delivery Control Tower")

st.caption(
    "Project Controls AI Assistant | Portfolio Demonstration | Simulated Data"
)

project_id = st.selectbox(
    "Select Project",
    projects["Project ID"].tolist()
)

resultado = analyze_project(project_id)

project_name = projects.loc[
    projects["Project ID"] == project_id,
    "Project Name"
].iloc[0]

st.subheader(project_name)


# --------------------------------
# 5. KPIs
# --------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Management Attention",
        resultado["attention_level"]
    )

with col2:
    st.metric(
        "Overdue Milestones",
        resultado["overdue_milestones"]
    )

with col3:
    st.metric(
        "Max Schedule Delay",
        f'{resultado["max_schedule_delay"]} days'
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Red Procurement Packages",
        resultado["red_procurement_packages"]
    )

with col5:
    st.metric(
        "Financial Variance",
        f'{resultado["financial_variance_pct"]}%'
    )

with col6:
    st.metric(
        "Maximum Risk Score",
        resultado["max_risk_score"]
    )

st.write(
    "Maximum Procurement Delay:",
    resultado["max_procurement_delay"],
    "days"
)

st.divider()


# --------------------------------
# 6. AI EXECUTIVE BRIEF
# --------------------------------

st.subheader("AI Executive Project Brief")

if st.button("Generate AI Executive Brief"):

    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
    )

    prompt = f"""
You are a Project Controls Assistant.

Analyze the following infrastructure project using ONLY
the data provided below.

Project ID: {resultado["project_id"]}
Project Name: {project_name}
Management Attention: {resultado["attention_level"]}
Overdue Milestones: {resultado["overdue_milestones"]}
Maximum Schedule Delay: {resultado["max_schedule_delay"]} days
Red Procurement Packages: {resultado["red_procurement_packages"]}
Maximum Procurement Delay: {resultado["max_procurement_delay"]} days
Financial Variance: {resultado["financial_variance_pct"]}%
Maximum Residual Risk Score: {resultado["max_risk_score"]}

Provide:

## 1. Executive Summary

## 2. Evidence from the Data

## 3. Management Interpretation

## 4. Recommended Actions

Do not invent project facts that are not supported by the data.
Clearly distinguish facts from management interpretation.
"""

    with st.spinner("Analyzing project..."):

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

    st.markdown(response.output_text)
