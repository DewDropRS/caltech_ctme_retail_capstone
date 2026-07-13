# ============================================================
# src/cohort_analysis.py
# Performs cohort analysis using a customer's first purchase date
# to track retention and spending behavior.
# ============================================================

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from src.logger import get_logger
from src.config import (
    RETENTION_HEATMAP_FILE,
    FIGURE_TITLE_FONTSIZE,
    TICK_LABEL_FONTSIZE,
    AXIS_LABEL_FONTSIZE,
    FOOTNOTE_FONTSIZE,
    COHORT_MATRIX_FILE
)
logger = get_logger(__name__)

def get_acquisition_cohorts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds the acquisition cohort matrix and returns a dataframe with one row per
    customer and their cohort month (year and month of their first purchase date).
    :param df: an analysis-ready cleaned dataframe
    :return df: acquisition cohort DataFrame (pd.DataFrame)
    """

    cohort_df = (df.groupby('CustomerID')['InvoiceDate']
                 .min()
                 .dt.to_period('M')
                 .reset_index()
                 .rename(columns={'InvoiceDate': 'cohort_month'}))

    logger.info(f"[get_acquisition_cohorts] {len(cohort_df)} unique customers assigned to cohorts.")
    logger.info(f"[get_acquisition_cohorts] Acquisition cohort dataframe has been created and returned.")

    return cohort_df


def build_cohort_matrix(cleaned_data: pd.DataFrame, acq_cohort: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a pivot table of unique active customers per cohort month (rows)
    and months since first purchase (columns).
    :param cleaned_data: cleaned retail dataframe
    :param acq_cohort:  acquisition cohort dataframe with CustomerID and cohort_month
    :return df: cohort matrix (pd.DataFrame)
    """

    merged = pd.merge(cleaned_data,acq_cohort, how='left', on='CustomerID')
    merged['cohort_index'] = (merged['InvoiceDate'].dt.to_period('M') - merged['cohort_month']).apply(lambda x: x.n)
    cohort_matrix = (merged.groupby(by=['cohort_month','cohort_index'])['CustomerID']
            .nunique()
            .reset_index(name='CustomerDistinctCount')
            .pivot(index='cohort_month', columns='cohort_index', values='CustomerDistinctCount')
            )

    logger.info(f"[build_cohort_matrix] Cohort matrix shape: {cohort_matrix.shape}")
    logger.info(f"[build_cohort_matrix] Cohort months range from {cohort_matrix.index.min()} to {cohort_matrix.index.max()}")
    logger.info(f"[build_cohort_matrix] Cohort matrix dataframe has been created and returned.")

    return cohort_matrix

def build_retention_matrix(cohort_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Builds the retention matrix that is a version of the cohort matrix but with
    row percentages replacing customer counts. Note: Cohort index zero contains the
    customer count at the baseline cohort month.
    :param cohort_matrix: the dataframe returned from build_cohort_matrix (DataFrame)
    :return: retention_matrix with row percentages replacing customer counts
    """

    totals_series = cohort_matrix[0]
    retention_matrix = (cohort_matrix.div(totals_series, axis=0) * 100).round(1)

    logger.info(
        f"[build_retention_matrix] Retention matrix created: {retention_matrix.shape[0]} cohorts x {retention_matrix.shape[1]} periods.")

    return retention_matrix


def plot_retention_heatmap(retention_matrix: pd.DataFrame) -> None:
    """
    Visualizes retention percentages using a heatmap plot.
    :param retention_matrix: the dataframe returned by build_retention_matrix (DataFrame)
    :return: None
    """

    retention_matrix.index = retention_matrix.index.astype(str)
    annotations = retention_matrix.map(lambda x: f'{x:.1f}%' if pd.notna(x) else '')
    # plot heatmap
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(data=retention_matrix,
                ax=ax,
                annot=annotations,
                cmap='Blues',
                fmt='',
                annot_kws={'size': 7},
                cbar_kws={
                    "label": 'Intensity',
                    "format": '%.0f%%'
                })
    sns.despine()
    ax.set_title('Cohort Analysis: Customer Retention Heatmap', fontsize=FIGURE_TITLE_FONTSIZE)
    ax.set_xlabel('Months Since First Purchase', fontsize=AXIS_LABEL_FONTSIZE)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=TICK_LABEL_FONTSIZE)
    ax.set_ylabel('Cohort Month', fontsize=AXIS_LABEL_FONTSIZE)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=TICK_LABEL_FONTSIZE)
    fig.text(0.5, -0.02,
             f"* Each cohort month's last observation reflects a partial month due to the dataset "
             f"ending December 9, 2011.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')
    plt.tight_layout()
    plt.savefig(RETENTION_HEATMAP_FILE
                , dpi=150
                , bbox_inches='tight'
                )
    plt.close()

    logger.info(f"[plot_retention_heatmap] Retention heatmap saved to {RETENTION_HEATMAP_FILE.name}")


def run_cohort_analysis(df: pd.DataFrame) -> None:
    """
    Runs all the cohort analysis steps such as building the cohort and retention matrices
    and plots the retention heatmap.
    :param df: cleaned dataframe that is returned from data cleaning step (DataFrame)
    :return: None
    """

    logger.info("[run_cohort_analysis] Starting Cohort analysis ...")

    acquisition_cohorts = get_acquisition_cohorts(df)
    cohort_matrix = build_cohort_matrix(df, acquisition_cohorts)
    retention_matrix = build_retention_matrix(cohort_matrix)

    # Drops the last incomplete cohort month prior to plotting heatmap
    # retention_matrix = retention_matrix.iloc[:-1]
    plot_retention_heatmap(retention_matrix)

    cohort_matrix.to_csv(COHORT_MATRIX_FILE)
    logger.info("[run_cohort_analysis] Cohort analysis complete.")
