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
import xgboost as xgb

from src.config import(

    RANDOM_STATE,   
    FIGURE_TITLE_FONTSIZE,
    SUBPLOT_TITLE_FONTSIZE,
    AXIS_LABEL_FONTSIZE,
    TICK_LABEL_FONTSIZE,
    ANNOTATION_FONTSIZE,
    FOOTNOTE_FONTSIZE
)

from src.logger import get_logger

logger = get_logger(__name__)

# shap.Explainer, shap.summary_plot, shap.plots.bar

def build_shap_explainer(rfm_scores_labeled: pd.DataFrame) -> tuple[shap.TreeExplainer, pd.DataFrame]:
    """
    Trains an XGBoost classifier on the RFM cluster labels and returns the SHAP Explainer object.
    :param rfm_scores_labeled: labeled recency, frequency, monetary metrics and scores (DataFrame)
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

    