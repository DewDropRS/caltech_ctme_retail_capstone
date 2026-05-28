# Caltech CTME Data Science Bootcamp
## Capstone Project 3: Retail Customer Segmentation

Customer segmentation using RFM (Recency, Frequency, Monetary) analysis and 
k-means clustering on a UK-based online retail dataset spanning Dec 2010 – Dec 2011.

---

## What I Learned

_To be filled in as project progresses._

---

## Features

### Core Requirements
- Preliminary data inspection and cleaning (nulls, duplicates, cancellations)
- Cohort analysis: monthly cohorts, active customer counts, retention rate heatmap
- RFM model: recency, frequency, and monetary metrics per customer
- RFM segmentation: quartile scoring, segment labels, RFM score
- K-means clustering: log transformation, standardization, elbow method, cluster profiles
- Visualizations: country spend, top 15 products, orders by hour, RFM distributions, cluster heatmap

### Enhancements
- SHAP (SHapley Additive exPlanations) values for cluster explainability
- Formal unit test suite using pytest
- Structured JSON logging with rotating file handler
- Proper package structure using pyproject.toml
- Containerized pipeline using Docker

---

## Tech Stack

- Python 3.10+
- pandas, numpy
- scikit-learn (k-means, StandardScaler)
- XGBoost (classifier for SHAP explainability layer)
- SHAP
- matplotlib, seaborn
- openpyxl (Excel file reading)
- python-json-logger
- pytest

---

## Installation

This project uses `pyproject.toml` for dependency management and is installed
as an editable package — no `sys.path` hacks needed.

1. Clone the repository:
```bash
   git clone https://github.com/DewDropRS/caltech_ctme_retail_capstone.git
   cd caltech_ctme_retail_capstone
```

2. Create and activate a virtual environment:
```bash
   python -m venv .venv
   source .venv/bin/activate        # Mac/Linux
   .venv\Scripts\activate           # Windows
```

3. Install the project and all dependencies:
```bash
   pip install -e ".[dev]"
```
   The `-e` flag installs the project in editable mode. The `[dev]` flag also
   installs pytest for running tests.

   Note: `pyproject.toml` is a configuration file, not a Python script — always
   run package and environment commands from the terminal, not the PyCharm run
   button. Any time you add a new dependency to `pyproject.toml`, re-run
   `pip install -e ".[dev]"` to install it.

4. Place the dataset in the expected location:
```
   data/raw/Online_Retail.xlsx
```

## How to Run

_To be filled in once main.py is complete._

---

## Project Structure


## Working Remotely (iPad / Browser)

This project supports browser-based development via GitHub Codespaces, 
allowing you to work from any device without a local Python installation.

### Setup

1. Go to the repository on GitHub
2. Click the green **Code** button → **Codespaces** tab
3. Click **Create codespace on main**
4. Wait approximately one minute for the environment to load
5. In the Codespaces terminal, install dependencies:
```bash
   pip install -e ".[dev]"
```

### Notes

- Codespaces provides a full VS Code environment in the browser
- All project files are available immediately — no cloning needed
- Dependencies must be reinstalled each time a new Codespace is created
- Outputs generated in Codespaces are not automatically synced to your 
  local machine — commit and push changes to preserve them
- GitHub Free tier includes 120 core hours per month of Codespaces usage