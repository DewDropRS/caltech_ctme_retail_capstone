import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.eda import perform_eda
from src.cohort_analysis import run_cohort_analysis
from src.rfm_model import run_rfm_analysis
from src.kmeans_model import run_kmeans
from src.shap_explainer import run_shap_explainer
from src.config import DATA_FILE
from src.logger import get_logger
from src.data_exporter import export_viz_ready_data

logger = get_logger(__name__)


def main():
    """
    Executes the pipeline from data loading to model evaluation
    """

    logger.info("[main] Starting retail analytics pipeline...")

    # Step 1: Load the raw data
    df = load_data(DATA_FILE)

    # Step 2: Perform data cleaning
    df_clean = clean_data(df)

    # Step 3: Exploratory Data Analysis on cleaned data
    perform_eda(df_clean)

    # Step 4: Cohort Analysis
    run_cohort_analysis(df_clean)

    # Step 5: Recency, Frequency, Monetary (RFM) Model
    rfm_scores = run_rfm_analysis(df_clean)

    # Step 6: K-Means
    rfm_scores_labeled = run_kmeans(rfm_scores)

    # Step 7: SHAP Explainer
    run_shap_explainer(rfm_scores_labeled)

    # Step 8: Data Exporter
    export_viz_ready_data(df_clean, rfm_scores_labeled)

    logger.info("[main] Pipeline complete.")

if __name__ == "__main__":
    main()