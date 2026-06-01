# ============================================================
# src/rfm_model.py
# Generates the Recency, Frequency, Monetary (RFM) model.
# ============================================================

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from src.config import(
    RFM_REFERENCE_DATE,
    RFM_QUARTILES,
    CATEGORICAL_COLS,
    COLUMN_LABELS,
    RFM_HISTOGRAMS_FILE,
    RFM_HEATMAP_FILE,
    RFM_SCORE_EXPORT_FILE,
    RFM_SCORE_SUMMARIZED_EXPORT_FILE,

    RETENTION_HEATMAP_FILE,
    FIGURE_TITLE_FONTSIZE,
    SUBPLOT_TITLE_FONTSIZE,
    TICK_LABEL_FONTSIZE,
    AXIS_LABEL_FONTSIZE,
    FOOTNOTE_FONTSIZE
)
from src.logger import get_logger

logger = get_logger(__name__)

def build_rfm_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds the customer-level rfm metrics dataframe required to calculate rfm metrics.
    :param df: an analysis-ready cleaned dataframe
    :return df: a dataframe with added recency, frequency, and monetary metrics
    """

    rfm_df = (df
            .groupby('CustomerID', as_index=False)
            .agg(
                frequency = ('InvoiceNo', 'nunique'),
                latest_purchase_date = ('InvoiceDate', 'max'),
                monetary = ('Revenue', 'sum')
                )
            .assign(
                recency=lambda x:
                (pd.Timestamp(RFM_REFERENCE_DATE) - x['latest_purchase_date']).dt.days
                )
            .drop(columns='latest_purchase_date')
            )

    logger.info(f"[build_rfm_metrics] RFM dataframe created: {rfm_df.shape[0]} customers.")

    return rfm_df


def build_rfm_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the RFM scoring columns and returns the customer-level dataframe.
    :param df: the dataframe returned from build_rfm_metrics
    :return: a dataframe with added rfm scores
    """

    score_df = (
        df
        .assign(
            # inverted scoring for recency because low number of days since last purchase date are better
            # and should be scored higher
            r_score=lambda x: RFM_QUARTILES - pd.qcut(x['recency'], q=RFM_QUARTILES, labels=False, duplicates='drop'),
            f_score=lambda x: pd.qcut(x['frequency'], q=RFM_QUARTILES, labels=False, duplicates='drop') + 1,
            m_score=lambda x: pd.qcut(x['monetary'], q=RFM_QUARTILES, labels=False, duplicates='drop') + 1
        )
    )
    score_df['rfm_segment'] = score_df['r_score'].astype(str) + score_df['f_score'].astype(str) + score_df['m_score'].astype(str)
    score_df['rfm_score'] = score_df['r_score'] + score_df['f_score'] + score_df['m_score']

    logger.info(f"[build_rfm_scores] RFM scores calculated and added to dataframe.")

    return score_df

def plot_rfm_scores(df: pd.DataFrame) -> None:
    """
    Plots histograms for recency, frequency, monetary, and rfm combined score.
    :param df: dataframe output from build_rfm_scores
    :return: None
    """
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    # flatten axes array into a 1D list.
    axes = axes.flatten()
    # loop over all columns in the dataframe and plot a histogram for each

    for i, col in enumerate(CATEGORICAL_COLS):
        temp_df = df[[col]].copy()
        temp_df[col] = temp_df[col].astype(str)
        order = sorted(temp_df[col].unique(), key=lambda x: int(x))
        sns.countplot(
            x=col,
            data=temp_df,
            ax=axes[i],
            order=order,
            color='#2E75B6'
        )

        axes[i].set_title(f'Distribution of {COLUMN_LABELS.get(col, col)}', fontsize=SUBPLOT_TITLE_FONTSIZE )
        axes[i].set_xlabel(COLUMN_LABELS.get(col, col), fontsize=AXIS_LABEL_FONTSIZE)
        axes[i].set_ylabel('Count', fontsize=AXIS_LABEL_FONTSIZE)

    fig.suptitle('Distributions of RFM Scores', fontsize=FIGURE_TITLE_FONTSIZE)
    sns.despine()
    plt.tight_layout()
    plt.savefig(RFM_HISTOGRAMS_FILE, dpi=150, bbox_inches='tight')
    plt.close()

    logger.info(f"[plot_rfm_scores] Distribution plots for RFM scores saved to {RFM_HISTOGRAMS_FILE.name}.")


