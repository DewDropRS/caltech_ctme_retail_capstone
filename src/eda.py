# ============================================================
# src/eda.py
# Exploratory Data Analysis
# Explores the distribution, central tendency,
# and variability of the data. Creates visualizations to reveal
# patterns.
# ============================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.logger import get_logger
from src.config import (
    DESCRIPTIVE_STATS_FILE,
    DISTRIBUTION_PLOTS_FILE,
    BOXPLOTS_FILE,
    TOP_N_COUNTRIES,
    COUNTRY_BARPLOT_FILE,
    TOP_N_PRODUCTS,
    PRODUCT_QUANTITY_FILE,
    MONTHLY_REV_TXN_FILE,
    HOURLY_TXN_FILE,

    FIGURE_TITLE_FONTSIZE,
    SUBPLOT_TITLE_FONTSIZE,
    AXIS_LABEL_FONTSIZE,
    TICK_LABEL_FONTSIZE,
    ANNOTATION_FONTSIZE,
    FOOTNOTE_FONTSIZE,

)

logger = get_logger(__name__)


def descriptive_stats(df: pd.DataFrame) -> None:
    """
    Generates descriptive statistics for Quantity and UnitPrice.
    :param df: cleaned dataframe
    :return: None
    """

    stats = df[['Quantity', 'UnitPrice']].describe()
    stats.to_csv(DESCRIPTIVE_STATS_FILE, index=False)
    logger.info(f"Descriptive stats:\n{stats.to_string()}")
    logger.info(f"Descriptive statistics generated and saved to {DESCRIPTIVE_STATS_FILE.name}")


