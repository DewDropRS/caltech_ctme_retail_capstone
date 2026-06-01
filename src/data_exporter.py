# ============================================================
# src/data_exporter.py
# Generates a flat Tableau-ready csv file containing cleaned
# transaction data with RFM scores and cluster labels.
# ============================================================
import pandas as pd
from src.logger import get_logger
from src.config import VIZ_READY_DATA_FILE

logger = get_logger(__name__)


def export_viz_ready_data(df_cleaned: pd.DataFrame, rfm_scores_labeled: pd.DataFrame) -> None:
    """
    Merges cleaned transaction data with customer-level RFM scores and cluster labels
    and exports a Tableau-ready CSV file for dashboard analysis.
    :param df_cleaned: Cleaned data (DataFrame)
    :param rfm_scores_labeled: labeled rfm scores (DataFrame)
    :return: None
    """

    df_tab = pd.merge(df_cleaned, rfm_scores_labeled, how='left', on='CustomerID')
    df_tab.to_csv(VIZ_READY_DATA_FILE, index=False)

    logger.info(f'[export_tableau_ready_data] Tableau-ready CSV exported to {VIZ_READY_DATA_FILE.name}')
    logger.info(f'[export_tableau_ready_data] Export shape: {df_tab.shape[0]:,} rows x {df_tab.shape[1]} columns')
