# ============================================================
# src/shap_explainer.py
# Uses SHAP (SHapley Additive exPlanations) to explain which
# RFM features drive K-Means cluster assignments. A XGBoost
# classifier is trained on the cluster labels to enable
# SHAP feature importance analysis.
# ============================================================
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import shap
from xgboost import XGBClassifier

from src.config import (
    RANDOM_STATE,
    FIGURE_TITLE_FONTSIZE,
    KMEANS_N_CLUSTERS,
    FIGURES_DIR,
    SHAP_BAR_FILE
)

from src.logger import get_logger

logger = get_logger(__name__)


def build_shap_explainer(rfm_scores_labeled: pd.DataFrame) -> tuple[shap.TreeExplainer, pd.DataFrame]:
    """
    Trains an XGBoost classifier on the RFM cluster labels and returns the SHAP Explainer object.
    :param rfm_scores_labeled: labeled recency, frequency, and monetary metrics (DataFrame)
    :return: shap.TreeExplainer (SHAP object), X features (DataFrame)
    """

    X = rfm_scores_labeled[['recency', 'frequency', 'monetary']]
    y = rfm_scores_labeled['cluster']

    xgb_model = XGBClassifier(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5, 
        random_state=RANDOM_STATE
    )

    # Train the model
    xgb_model.fit(X, y)

    explainer = shap.TreeExplainer(xgb_model)

    logger.info('[build_shap_explainer] XGB Classifier trained and SHAP TreeExplainer built')

    return explainer, X


def compute_shap_values(explainer: shap.TreeExplainer, X: pd.DataFrame) ->  list[np.ndarray]:
    """
    Computes the SHAP values - one value per feature per customer per cluster.
    :param explainer: SHAP TreeExplainer built from the trained XGBoost classifier
    :param X: customer-level rfm metrics (DataFrame)
    :return shap_values: SHAP values List[np.ndarray]
    """

    shap_values = explainer.shap_values(X)
    logger.info(f'[compute_shap_values] SHAP values computed and returned.')

    return shap_values


def plot_shap_summary(shap_values: list[np.ndarray], X: pd.DataFrame) -> None:
    """
    Visualizes the SHAP values based on the XGBoost classifier as a beeswarm plot to better understand
    how each RFM feature contributes to the K-Means classification assignment.
    :param shap_values: SHAP values (List)
    :param X: customer-level rfm metrics (DataFrame)
    :return: None
    """

    for i in range(KMEANS_N_CLUSTERS):
        shap.summary_plot(shap_values[:, :, i], X, show=False)
        plt.title(f'SHAP Values — K-Means Cluster {i}', fontsize=FIGURE_TITLE_FONTSIZE)
        plt.savefig(FIGURES_DIR / f'shap_summary_beeswarm_{i}.png', dpi=150, bbox_inches='tight')
        plt.close()

    logger.info(f'[plot_shap_summary] SHAP summary values for each cluster visualized and saved to shap_summary_cluster_[n].png.')


def plot_shap_bar(shap_values: list[np.ndarray], X: pd.DataFrame) -> None:
    """
    Visualizes the average SHAP values across clusters in a bar chart to show overall feature importance.
    :param shap_values: SHAP values (List)
    :param X: customer-level RFM metrics (DataFrame)
    :return: None
    """

    shap.summary_plot(shap_values, X, plot_type='bar', show=False)

    # gcf() - get current figure, used to resize after SHAP renders it
    plt.gcf().set_size_inches(10, 4)
    plt.title('Mean Absolute SHAP Values by Feature and K-Means Cluster', fontsize=FIGURE_TITLE_FONTSIZE)
    plt.savefig(SHAP_BAR_FILE, dpi=150, bbox_inches='tight')
    plt.close()

    logger.info(f'[plot_shap_bar] Mean absolute SHAP values by feature and cluster visualized '
                f'in a bar chart and saved to {SHAP_BAR_FILE.name}')


def run_shap_explainer(rfm_scores_labeled: pd.DataFrame) -> None:
    """
    Runs all SHAP Explainer steps.
    :param rfm_scores_labeled: labeled RFM scores (DataFrame)
    :return: None
    """

    logger.info("[run_shap_explainer] Starting SHAP explainer analysis...")

    explainer, X = build_shap_explainer(rfm_scores_labeled)
    shap_values = compute_shap_values(explainer, X)
    plot_shap_summary(shap_values, X)
    plot_shap_bar(shap_values, X)

    logger.info("[run_shap_explainer] SHAP explainer analysis complete.")
