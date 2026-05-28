# ============================================================
# src/kmeans_model.py
# Performs K-Means clustering on RFM data to segment customers
# into distinct behavioral groups using log transformation,
# standardization, and elbow method for optimal k selection.
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist

from src.config import (

    # file directories
    MODEL_KMEANS_FILE,
    ELBOW_PLOT_FILE,
    CLUSTER_HEATMAP_FILE,
    CLUSTER_EXPORT_FILE,
    RFM_SCORES_LABELED_FILE,

    # model constants
    KMEANS_K_MIN,
    KMEANS_K_MAX,
    KMEANS_N_CLUSTERS,
    RANDOM_STATE,

    # constants for plots
    FIGURE_TITLE_FONTSIZE,
    SUBPLOT_TITLE_FONTSIZE,
    AXIS_LABEL_FONTSIZE,
    TICK_LABEL_FONTSIZE,
    ANNOTATION_FONTSIZE,
    FOOTNOTE_FONTSIZE

)
from src.logger import get_logger

logger = get_logger(__name__)


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the features needed for K-Means model using the dataframe containing RFM metrics and scores.
    Returns the log-transformed and scaled dataframe that will feed into model selection.
    :param df: RFM scores data (DataFrame)
    :return: Transformed and scaled data (DataFrame)
    """

    # Pipeline Steps:
    # Data Preparation
    # 1. Select RFM features — recency, frequency, monetary
    df = df[['recency', 'frequency', 'monetary']]
    # 2. Apply log transformation to handle skewness
    norm = np.log1p(df)
    # 3. Standardize the data using StandardScaler
    scaler = StandardScaler()
    norm_scaled = pd.DataFrame(scaler.fit_transform(norm), columns=df.columns, index=df.index)

    logger.info(f'[prepare_features] Feature preparation complete and normalized, scaled dataframe returned.')

    return norm_scaled


def compute_elbow_metrics(df: pd.DataFrame) -> tuple[list[float], list[float], list[float]]:
    """
    Takes the log-transformed and scaled data to generate distortion, wcss values, and silhouette scores
     as a tuple of lists to be used in the elbow plot, which will help determine the optimal number of clusters for
    the final K-Means model.
    :param df: log-transformed and standardized RFM feature matrix
    :return: tuple of three float lists — distortions, wcss (within-cluster sum of squares), and silhouette scores
    """
    # Model Selection
    # 4. Run elbow method — test k values from KMEANS_K_MIN to KMEANS_K_MAX, calculate inertia for each
    wcss = [] # within-cluster sum of squares (inertia)
    distortions = []
    silhouette_scores = []
    for k in range(KMEANS_K_MIN, KMEANS_K_MAX + 1):
        model = KMeans(
            n_clusters=k,
            init="k-means++",
            max_iter=300,
            n_init=10,
            random_state=RANDOM_STATE

        )
        model.fit(df)
        wcss.append(model.inertia_)
        # Calculate distortion: for each point find the squared distance to its nearest cluster center,
        # sum them all, then divide by the number of points to get the average (normalized inertia)
        distortions.append(
            sum(
                np.min(cdist(df, model.cluster_centers_, 'euclidean'), axis=1) ** 2
            ) / df.shape[0]
        )
        silhouette_scores.append(silhouette_score(df, model.labels_))

    logger.info(f'[compute_elbow_metrics] Distortion and wcss elbow metrics computed and returned.')

    return distortions, wcss, silhouette_scores


def plot_elbow_curve(distortions, wcss, silhouette_scores)-> None:
    """
    Plots the Elbow Curves for WCSS and Distortion and the Silhouette Scores to help determine the
    optimal k clusters to use for the final K-Means model.
    :param distortions:
    :param wcss:
    :param silhouette_scores:
    :return: None
    """

    # 5. Plot elbow curve — visualize inertia vs k to identify optimal number of clusters
    K_range = range(KMEANS_K_MIN, KMEANS_K_MAX + 1)
    df_inertia = pd.DataFrame({'Number of Clusters (k)': K_range, 'WCSS': wcss})
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(4, 12))
    fig.suptitle('K-Means Model Selection', fontsize=FIGURE_TITLE_FONTSIZE)
    sns.lineplot(
        data = df_inertia,
        x='Number of Clusters (k)',
        y='WCSS',
        marker='o',
        linewidth=2,
        ax=axes[0])
    sns.despine()
    axes[0].set_title('Elbow Curve - Within Cluster Sum of Squares (WCSS)', fontsize=SUBPLOT_TITLE_FONTSIZE)
    axes[0].yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x / 1000):,}K')
    )
    axes[0].axvline(x=6, color='red', linestyle='--', linewidth=1, label='Optimal k=6')
    axes[0].yaxis.grid(True, linestyle='--', alpha=0.7)

    df_distortions = pd.DataFrame({'Number of Clusters (k)': K_range, 'Distortions': distortions})
    sns.lineplot(
        data = df_distortions,
        x='Number of Clusters (k)',
        y='Distortions',
        marker='o',
        linewidth=2,
        ax=axes[1])
    sns.despine()
    axes[1].set_title('Elbow Curve - Distortions', fontsize=SUBPLOT_TITLE_FONTSIZE)
    axes[1].axvline(x=6, color='red', linestyle='--', linewidth=1, label='Optimal k=6')
    axes[1].yaxis.grid(True, linestyle='--', alpha=0.7)

    df_silhouette_scores = pd.DataFrame({'Number of Clusters (k)': K_range, 'Silhouette Scores': silhouette_scores})
    sns.lineplot(
        data = df_silhouette_scores,
        x='Number of Clusters (k)',
        y='Silhouette Scores',
        marker='o',
        linewidth=2,
        ax=axes[2])
    sns.despine()
    axes[2].set_title('Silhouette Scores', fontsize=SUBPLOT_TITLE_FONTSIZE)
    axes[2].yaxis.grid(True, linestyle='--', alpha=0.7)
    fig.text(0.5, -0.05,
             f"*The Silhouette Score plot does not show another peak after k=2.\nTwo customer segments is "
             f"too few for business needs.\nk=6 is selected based on the elbow curve inflection point.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')

    plt.tight_layout()
    plt.savefig(ELBOW_PLOT_FILE
                , dpi=150
                , bbox_inches='tight'  # prevents labels from getting cut off
                )
    plt.close()

    logger.info(f'[plot_elbow_curve] Elbow and Silhouette plots saved to {ELBOW_PLOT_FILE.name}.')

    # 6. Set KMEANS_N_CLUSTERS in config.py after reviewing the elbow plot


def train_final_model(norm_scaled: pd.DataFrame, rfm_scores: pd.DataFrame) -> tuple[ pd.DataFrame, pd.DataFrame]:
    """
    Trains the final K-Means model using the optimal k clusters determined from the elbow curve plots.
    Saves the final trained model and returns a dataframe containing the customer-level rfm scores
    and classification labels.
    :param norm_scaled: normalized and scaled rfm data (DataFrame)
    :param rfm_scores: customer-level rfm scores data (DataFrame)
    :return: tuple of (norm_scaled_labeled, rfm_scores_labeled)
    """
    kmeans_model = KMeans(
        n_clusters=KMEANS_N_CLUSTERS,
        init="k-means++",
        max_iter=300,
        n_init=10,
        random_state=RANDOM_STATE
    )
    kmeans_model.fit(norm_scaled)
    joblib.dump(kmeans_model, MODEL_KMEANS_FILE)
    logger.info(f'[train_final_model] K-Means model trained and saved to {MODEL_KMEANS_FILE.name}')

    # assign cluster labels back to dataframes
    # kmeans_model.labels_  is a numpy.ndarray
    norm_scaled_labeled = norm_scaled.assign(cluster=kmeans_model.labels_)
    rfm_scores_labeled = rfm_scores.assign(cluster=kmeans_model.labels_)

    rfm_scores_labeled.to_csv(RFM_SCORES_LABELED_FILE)

    logger.info(
        f'[train_final_model] Cluster distribution:\n{rfm_scores_labeled["cluster"].value_counts().sort_index().to_string()}')
    logger.info(f'[train_final_model] Final K-Means model trained and saved. Dataframes with cluster labels returned.')

    return norm_scaled_labeled, rfm_scores_labeled


def build_cluster_profile(rfm_scores_labeled: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a cluster profile dataframe containing customer count and rfm mean scores.
    :param rfm_scores_labeled: customer-level rfm scores with cluster labels (DataFrame)
    :return: aggregated means grouped by cluster (DataFrame)
    """

    rfm_cluster_profile = (rfm_scores_labeled.groupby(by='cluster', as_index=False)
        .agg(
            customer_count=('CustomerID', 'nunique'),
            recency_mean=('recency', 'mean'),
            frequency_mean=('frequency', 'mean'),
            monetary_mean=('monetary', 'mean'),
            rfm_score_mean=('rfm_score', 'mean')
            )
        .round({'recency_mean': 1, 'frequency_mean': 1, 'monetary_mean': 2, 'rfm_score_mean': 1})
    )

    rfm_cluster_profile.to_csv(CLUSTER_EXPORT_FILE, index=False)
    logger.info(
        f'[build_cluster_profile] Cluster profile built: {rfm_cluster_profile.shape[0]} clusters x {rfm_cluster_profile.shape[1]} columns')
    logger.info(f'[build_cluster_profile] Cluster profile saved to {CLUSTER_EXPORT_FILE.name}')

    return rfm_cluster_profile


