# DQ Validation Hub

A Streamlit application for data quality validation across Azure Synapse, Microsoft Fabric and Oracle databases, plus Excel-based file comparison. Built for the Data Quality Centre of Excellence (DQ COE).

## Tools included

| Tool | Description |
|---|---|
| 🏠 Home | Overview of all tools |
| 📈 Application Statistics | Usage telemetry: runs, durations and per-feature metrics |
| 🤖 AI DQ Orchestrator | AI-assisted validation (calls a local LLM endpoint, see Notes) |
| 📋 Validation Report Generator | Build a blank Excel validation report with a Summary sheet and one sheet per selected scenario |
| 🔍 Schema Validator | Compare columns, datatypes, row counts and null counts between source and target |
| 📄 File Generator | Run SQL queries and export results to Excel (one workbook or one file per query) |
| 🔄 File Comparator | Diff paired `_Source.xlsx` / `_Target.xlsx` files |
| 📑 MID File Validator | Compare two Excel files row by row using highlighted cells or mapped columns; outputs All Records, Mismatches, New Entries and Duplicates sheets |
| 📊 Fact Metric Validator | Compare aggregate metrics (SUM, AVG, MIN, MAX, COUNT) across environments |
| 🔑 Keys Validator | Orphan keys, duplicate check and null count checks on key columns |
| 🎨 Colour Record Filter | Extract colour-highlighted rows from an Excel file into a separate sheet |
| 🔌 Connections | Save and manage database connection profiles reused by every tool |

## Project structure

```
dq_hub/
├── application.py            # Entry point: login check, sidebar and routing
├── requirements.txt
├── packages.txt              # System packages (unixodbc) for Streamlit Cloud
├── auth/                     # Login
│   ├── auth.py               # Login form, session handling, logout
│   └── auth_config.json      # Users and roles
├── connections/              # Database connection profiles
│   ├── connection_manager.py # Read/write profiles (JSON)
│   ├── conn_picker.py        # Reusable connection dropdown widget
│   └── connections.json
├── modules/                  # One file per tool screen (each exposes run())
│   ├── Home.py
│   ├── Connections.py
│   ├── SchemaValidator.py
│   ├── FileGenerator.py
│   ├── FileComparator.py
│   ├── MIDFileValidator.py
│   ├── FactMetrics.py
│   ├── KeysValidator.py
│   ├── ColourFilter.py
│   ├── ValidationReportGenerator.py
│   ├── AIIntegration.py
│   └── AppStatistics.py
├── utils/
│   ├── db_utils.py           # SQLAlchemy engine builder
│   └── metrics_tracker.py    # Usage logging
└── data/
    └── app_statistics.json   # Auto-created at runtime (git-ignored)
```

The tool folder is named `modules/`, not `pages/`, on purpose. Streamlit builds its own navigation from a `pages/` folder, which would clash with the custom sidebar and bypass the login check in `application.py`.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
For Oracle support also install:
```bash
pip install oracledb
```

### 2. ODBC driver (Synapse and Fabric)
Install **ODBC Driver 17 for SQL Server** from Microsoft:
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### 3. Run the app
```bash
streamlit run application.py
```

## Login

The app requires sign-in before any tool is shown. Users and roles are defined in `auth/auth_config.json`:

```json
{ "users": { "username": { "password": "...", "role": "admin | user | viewer" } } }
```

- Change the default passwords before sharing the app with anyone.
- Passwords are stored in plain text. Keep the repository **private**, or move credentials to Streamlit secrets or hashed passwords before wider use.

## Connection profiles

Open **Connections** in the sidebar to save a profile once. Every tool then offers a dropdown to pick it.

- Supported environments: **Synapse**, **Fabric** (SQL analytics endpoint) and **Oracle**.
- Authentication options for Synapse and Fabric: `ActiveDirectoryDeviceCodeFlow` (recommended for mobile or remote servers), `ActiveDirectoryInteractive` (desktop browser pop-up), `ActiveDirectoryPassword` and `SQL`.
- Profiles are stored in `connections/connections.json`. They hold server and database names only; do not add credentials to this file.
- Oracle passwords are never stored. They are requested at runtime.

## File Comparator naming convention

Name files `TableName_Source.xlsx` and `TableName_Target.xlsx`. Upload both together and the tool pairs them automatically.

## Application statistics

Each tool logs its run time and counts to `data/app_statistics.json`, shown on the **Application Statistics** page. The file is created on first use and excluded from Git.

## Deployment notes

- On Streamlit Cloud, set the main file path to `application.py`. Paths are case-sensitive.
- `packages.txt` installs `unixodbc` only. Synapse and Fabric connections also need **ODBC Driver 17 for SQL Server** on the host machine.
- The AI DQ Orchestrator calls a local endpoint (`http://localhost:11434`), so it only works where that service is running.

## Notes

- All validation results can be downloaded as Excel reports.
- `connections/connections.json` and `data/app_statistics.json` are created automatically if missing.
