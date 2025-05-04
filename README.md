# DPDZero

# 📞 Agent Performance Analysis Pipeline

This repository contains a complete data pipeline and dashboard for analyzing the daily performance of agents based on call logs, login sessions, and loan contact attempts. The pipeline processes raw data, performs validation and transformation, computes key metrics, and displays insights using a Streamlit-based dashboard.

---

## 🚀 Project Overview

The goal of this project is to evaluate agent productivity and efficiency using operational data. It automates the ingestion, validation, merging, and feature engineering stages, then visualizes the final metrics in an interactive dashboard.

---

## 🧱 Pipeline Stages

### 1. **Data Ingestion**
Raw CSV files are ingested into the pipeline:
- `call_logs.csv`
- `user_logins.csv`
- `loan_contacted.csv`  
Files are stored in the `artifacts/raw/` directory.

### 2. **Data Validation**
The following columns are validated for correct format and missing values:
- `call_date`
- `agent_id`
- `org_id`

### 3. **Data Merging**
All three datasets are merged on `agent_id`, `org_id`, and `call_date` to create a unified daily activity view for each agent.

### 4. **Feature Engineering**
Computed metrics for each agent include:
- 📞 **Total Calls Made**  
- 💼 **Unique Loans Contacted**  
- ✅ **Connect Rate** = Completed Calls / Total Calls  
- ⏱ **Avg Call Duration (in minutes)**  
- 👤 **Presence** (1 if login_time exists, else 0)

---

## 📊 Streamlit Dashboard

Launch the interactive dashboard to:
- View daily performance summary
- Identify top performers
- Visualize connect rates, call durations, and volume
- Generate and copy a Slack-style summary
- Download the final report as a CSV

Run the dashboard locally:
```bash
streamlit run app.py
