# ============================================================
# config.py
# Central configuration for the retail capstone pipeline.
# All constants, file paths, and model settings live here.
# Nothing is hardcoded in the individual modules — they import from here.
# ============================================================

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_FILE = DATA_RAW_DIR / "online_retail.xlsx"

FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
DATA_DIR = PROJECT_ROOT / "outputs" / "data"
MODELS_DIR = PROJECT_ROOT / "outputs" / "models"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# Data Cleaning
CANCELLATION_PREFIX = "C"

MIN_QUANTITY = 1
MIN_UNIT_PRICE = 0.0

# EDA Outputs
DESCRIPTIVE_STATS_FILE = REPORTS_DIR / "eda_descriptive_stats.csv"
DISTRIBUTION_PLOTS_FILE = FIGURES_DIR / "eda_distribution_plots.png"
BOXPLOTS_FILE = FIGURES_DIR / "eda_boxplots.png"

TOP_N_COUNTRIES = 5
COUNTRY_BARPLOT_FILE = FIGURES_DIR / "eda_country_barplot.png"

TOP_N_PRODUCTS = 20
PRODUCT_QUANTITY_FILE = FIGURES_DIR / "eda_product_quantity.png"

MONTHLY_REV_TXN_FILE = FIGURES_DIR / "eda_monthly_revenue_transactions.png"
HOURLY_TXN_FILE = FIGURES_DIR / "eda_hourly_transactions.png"

# Cohort Analysis
COHORT_DATE_FORMAT = "%Y-%m"
RETENTION_HEATMAP_FILE = FIGURES_DIR / "cohort_analysis_retention_heatmap.png"

# RFM Model
RFM_REFERENCE_DATE = "2011-12-10"
RFM_QUARTILES = 4
CATEGORICAL_COLS = ['r_score', 'f_score', 'm_score', 'rfm_score']
# Dictionary mapping column names to descriptive axis labels with units
COLUMN_LABELS = {
    'r_score': 'Recency Score',
    'f_score': 'Frequency Score',
    'm_score': 'Monetary Score',
    'rfm_score': 'RFM Score',
}
RFM_HISTOGRAMS_FILE = FIGURES_DIR / "rfm_scores_histograms.png"
RFM_HEATMAP_FILE = FIGURES_DIR / "rfm_scores_heatmap.png"
RFM_SCORE_EXPORT_FILE = DATA_DIR / "rfm_score.csv"
RFM_SCORE_SUMMARIZED_EXPORT_FILE = REPORTS_DIR / "rfm_score_summarized.csv"
# After running K-Means, cluster labels are added to rfm scores data
RFM_SCORES_LABELED_FILE = DATA_DIR / "rfm_scores_labeled.csv"

# K-Means Clustering
KMEANS_K_MIN = 2
KMEANS_K_MAX = 11
KMEANS_N_CLUSTERS = 6
RANDOM_STATE = 42

# Saved Models
MODEL_KMEANS_FILE = MODELS_DIR / 'kmeans_model.joblib'
ELBOW_PLOT_FILE = FIGURES_DIR / 'kmeans_elbow_plot.png'
CLUSTER_HEATMAP_FILE = FIGURES_DIR / 'kmeans_heatmap.png'
CLUSTER_EXPORT_FILE = REPORTS_DIR / 'kmeans_cluster_profile.csv'

# SHAP
SHAP_BAR_FILE = FIGURES_DIR / 'shap_summary_bar.png'

# Data Export
VIZ_READY_DATA_FILE = DATA_DIR / 'viz_ready_data.csv'

# Logging
LOG_DIR = PROJECT_ROOT / "outputs"
LOG_FILE = LOG_DIR / "pipeline.log"
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3

# Visualization Settings
FIGURE_TITLE_FONTSIZE = 14
SUBPLOT_TITLE_FONTSIZE = 11
AXIS_LABEL_FONTSIZE = 10
TICK_LABEL_FONTSIZE = 9
ANNOTATION_FONTSIZE = 9
FOOTNOTE_FONTSIZE = 9

# Creates output directories if they don't already exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)