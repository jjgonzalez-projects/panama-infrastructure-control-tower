# Panama Infrastructure Delivery Control Tower

An interactive **Project Controls & AI Decision Support** prototype designed to demonstrate how infrastructure portfolio data can be transformed into actionable management insights.

🚀 **[Launch the Live Application](https://panama-infrastructure-control-tower.streamlit.app)**

![Panama Infrastructure Delivery Control Tower](Captura%20-%20UN%20.png)

> **Portfolio demonstration using simulated project data.**

## Overview

The Panama Infrastructure Delivery Control Tower combines structured project data, automated project controls analysis, interactive portfolio monitoring, and generative AI in a lightweight management decision-support application.

The tool provides both a **portfolio-level management view** and a **project-level drill-down**, allowing users to identify projects requiring attention and generate concise executive project briefs.

## Key Features

- Upload and analyze Excel-based project portfolios
- Automated workbook structure and column validation
- Portfolio-level management overview
- HIGH / MODERATE / LOW management attention classification
- Schedule delay monitoring
- Procurement performance monitoring
- Financial variance analysis
- Residual risk monitoring
- Cross-project Portfolio Management View
- Individual project drill-down
- AI-assisted Executive Project Brief
- Guardrails designed to prevent unsupported project assumptions

## Portfolio Management View

The application analyzes the portfolio and provides an executive overview including:

- Total projects
- Projects requiring HIGH attention
- Projects requiring MODERATE attention
- Projects requiring LOW attention
- Projects with Red procurement packages
- Projects with overdue milestones

A cross-project management table allows decision-makers to compare schedule, procurement, financial, and risk indicators across the portfolio.

## AI-Assisted Decision Support

For each selected project, the application can generate an **Executive Project Brief** using the available project-control indicators.

The AI layer is intentionally separated from the calculation layer:

**Python calculates the indicators and management rules first. Generative AI then interprets and communicates those structured results.**

The prompt includes guardrails requiring the model to distinguish evidence from interpretation and avoid inventing unsupported causes, contractual impacts, technical issues, or supplier problems.

## Architecture

Excel Portfolio  
↓  
Pandas Data Processing  
↓  
Project Controls Rules & KPI Calculation  
↓  
Portfolio Management Analysis  
↓  
Streamlit Interactive Dashboard  
↓  
OpenAI API  
↓  
AI-Assisted Executive Project Brief

## Technology Stack

- Python
- Pandas
- Streamlit
- OpenPyXL
- OpenAI API
- Excel
- GitHub
- Streamlit Community Cloud

## Demonstration Data

This application uses a **simulated infrastructure project portfolio created specifically for this demonstration**.

The dataset contains 12 fictional infrastructure projects and was designed to simulate realistic project-control scenarios across schedule, procurement, financial performance, and residual risk.

The data does **not represent actual projects, organizations, contractors, suppliers, budgets, or operational information**.

The simulated portfolio is used exclusively to demonstrate the application's analytical workflow, management-attention logic, portfolio monitoring capabilities, and AI-assisted decision support.

Users may also upload their own compatible Excel workbook to test the application with a different portfolio structure.


## Purpose

This prototype was developed as a portfolio demonstration of how **Project Management, Project Controls, Procurement, Risk Management, Data Analytics, and Generative AI** can be integrated into a practical decision-support workflow.

The project demonstrates the progression from structured portfolio data to management-level insights while maintaining a clear separation between deterministic calculations and AI-assisted interpretation.