def plot_histograms(df: pd.DataFrame) -> None:
    """
    Plots histograms to examine the distribution of Quantity and UnitPrice.
    :param df: cleaned dataframe
    :return: None
    """

    fig, axes=plt.subplots(ncols=2,nrows=1,figsize=(10,5))

    sns.histplot(data=df, x='Quantity', ax=axes[0], bins=50, log_scale=True)
    sns.despine()
    axes[0].set_title("Quantity Distribution", fontsize=SUBPLOT_TITLE_FONTSIZE)
    axes[0].set_xlabel("Quantity", fontsize=AXIS_LABEL_FONTSIZE)
    axes[0].set_ylabel("Count", fontsize=AXIS_LABEL_FONTSIZE)
    axes[0].set_xlim(0.5, df['Quantity'].quantile(0.99))

    sns.histplot(data=df, x='UnitPrice', ax=axes[1], bins=20, log_scale=True)
    sns.despine()
    axes[1].set_title("UnitPrice Distribution", fontsize=SUBPLOT_TITLE_FONTSIZE)
    axes[1].set_xlabel("UnitPrice", fontsize=AXIS_LABEL_FONTSIZE)
    axes[1].set_ylabel("Count", fontsize=AXIS_LABEL_FONTSIZE)
    axes[1].set_xlim(0.01, df['UnitPrice'].quantile(0.99))

    fig.suptitle("Retail EDA: Quantity and Unit Price Distributions", fontsize=FIGURE_TITLE_FONTSIZE)
    fig.text(0.5, -0.02, "Note: Log scale applied due to right-skewed distribution.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')
    plt.tight_layout()
    plt.savefig(DISTRIBUTION_PLOTS_FILE
                , dpi=150
                , bbox_inches='tight'  # prevents labels from getting cut off
                )
    plt.close()
    logger.info(f"[plot_histograms] Distribution plots for Quantity and UnitPrice saved to {DISTRIBUTION_PLOTS_FILE.name}")


def plot_boxplots(df: pd.DataFrame) -> None:
    """
    Plots box and whisker plots for Quantity and UnitPrice to visualize data distributions
    and capture potential outliers.
    :param df: cleaned dataframe
    :return: None
    """
    # Outlier detection for Quantity
    # get Q1 for Quantity
    quantity_q1 = df['Quantity'].quantile(0.25)
    # get Q3 for Quantity
    quantity_q3 = df['Quantity'].quantile(0.75)
    # Calculate IQR (Interquartile Range)
    quantity_iqr = quantity_q3 - quantity_q1
    # Calculate the outliers for Quantity
    quantity_outliers_low =quantity_q1 - 1.5 * quantity_iqr
    quantity_outliers_high = quantity_q3 + 1.5 * quantity_iqr

    # Outlier detection for UnitPrice
    # get Q1 for UnitPrice
    unit_price_q1 = df['UnitPrice'].quantile(0.25)
    # get Q3 for UnitPrice
    unit_price_q3 = df['UnitPrice'].quantile(0.75)
    # Calculate IQR (Interquartile Range)
    unit_price_iqr = unit_price_q3 - unit_price_q1
    # Calculate the outliers for UnitPrice
    unit_price_outliers_low =unit_price_q1 - 1.5 * unit_price_iqr
    unit_price_outliers_high = unit_price_q3 + 1.5 * unit_price_iqr

    quantity_outlier_count = \
    df[(df['Quantity'] < quantity_outliers_low) | (df['Quantity'] > quantity_outliers_high)].shape[0]

    unit_price_outlier_count = \
    df[(df['UnitPrice'] < unit_price_outliers_low) | (df['UnitPrice'] > unit_price_outliers_high)].shape[0]

    # color the outliers
    flierprops = dict(marker='o', markerfacecolor='red', markersize=4, alpha=0.5)

    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(10, 5))
    fig.suptitle("Retail EDA: Quantity and Unit Price Box & Whisker Plots", fontsize=FIGURE_TITLE_FONTSIZE)
    sns.boxplot(data=df, y='Quantity', ax=axes[0], flierprops=flierprops)
    sns.despine()
    axes[0].set_xlabel(f"Outliers: {quantity_outlier_count:,} records", fontsize=AXIS_LABEL_FONTSIZE , style='italic')
    axes[0].yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x / 1000)}K')
    )
    sns.boxplot(data=df, y='UnitPrice', ax=axes[1], flierprops=flierprops)
    axes[1].set_xlabel(f"Outliers: {unit_price_outlier_count:,} records", fontsize=AXIS_LABEL_FONTSIZE , style='italic')
    axes[1].yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'£{x:.0f}')
    )
    fig.text(0.5, -0.02,
             f"Most quantities are below {quantity_q3} units (75th percentile), though a small number of "
             f"transactions contain extremely high quantities.\n"
             f" Similarly, unit prices are mostly below £{unit_price_q3} (75th percentile) with a few transactions "
             f"having unusually high unit prices.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')
    plt.tight_layout()
    plt.savefig(BOXPLOTS_FILE
                , dpi=150
                , bbox_inches='tight'  # prevents labels from getting cut off
                )
    plt.close()
    logger.info(
        f"[plot_boxplots] Quantity outliers detected: {quantity_outlier_count:,} "
        f"({((quantity_outlier_count)/df.shape[0]*100):.1f}%) records below {quantity_outliers_low:.1f} "
        f"or above {quantity_outliers_high:.1f}")
    logger.info(
        f"[plot_boxplots] UnitPrice outliers detected: {unit_price_outlier_count:,} "
        f"({((unit_price_outlier_count)/df.shape[0]*100):.1f}%) records below {unit_price_outliers_low:.2f} "
        f"or above {unit_price_outliers_high:.2f}")
    logger.info(f"[plot_boxplots] Outliers are retained since k-means log transformation will reduce their influence "
                f"on the clustering.")
    logger.info(f"[plot_boxplots] Boxplots saved to {BOXPLOTS_FILE.name}")


def plot_top_countries (df: pd.DataFrame)->None:
    """
    Visualizes the top 5 countries by transaction count as a horizontal barplot.
    :param df: cleaned dataframe
    :return: None
    """

    df_country_counts = (df.groupby(by='Country',sort=True).size().reset_index(name='Transactions').sort_values('Transactions', ascending=False))
    top = df_country_counts.head(TOP_N_COUNTRIES)
    other = df_country_counts.iloc[TOP_N_COUNTRIES:]['Transactions'].sum()
    barplot_df = pd.concat([
        top,
        pd.DataFrame({'Country': ['Other'], 'Transactions': [other]})
    ], ignore_index=True)
    total = barplot_df['Transactions'].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=barplot_df, x='Transactions', y='Country', ax=ax, orient='h')
    sns.despine()
    ax.set_xlabel('Transactions', fontsize=AXIS_LABEL_FONTSIZE)
    ax.set_ylabel('Country', fontsize=AXIS_LABEL_FONTSIZE)
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x / 1000)}K')
    )
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    for bar in ax.patches:
        ax.text(
            bar.get_width(),  # x position (value)
            bar.get_y() + bar.get_height() / 2,  # y position
            f'{int(bar.get_width())/total *100:.1f}%\n({int(bar.get_width()):,})',  # label text with comma formatting
            va='center',  # vertical alignment
            ha='left',  # horizontal alignment — start text at bar end
            fontsize=ANNOTATION_FONTSIZE
        )

    plt.title(f'Retail EDA: Top {TOP_N_COUNTRIES} countries by number of transactions', fontsize=FIGURE_TITLE_FONTSIZE)
    plt.tight_layout()
    plt.savefig(COUNTRY_BARPLOT_FILE
                , dpi=150
                , bbox_inches='tight'  # prevents labels from getting cut off
                )
    plt.close()

    logger.info(f"[plot_top_countries] Transactions by country plot saved to {COUNTRY_BARPLOT_FILE.name}")


