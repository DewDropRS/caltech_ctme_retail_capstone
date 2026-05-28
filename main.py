import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.eda import perform_eda
from src.cohort_analysis import run_cohort_analysis
from src.rfm_model import run_rfm_analysis
from src.kmeans_model import run_kmeans
from src.config import DATA_FILE
from src.logger import get_logger

logger = get_logger(__name__)


def main():
    """
    Executes the pipeline from data loading to model evaluation
    """

    # Step 1: Load the raw data
    df = load_data(DATA_FILE)

    # Step 2: Perform data cleaning
    df = clean_data(df)

    # Step 3: Exploratory Data Analysis on cleaned data
    # perform_eda(df)

    # Step 4: Cohort Analysis
    #run_cohort_analysis(df)

    # Step 5: Recency, Frequency, Monetary (RFM) Model
    rfm_scores = run_rfm_analysis(df)

    # Step 6: K-Means
    run_kmeans(rfm_scores)


if __name__ == "__main__":
    main()