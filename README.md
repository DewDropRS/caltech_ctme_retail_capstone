# Retail Capstone: Customer Segmentation
## Customer segmentation using RFM (Recency, Frequency, Monetary) analysis and k-means clustering on a UK-based online retail dataset spanning Dec 2010 – Dec 2011.
*Caltech Center for Technology & Management Education (CTME) — Data Science Bootcamp*

---

## Features

### Core Requirements
- Preliminary data inspection and cleaning (nulls, duplicates, cancellations)
- Cohort analysis: monthly cohorts, active customer counts, retention rate heatmap
- RFM model: recency, frequency, and monetary metrics per customer
- RFM segmentation: quartile scoring, segment labels, RFM score
- K-means clustering: log transformation, standardization, elbow method, cluster profiles
- Visualizations: country spend, top products, orders by hour, RFM distributions, cluster heatmap

### Enhancements:
### SHAP (SHapley Additive exPlanations)
SHAP values are used to explain which RFM features drive K-Means cluster assignments. 
Key applications include:
- Feature importance — identifying which of recency, frequency, and monetary value 
  most influences cluster membership
- Data exploration — understanding patterns in how customer behavior maps to segments
- Model debugging — identifying which features may be causing unexpected cluster assignments

#### How to Read the SHAP Beeswarm Plot
Each plot represents a cluster and each dot represents one customer. Reading the plot:

- **X-axis (SHAP value)** — how much a feature pushes the prediction toward (right, positive) 
  or away from (left, negative) a given cluster
- **Color** — the actual raw RFM metric value for that customer. Red/pink = high feature 
  value (e.g. high spend, high frequency, or many days since last purchase). Blue = low 
  feature value (e.g. low spend, few purchases, or purchased recently). Color tells you 
  *what kind* of customer it is; x-axis position tells you *how strongly* that feature 
  influenced their cluster assignment. 
- **Density bar** — the vertical bar shows where most customers are concentrated
- **Wide spread to the right** — that feature strongly drives membership in that cluster
- **Most dots left of 0** — most customers do not belong to that cluster, 
  which is expected for small or exclusive segments

#### How to Read the SHAP Bar Plot
Each bar represents a feature (recency, frequency, monetary). 

- **Bar length** — total mean absolute SHAP value across all clusters; 
  longer bars indicate more important features overall
- **Colored segments** — each color represents a cluster's contribution 
  to that feature's overall importance
- **X-axis** — mean absolute SHAP value; larger = stronger average impact 
  on cluster assignment

### Formal unit test suite using pytest
Five unit tests cover the core data cleaning functions: cancellation removal, 
invalid value removal, missing CustomerID removal, duplicate removal, and 
non-product record removal. Tests run against a small synthetic DataFrame 
defined in `conftest.py` — a controlled sample with known values covering 
each test scenario independently.

**Running the tests:**
```bash
python -m pytest tests/ -v
```

The `-v` flag enables verbose output showing each test name and pass/fail status.

Note: pytest is installed as part of the `[dev]` optional dependencies. 
Make sure you ran `pip install -e ".[dev]"` and not just `pip install -e .`

**Test file structure:**
- `tests/conftest.py` — defines the `sample_df` fixture, a synthetic 6-row DataFrame 
  that mimics the real retail data structure with rows covering valid transactions, 
  cancellations, duplicates, null CustomerIDs, and invalid values
- `tests/test_data_cleaning.py` — five test functions, each testing one cleaning function 
  in isolation against a fresh copy of `sample_df`

**Key concept:** Tests verify function behavior, not the real dataset. Each test 
function receives an independent fresh copy of `sample_df` from pytest — changes 
made in one test do not affect another.

### Structured JSON logging with rotating file handler
All pipeline events are logged as structured JSON to `outputs/pipeline.log` with a 
rotating file handler that caps log size at 5MB and retains the 3 most recent files. 
Each log entry includes timestamp, log level, module name, and message.

### Proper package structure using pyproject.toml
Dependencies are managed through `pyproject.toml` — a single configuration file that 
replaces the need for `requirements.txt` and `setup.py`. The project is installed in 
editable mode (`pip install -e ".[dev]"`) so imports resolve correctly without any 
`sys.path` manipulation.

### Containerized pipeline using Docker
The full pipeline is containerized using Docker for reproducible deployment across any 
platform. A non-privileged user is used for security, and output directories are 
pre-created with appropriate permissions. Data and outputs are mounted as volumes at 
runtime rather than baked into the image.

---

## Tech Stack

| Tool                | Purpose |
|---------------------|---------|
| Python 3.10+        | Core programming language |
| pandas, numpy       | Data manipulation and numerical computing |
| scikit-learn        | K-Means clustering and StandardScaler normalization |
| XGBoost             | Classifier trained on cluster labels for SHAP explainability |
| SHAP                | Feature importance and model explainability |
| matplotlib, seaborn | Data visualization and plot generation |
| openpyxl            | Excel file reading (.xlsx) |
| python-json-logger  | Structured JSON logging with rotating file handler |
| pytest              | Unit testing |
| Docker              | Containerized pipeline for reproducible deployment |
| pyproject.toml      | Dependency management and editable package installation |