def plot_top_products(df: pd.DataFrame) -> None:
    """
    Visualizes the most frequently purchased products as a horizontal barplot.
    :param df: cleaned dataframe
    :return: None
    """

    df_products_counts = (df.groupby(by='Description', sort=True)['Quantity']
                          .sum()
                          .reset_index(name='Total_Quantity')
                          .sort_values('Total_Quantity', ascending=False))

    top = df_products_counts.head(TOP_N_PRODUCTS)
    other = df_products_counts.iloc[TOP_N_PRODUCTS:]['Total_Quantity'].sum()
    barplot_df = pd.concat([
        top,
        pd.DataFrame({'Description': ['Other'], 'Total_Quantity': [other]})
    ], ignore_index=True)
    total = barplot_df['Total_Quantity'].sum()
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 20))
    sns.barplot(data=barplot_df, x='Total_Quantity', y='Description', ax=ax, orient='h')
    sns.despine()
    ax.set_xlabel('Units Sold', fontsize=AXIS_LABEL_FONTSIZE)
    ax.set_ylabel('Product', fontsize=AXIS_LABEL_FONTSIZE)
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x / 1000)}K')
    )
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    for bar in ax.patches:
        ax.text(
            bar.get_width(),  # x position (value)
            bar.get_y() + bar.get_height() / 2,  # y position
            f'{int(bar.get_width())/total *100:.1f}%\n({int(bar.get_width()):,})',  # label text with comma formatting
            va='center',  # vertical alignment
            ha='left',  # horizontal alignment — start text at bar end
            fontsize=ANNOTATION_FONTSIZE
        )

    ax.set_title(f'Retail EDA: Top {TOP_N_PRODUCTS} most purchased products', fontsize=FIGURE_TITLE_FONTSIZE)
    plt.tight_layout()
    plt.savefig(PRODUCT_QUANTITY_FILE
                , dpi=150
                , bbox_inches='tight'  # prevents labels from getting cut off
                )
    plt.close()

    top20_pct = top['Total_Quantity'].sum() / df_products_counts['Total_Quantity'].sum() * 100
    logger.info(
        f"[plot_top_products] Top {TOP_N_PRODUCTS} products account for {top20_pct:.1f}% of total quantity sold — "
        f"purchases are widely distributed across products.")
    logger.info(f"[plot_top_products] Top {TOP_N_PRODUCTS} products purchased by quantity saved to {PRODUCT_QUANTITY_FILE.name}")