def plot_cluster_profile_heatmap(rfm_cluster_profile: pd.DataFrame) -> None:
    """
    Plots a heatmap of the normalised metrics: customer_count, recency_mean, frequency_mean, monetary_mean, and
    rfm_score_mean.
    :param rfm_cluster_profile: RFM means by cluster (DataFrame)
    :return: None
    """
    cluster_t = rfm_cluster_profile.copy()
    cluster_t = cluster_t.set_index('cluster').T
    print(f"cluster_t:\n{cluster_t}")
    columns = ['customer_count', 'recency_mean', 'frequency_mean', 'monetary_mean', 'rfm_score_mean']

    # Normalization method: normalized = (value - min) / (max - min)
    cluster_normalized = rfm_cluster_profile.copy()
    cluster_normalized[columns] = (rfm_cluster_profile[columns] - rfm_cluster_profile[columns].min()) / (
                rfm_cluster_profile[columns].max() - rfm_cluster_profile[columns].min())
    # invert recency
    cluster_normalized['recency_mean'] = 1 - cluster_normalized['recency_mean']
    cluster_normalized = cluster_normalized.set_index('cluster')
    cluster_normalized.columns = ['Customer Count', 'Mean Recency (days)', 'Mean Transactions', 'Mean Revenue (£)', 'Mean RFM Score']
    cluster_normalized = cluster_normalized.T
    print(f"cluster_normalized:\n{cluster_normalized}")

    result = []
    for r in range(cluster_normalized.shape[0]):
        row = []  # start a new row list
        for c in range(cluster_normalized.shape[1]):
            val1 = cluster_normalized.iat[r, c].round(2)
            if r == 0:  # Customer Count row
                val2 = int(cluster_t.iat[r, c])
            elif r==3: # revenue
                val2 = cluster_t.iat[r, c].round(2)
            else:
                val2 = cluster_t.iat[r, c].round(1)

            row.append(f"{val1}\n({val2})")
        result.append(row)


    # Heatmap plot
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.suptitle("Customer Behavior by Cluster", fontsize=FIGURE_TITLE_FONTSIZE)
    sns.heatmap(data=cluster_normalized,
                ax=ax,
                annot=result,
                cmap='Blues',
                fmt='',
                annot_kws={'size': ANNOTATION_FONTSIZE}
                )
    sns.despine()
    ax.set_title('values: normalized (actual)', fontsize=SUBPLOT_TITLE_FONTSIZE)
    ax.set_xlabel('Cluster', fontsize=AXIS_LABEL_FONTSIZE)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=TICK_LABEL_FONTSIZE)
    plt.setp(ax.get_yticklabels(), rotation='horizontal', ha='right', fontsize=TICK_LABEL_FONTSIZE)
    fig.text(0.5, -0.05,
             f"Clusters 0–2 are candidates for re-engagement campaigns;\n"
             f"Clusters 3–5 are active customers suited for retention and upsell strategies.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')
    plt.tight_layout()
    plt.savefig(CLUSTER_HEATMAP_FILE
                , dpi=150
                , bbox_inches='tight'
                )
    plt.close()

    logger.info(f"[plot_cluster_profile_heatmap] The Customer Behavior by Cluster {CLUSTER_HEATMAP_FILE.name}.")


def run_kmeans(rfm_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Runs all K-Means steps: Prepares features, computes and plots elbow metrics, runs model with optimal k clusters,
    and plots the customer behavior by cluster.
    :param rfm_scores: rfm scores data (DataFrames)
    :return: rfm_scores_labeled (DataFrame)
    """

    logger.info("[run_kmeans] Starting K-Means model...")

    norm_scaled = prepare_features(rfm_scores)
    distortions, wcss, silhouette_scores = compute_elbow_metrics(norm_scaled)
    plot_elbow_curve(distortions, wcss, silhouette_scores)
    norm_scaled_labeled, rfm_scores_labeled = train_final_model(norm_scaled, rfm_scores)
    rfm_cluster_profile = build_cluster_profile(rfm_scores_labeled)
    plot_cluster_profile_heatmap(rfm_cluster_profile)

    logger.info("[run_kmeans] K-Means analysis complete. Model, figures, and exports saved.")

    return rfm_scores_labeled