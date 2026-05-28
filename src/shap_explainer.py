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
import xgboost as xgb

from src.config import(

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

def build_shap_explainer(rfm_scores_labeled: pd.DataFrame) -> shap.TreeExplainer:
    """
    Trains an XGBoost classifier on the RFM cluster labels and returns the SHAP Explainer object.
    :param rfm_scores_labeled:
    :return: shap.TreeExplainer
    """


    explainer = shap.TreeExplainer(model)