def plot_rev_txn_over_time(df: pd.DataFrame) -> None:
    """
    Visualizes total monthly revenue per month.
    :param df: cleaned dataframe
    :return: None
    """

    df['year_month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df_month_revenue = df.groupby(by='year_month',sort=True).agg({'Revenue': 'sum'}).reset_index()
    df_month_transactions = df.groupby(by='year_month',sort=True).size().reset_index(name='Transactions')

    fig, ax1 = plt.subplots(figsize=(10, 8))

    sns.lineplot(x='year_month', y='Revenue',
                 data=df_month_revenue,
                 ax=ax1,
                 linewidth=2,
                 color='#2E75B6',
                 marker='o',
                 label='Revenue'
                 )
    sns.despine()
    ax1.set_title('Retail EDA: Monthly Revenue and Transaction Volume', fontsize=FIGURE_TITLE_FONTSIZE)
    ax1.set_xlabel('Month', fontsize=AXIS_LABEL_FONTSIZE)
    ax1.set_ylabel('Revenue', fontsize=AXIS_LABEL_FONTSIZE)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax1.set_axisbelow(True)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=TICK_LABEL_FONTSIZE)
    ax1.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'£{int(x / 1000):,}K')
    )
    #second y-axis
    ax2 = ax1.twinx()
    sns.lineplot(x='year_month', y='Transactions',
                 data=df_month_transactions,
                 ax=ax2,
                 linewidth=2,
                 color='#E07B39',
                 marker='o',
                 label='Transactions'
                 )
    sns.despine()
    ax2.set_ylabel('Transactions', fontsize=AXIS_LABEL_FONTSIZE)
    ax2.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x / 1000):,}K')
    )
    # legend
    ax1.get_legend().remove()
    ax2.get_legend().remove()
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=ANNOTATION_FONTSIZE)

    fig.text(0.5, -0.02,
             f"Revenue and Transactions began to surge in September of 2011, coinciding with holiday gift buying.\n"
             f"December 2011 reflects partial data only; the dataset ends on {df['InvoiceDate'].max().strftime('%B %d, %Y')}.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')
    plt.tight_layout()
    plt.savefig(MONTHLY_REV_TXN_FILE
                , dpi=150
                , bbox_inches='tight'  # prevents labels from getting cut off
                )
    plt.close()
    logger.info(f"[plot_rev_txn_over_time] Revenue and transaction volume by month plot saved to {MONTHLY_REV_TXN_FILE.name}")


def plot_orders_by_hour(df: pd.DataFrame) -> None:
    """
    Visualizes transaction volume by hour of the day.
    :param df: cleaned dataframe
    :return: None
    """

    # Extract hour (0–23)
    df['hour'] = df['InvoiceDate'].dt.hour
    # Create a label column for plotting (12AM, 1AM, ..., 11PM)
    df['hour_label'] = df['hour'].apply(lambda h: f"{h % 12 or 12}{'AM' if h < 12 else 'PM'}")

    df_hourly_transactions = (df.groupby(by=['hour', 'hour_label'], sort=True)
                              .size()
                              .reset_index(name='Transactions'))
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(data=df_hourly_transactions, x='hour', y='Transactions', ax=ax, orient='v')
    sns.despine()
    ax.set_xlabel('Hour', fontsize=AXIS_LABEL_FONTSIZE)
    ax.set_xticks(range(len(df_hourly_transactions)))
    ax.set_xticklabels(df_hourly_transactions['hour_label'], rotation=45, ha='right', fontsize=TICK_LABEL_FONTSIZE)
    ax.set_ylabel('Transactions', fontsize=AXIS_LABEL_FONTSIZE)
    ax.set_title('Retail EDA: Hourly Transaction Volume')
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x / 1000):,}K')
    )
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    plt.subplots_adjust(bottom=0.1)
    fig.text(0.5, -0.05,
             f"Online orders placed by wholesalers are concentrated\nduring business hours (8AM–5PM), peaking at 12PM.",
             ha='center', fontsize=FOOTNOTE_FONTSIZE, style='italic')
    plt.tight_layout()
    plt.savefig(HOURLY_TXN_FILE
                , dpi=150
                , bbox_inches='tight'  # prevents labels from getting cut off
                )
    plt.close()

    logger.info(f"[plot_orders_by_hour] Orders placed during business hours (8AM-5PM) and peak at 12PM.")
    logger.info(f"[plot_orders_by_hour] Hourly transaction volume plot saved to {HOURLY_TXN_FILE.name}")


def perform_eda(df: pd.DataFrame) -> None:
    """
    Runs all exploratory data analysis steps and saves all visualizations.
    :param df: cleaned dataframe (DataFrame)
    :return: None
    """
    logger.info("[perform_eda] Starting exploratory data analysis...")

    descriptive_stats(df)
    plot_histograms(df)
    plot_boxplots(df)
    plot_top_countries(df)
    plot_top_products(df)
    plot_rev_txn_over_time(df)
    plot_orders_by_hour(df)

    logger.info("[perform_eda] EDA complete. All figures saved to outputs/figures/")

