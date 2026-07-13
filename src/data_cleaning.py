# ============================================================
# src/data_cleaning.py
# Checks for missingness, duplicates, invalid values, and determines
# if any records should be excluded from analysis.
# ============================================================
import pandas as pd
from src.logger import get_logger
from src.config import(
    CANCELLATION_PREFIX,
    MIN_QUANTITY,
    MIN_UNIT_PRICE,
)

logger = get_logger(__name__)

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe as input and removes duplicates.
    :param df: input dataframe
    :return df: cleaned dataframe with duplicates removed
    """

    before = df.shape[0]
    # Remove duplicate rows — keep first occurrence, drop all subsequent copies.
    df = df.drop_duplicates()
    after = df.shape[0]
    logger.info(f"[remove_duplicates] Removed {before - after} duplicate rows.")

    return df

def remove_missing_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes records whose CustomerIDs are null.
    :param df: input dataframe
    :return df: cleaned dataframe with null CustomerID rows removed
    """

    # Drop records that have null as CustomerID
    before = df.shape[0]
    df = df.dropna(subset=['CustomerID'])
    after = df.shape[0]
    logger.info(f"[remove_missing_customers] Removed {before - after} rows that had missing CustomerID.")

    return df

def remove_cancellations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes cancelled orders from the dataframe.
    :param df: input dataframe
    :return: cleaned dataframe with cancelled orders removed
    """

    before = df.shape[0]
    # Invoice numbers that begin with 'C' represent cancelled orders
    # Drop canceled order records
    df = df[~df['InvoiceNo'].str.startswith(CANCELLATION_PREFIX, na=False)]
    after = df.shape[0]
    logger.info(f"[remove_cancellations] Removed {before - after} cancelled orders.")

    return df

def remove_invalid_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes invalid values that don't meet the minimum quantity and minimum unit price values.
    :param df: input dataframe
    :return: cleaned dataframe with invalid values removed
    """

    before = df.shape[0]
    df = df[(df['Quantity'] >= MIN_QUANTITY) & (df['UnitPrice'] >= MIN_UNIT_PRICE)]
    after = df.shape[0]
    logger.info(f"[remove_invalid_values] Removed {before - after} orders whose Quantity or UnitPrice do not meet the minimum requirements.")

    return df

def remove_non_product_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes non-product records that do not contribute to the RFM model.
    :param df: input dataframe
    :return: cleaned dataframe with invalid values removed
    """

    # keep only rows where StockCode starts with a digit AND UnitPrice is above MIN_UNIT_PRICE.
    before = df.shape[0]
    # Filter StockCode using regex pattern match for values that begin with a digit (^\d)
    df = df[df['StockCode'].astype(str).str.match(r'^\d') & (df['UnitPrice'] >= MIN_UNIT_PRICE)]
    after = df.shape[0]
    logger.info(f"[remove_non_product_records] Removed {before - after} non-product orders.")

    return df

def add_revenue_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds the calculated revenue column needed for RFM monetary value and EDA.
    :param df: a dataframe
    :return df: a dataframe with added revenue column (pd.Dataframe)
    """
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    logger.info(f"[add_revenue_column] Revenue column has been added.")

    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs all data cleaning steps: removes cancellations, invalid values,
    non-product records, missing customers, duplicates, and adds the revenue column.
    :param df: loaded dataframe (DataFrame)
    :return df: analysis ready dataframe (DataFrame)
    """

    logger.info(f"[clean_data] Starting data cleaning: {df.shape[0]:,} rows x {df.shape[1]} columns")

    # keep this order
    df = remove_cancellations(df)
    df = remove_invalid_values(df)
    df = remove_missing_customers(df)
    df = remove_duplicates(df)
    df = remove_non_product_records(df)
    df = add_revenue_column(df)

    logger.info(f"[clean_data] Final cleaned dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
    logger.info("[clean_data] Data cleaning complete.")

    return df