def summarize_rfm_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds the summary dataframe by RFM Score for number of customers, mean transactions, mean revenue,
    and mean recency.
    :param df: dataframe output from build_rfm_scores
    :return df: summary dataframe by rfm combined score
    """

    agg_df = (df
            .groupby('rfm_score', as_index=False)
            .agg(
                customer_count = ('CustomerID', 'nunique'),
                mean_transactions = ('frequency', 'mean'),
                mean_revenue = ('monetary', 'mean'),
                mean_recency=('recency', 'mean')
                )
              .round({'mean_transactions': 1, 'mean_revenue': 2, 'mean_recency': 1})
            )

    logger.info(f"[summarize_rfm_scores] RFM segment summary dataframe created.")

    return agg_df


def plot_rfm_heatmap(df: pd.DataFrame) -> None:
    """
    Plots a heatmap of the normalised metrics: customer_count, mean_transactions, mean_revenue, and mean recency
    :param df: returned datafrome from summarize_rfm_scores
    :return: None
    """

    rfm_t = df.copy()
    rfm_t = rfm_t.set_index('rfm_score').T

    columns = ['customer_count', 'mean_transactions', 'mean_revenue', 'mean_recency']

    # Normalization method: normalized = (value - min) / (max - min)
    rfm_normalized = df.copy()
    rfm_normalized[columns] = (df[columns] - df[columns].min()) / (
                df[columns].max() - df[columns].min())
    # invert recency
    rfm_normalized['mean_recency'] = 1 - rfm_normalized['mean_recency']
    rfm_normalized = rfm_normalized.set_index('rfm_score')
    rfm_normalized.columns = ['Customer Count', 'Mean Transactions', 'Mean Revenue (£)', 'Mean Recency (days)']
    rfm_normalized = rfm_normalized.T

    result = []
    for r in range(rfm_normalized.shape[0]):
        row = []  # start a new row list
        for c in range(rfm_normalized.shape[1]):
            val1 = rfm_normalized.iat[r, c].round(2)
            if r == 0:  # Customer Count row
                val2 = int(rfm_t.iat[r, c])
            elif r==2:
                val2 = rfm_t.iat[r, c].round(2)
            else:
                val2 = rfm_t.iat[r, c].round(1)

            row.append(f"{val1}\n({val2})")
        result.append(row)

    # Heatmap plot
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.suptitle("Customer Behavior by RFM Score", fontsize=FIGURE_TITLE_FONTSIZE)
    sns.heatmap(data=rfm_normalized,
                ax=ax,
                annot=result,
                cmap='Blues',
                fmt='',
                annot_kws={'size': 7}
                )
    sns.despine()
    ax.set_title('values: normalized (actual)', fontsize=SUBPLOT_TITLE_FONTSIZE)
    ax.set_xlabel('RFM Score', fontsize=AXIS_LABEL_FONTSIZE)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=TICK_LABEL_FONTSIZE)
    plt.setp(ax.get_yticklabels(), rotation='horizontal', ha='right', fontsize=TICK_LABEL_FONTSIZE)
    fig.text(0.5, -0.05,
             f"*Mean transactions, revenue, and recency improve consistently as RFM score increases, validating the scoring model.\n"
             f"*Customers scoring 4-6 represent the largest segment and are prime targets for marketing engagement.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')
    plt.tight_layout()
    plt.savefig(RFM_HEATMAP_FILE
                , dpi=150
                , bbox_inches='tight'
                )
    plt.close()

    logger.info(f"[plot_rfm_heatmap] The Customer Behavior by RFM Score heatmap has been saved to {RFM_HEATMAP_FILE.name}.")


def run_rfm_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs all the rfm analysis steps from building the rfm pipeline to plotting histograms and heatmap.
    :param df: an analysis-ready cleaned dataframe
    :return df: a customer-level DataFrame with one row per customer containing RFM metrics and scores
    """

    logger.info("[run_rfm_analysis] Starting RFM analysis...")

    rfm_metrics_df = build_rfm_metrics(df)
    rfm_scores_df = build_rfm_scores(rfm_metrics_df)
    plot_rfm_scores(rfm_scores_df)
    rfm_summarized_df = summarize_rfm_scores(rfm_scores_df)
    plot_rfm_heatmap(rfm_summarized_df)

    rfm_scores_df.to_csv(RFM_SCORE_EXPORT_FILE, index=False)
    rfm_summarized_df.to_csv(RFM_SCORE_SUMMARIZED_EXPORT_FILE, index=False)

    logger.info(f"[run_rfm_analysis] RFM scores saved to {RFM_SCORE_EXPORT_FILE.name}")
    logger.info(f"[run_rfm_analysis] RFM summary saved to {RFM_SCORE_SUMMARIZED_EXPORT_FILE.name}")
    logger.info("[run_rfm_analysis] RFM model complete.")

    return rfm_scores_df