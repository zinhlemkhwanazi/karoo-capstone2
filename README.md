# Karoo Agriculture Capstone: Q4 Performance Report

## Overview
This project delivers an automated **Q4 regional performance report** for **Karoo Organics**, replacing manual Excel-based reporting. The solution combines **relational database design**, **SQL analytics**, and **Python automation** to track actual revenue against sales targets and identify top-performing suppliers per region.

---

## Project Objectives
- Extend the existing Karoo Agricultural database to support **sales target tracking**
- Load baseline operational data from CSV files into MySQL
- Perform analytical SQL queries for:
  - Regional performance vs sales targets
  - Top suppliers per region
- Automate report generation using Python
- Export results to CSV for leadership consumption

---

## Tech Stack
- **Database:** MySQL Server 2022 (Windows Authentication)
- **Language:** Python 3.12.5
- **Libraries:** pandas, pyodbc,SQLAlchemy
- **Data Storage:** CSV (input & reporting)
- **Version Control:** Git & GitHub

---
## Database Design Summary
### Core Tables (Baseline)

Suppliers – Supplier master data including region

Orders – Transactional order data (Q4 2025 focus)

Sales_Targets – Regional quarterly sales targets

Primary and foreign keys enforce referential integrity, while constraints ensure data consistency.

## Key Analytical Outputs

1. Regional Performance vs Targets

Actual revenue per region

Target amount per region

Percentage of target achieved (CASE-based calculation)

2. Top Suppliers per Region

Uses RANK() with PARTITION BY region

Identifies top 3 suppliers by total revenue per region

## Automation Workflow
The generate_q4_report.py script:

- Connects to MySQL
- Executes analytical SQL queries
- Saves results to q4_performance.csv
- Prints a concise summary to the console
- Handles errors safely and closes database connections

This ensures the report can be regenerated on demand with no manual intervention.

## Repository Structure

```text
karoo-capstone1-Zuhayr/
│
├── schema.sql
│   └── Database schema definitions (DDL)
│
├── load_data.py
│   └── Loads CSV data into MySQL tables using parameterised inserts
│
├── analytics.sql
│   └── Analytical SQL queries used for reporting
│
├── generate_q4_report.py
│   └── Python automation script that runs analytics and exports results
│
├── q4_performance.csv
│   └── Generated report output (regional performance & rankings)
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Excludes environment files, virtual envs, editor configs
│
└── README.md