---

## Setup

### Prerequisites (both methods)

1. Clone the repository:
```bash
git clone https://github.com/DewDropRS/caltech_ctme_retail_capstone.git
cd caltech_ctme_retail_capstone
```

2. Place the dataset in the expected location:
    
    data/raw/online_retail.xlsx

---
### Option 1: Local Development

Use this method for development and testing. Requires Python 3.10+.

This project uses `pyproject.toml` for dependency management and is installed
as an editable package — no `sys.path` hacks needed.

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

2. Install the project and all dependencies:
```bash
# To run the pipeline only:
pip install -e .

# To also run tests:
pip install -e ".[dev]"
```
The `-e` flag installs the project in editable mode. The `[dev]` flag also
installs pytest for running tests.

Note: `pyproject.toml` is a configuration file, not a Python script — always
run package and environment commands from the terminal, not the PyCharm run
button. Any time you add a new dependency to `pyproject.toml`, re-run
`pip install -e ".[dev]"` to install it.

3. Run the pipeline:
```bash
python main.py
```

---

### Option 2: Docker

Use this method for reproducible deployment on any platform without a local 
Python setup. Requires Docker Desktop.

1. Build the image:
```bash
docker build -t retail-capstone .
```

2. Run the pipeline with data and outputs mounted:
```bash
docker run \
  -v "/path/to/data:/app/data" \
  -v "/path/to/outputs:/app/outputs" \
  retail-capstone
```

Replace `/path/to/data` and `/path/to/outputs` with your local paths.

---

### Running Tests

```bash
python -m pytest tests/ -v
```

---

## Outputs

Outputs are saved to the following directories:

- `outputs/figures/` — all plots and visualizations
- `outputs/data/` — customer-level RFM scores and viz-ready export
- `outputs/reports/` — descriptive stats, RFM summary, cluster profiles
- `outputs/models/` — trained K-Means model (`.joblib`)
- `outputs/pipeline.log` — structured JSON pipeline log

---

## Project Structure

```
caltech_ctme_retail_capstone/
├── src/
│   ├── __init__.py
│   ├── config.py           # All constants, file paths, and model settings
│   ├── logger.py           # Structured JSON logging with rotating file handler
│   ├── data_loader.py      # Ingests raw Excel data and logs basic info
│   ├── data_cleaning.py    # Removes cancellations, invalids, nulls, duplicates
│   ├── eda.py              # Exploratory data analysis and visualizations
│   ├── cohort_analysis.py  # Monthly cohorts and retention rate heatmap
│   ├── rfm_model.py        # RFM metrics, quartile scoring, and segmentation
│   ├── kmeans_model.py     # K-Means clustering, elbow method, cluster profiles
│   ├── shap_explainer.py   # SHAP feature importance on cluster assignments
│   └── data_exporter.py    # Exports viz-ready CSV for BI dashboards
├── data/
│   └── raw/                # Place online_retail.xlsx here (not tracked in git)
├── outputs/
│   ├── figures/            # All saved plots and visualizations
│   ├── data/               # Customer-level CSV exports
│   ├── reports/            # Aggregated analytical summaries
│   └── models/             # Saved K-Means model (.joblib)
├── tests/
│   ├── conftest.py         # Shared pytest fixtures
│   └── test_data_cleaning.py
├── docs/
│   ├── conventional_commits_guide.md
│   └── git_cheatsheet.md
├── main.py                 # Pipeline entry point
├── pyproject.toml          # Dependency management and package configuration
├── Dockerfile              # Containerized pipeline
├── .dockerignore
├── .gitignore
└── README.md
```

---

## Findings

### Data Cleaning
Of the original 541,909 transactions, 391,183 (72%) were retained for analysis 
after removing 150,726 records across five cleaning steps.

- The largest source of data loss was missing CustomerID — 133,359 rows representing 
  customers who could not be tracked for RFM analysis
- 9,288 cancellation transactions were removed as they do not represent completed sales
- 1,549 non-product records (postage, bank charges, manual entries) were excluded
- 1,338 rows with invalid Quantity or UnitPrice values were removed
- 5,192 duplicate rows were dropped

### EDA

- **Top Most Purchased Products** — Purchase volume is highly distributed across products. 
  The top-selling item, "PAPER CRAFT - LITTLE BIRDIE", accounts for only 1.6% of total 
  units sold, indicating no single product dominates sales.

- **Top Five Countries by Transaction Volume** — As expected for a UK-based online 
  retailer, 89.2% of transactions originated from the United Kingdom. Germany ranked 
  second at 2.2%, followed by France, EIRE, and Spain. The remaining 33 countries 
  combined account for just 4.1% of transactions.

