# DQ Validation Hub

A Streamlit application for data quality validation across Azure Synapse and Oracle databases.

## Tools included
| Tool | Description |
|---|---|
| 🔍 Schema Validator | Compare columns, datatypes and row counts between source and target |
| 📄 File Generator | Run SQL queries and export results to Excel |
| 📁 File Comparator | Diff paired Source / Target Excel files |
| 📊 Fact Metrics | Compare numeric metric sums across Synapse / Oracle |
| 🔑 Keys Validator | Orphan keys, duplicate check, null count (4 scenarios) |
| 🎨 Colour Filter | Extract colour-highlighted rows from Excel |
| 🔌 Connections | Save and manage database profiles reused across all tools |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

For Oracle support also install:
```bash
pip install oracledb
```

### 2. ODBC Driver (for Synapse)
Install **ODBC Driver 17 for SQL Server** from Microsoft:
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### 3. Run the app
```bash
streamlit run application.py
```

## Project structure
```
dq_hub/
├── application.py            # Main entry point, login check and routing
├── requirements.txt
├── packages.txt              # System packages (unixodbc) for Streamlit Cloud
├── auth/                     # Login
│   ├── auth.py
│   └── auth_config.json
├── connections/              # Database connection profiles
│   ├── connection_manager.py # JSON read/write for profiles
│   ├── conn_picker.py        # Reusable connection dropdown widget
│   └── connections.json
├── modules/                  # One file per tool screen (each has run())
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
    └── app_statistics.json   # Auto-created at runtime
```

> The tool folder is named `modules/` (not `pages/`) on purpose: Streamlit
> auto-builds its own navigation from a `pages/` folder, which would clash with
> the custom sidebar in `application.py`.

## Connection profiles
Go to **Connections** in the sidebar to save a profile once.
Every tool then shows a dropdown to pick that profile — no re-entering server/database details.

Profiles are stored in `connections/connections.json`.
**Do not commit this file if it contains sensitive credentials.**

## File Comparator naming convention
Files must be named: `TableName_Source.xlsx` and `TableName_Target.xlsx`
Upload both files together and the tool auto-pairs them.

## Notes
- Passwords for Oracle are not stored in profiles — enter them at runtime in the tool.
- The `connections.json` file is created automatically on first save.
- All validation results can be downloaded as Excel reports.