- **Quantity** — The distribution is multimodal with two distinct peaks — one around 
  1-2 units and another centered around 10 units — suggesting two buying patterns: 
  small individual purchases and larger round-number bulk orders, likely from wholesale 
  customers. The 75th percentile is 12 units with 6.5% of records identified as outliers. 
  Outliers were retained as the log transformation applied during K-Means preprocessing 
  reduces their influence on clustering.

- **Unit Price** — The distribution is roughly bell-shaped on log scale, centered around 
  £1-£3, consistent with a low-cost novelty and gift retailer. The mean unit price is 
  £2.87 with 8.4% of records identified as outliers, reflecting a small number of 
  high-value items such as furniture and large decorative pieces. Outliers were retained 
  for the same reason as Quantity.

- **Transaction Volume by Hour** — Online orders are concentrated during business hours 
  (8AM–5PM) and peak at 12PM, consistent with the dataset description that many customers 
  are wholesalers placing orders during the workday rather than individual consumers 
  shopping at any hour. 

- **Monthly Revenue and Transaction Volume** — Both metrics follow the same seasonal 
  pattern, remaining relatively flat from December 2010 through August 2011 before 
  ramping up sharply in September. November 2011 peaks at over 60K transactions and 
  £1.1M in revenue, consistent with holiday gift buying. Note that December 2011 
  reflects partial data only — the dataset ends December 9, 2011.

### Cohort Analysis
- **Retention Pattern** — The December 2010 cohort is the largest with 884 customers 
  and shows the strongest retention across all subsequent months. Subsequent cohorts 
  range from 169 to 452 customers and generally retain between 15-36% of customers 
  month over month.
- **Seasonality in Retention** — A visible uptick appears in the final observation month 
  of each cohort, coinciding with the Q4 holiday period, suggesting seasonal re-engagement 
  by customers who may not purchase regularly.
- **Overall Customer Loyalty** — Retention hovers around 20-25% across most cohorts, 
  with the December 2010 cohort being a clear outlier at 38% average retention. This 
  is expected given the nature of the product catalog — unlike consumables or subscription 
  services, specialty gift and novelty items are purchased infrequently and often tied 
  to special occasions, making repeat monthly purchasing unlikely for most customers.

### RFM Segmentation
- **Customer Distribution** — The largest concentration of customers falls in the 
  mid-to-low RFM score range (3-6), characterized by low mean transactions, lower 
  revenue, and higher recency days indicating they have not purchased recently. These 
  customers represent the best opportunity for re-engagement marketing campaigns.
- **High-Value Customers** — A solid segment of customers score between 9-11, 
  representing loyal, high-frequency, high-spend buyers. Given the wholesale nature 
  of the business, these are likely retail businesses purchasing inventory regularly 
  rather than individual consumers.

### K-Means Clustering
Six clusters were identified as the optimal number of segments balancing statistical 
fit with business interpretability.

- **Clusters 0-2 (Re-engagement Targets)** — These segments have modest mean RFM 
  scores ranging from 3.6 to 6.4, characterized by low mean transactions and low mean 
  revenue. Cluster 2 stands out with better mean recency, suggesting these customers 
  purchased more recently than Clusters 0 and 1. All three are good candidates for 
  re-engagement and win-back campaigns.

- **Cluster 3 (Champions)** — The smallest segment with only 270 customers but the 
  highest mean RFM score of 10.9, highest mean transactions (22.7), and highest mean 
  revenue (£15,634). These are the VIP customers and best targets for retention 
  strategies and loyalty programs.

- **Clusters 4-5 (Loyal Mid-Tier)** — These segments have strong RFM scores (9.6 and 
  8.9 respectively) with good recency and moderate-to-high transaction frequency. 
  Although they do not spend as much as Cluster 3, they represent engaged customers 
  well suited for retention strategies, loyalty programs, and nurture campaigns aimed 
  at increasing their spend.

- **SHAP Analysis** — Recency was identified as the strongest overall driver of cluster 
  assignment, followed by frequency and monetary value. See the SHAP plots in 
  `outputs/figures/` for cluster-level breakdowns.

---

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

---

## Author

**Rocio Segura**
Data Analytics Professional | Healthcare Analytics Specialist

- 15+ years of experience in healthcare analytics 
- Caltech CTME Data Science Bootcamp — Capstone Project
- Stanford Statistics for AI/ML

[![GitHub](https://img.shields.io/badge/GitHub-DewDropRS-181717?style=flat&logo=github)](https://github.com/DewDropRS)

---

## References

- [Docker Python Guide](https://docs.docker.com/guides/python/)
- [Online Retail Dataset — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail) — Chen, D. (2015)
- [SHAP Documentation](https://shap.readthedocs.io/en/latest/)
- [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [Conventional Commits](https://www.conventionalcommits.org)
- [pytest Documentation](https://docs.pytest.org/en/stable/)