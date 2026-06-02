import pytest
import pandas as pd

from src.data_cleaning import(
    remove_duplicates,
    remove_missing_customers,
    remove_cancellations,
    remove_invalid_values,
    remove_non_product_records
)

from src.config import(
    MIN_QUANTITY,
    MIN_UNIT_PRICE,
    CANCELLATION_PREFIX,
)


def test_remove_cancellations(sample_df: pd.DataFrame) -> None:
    """
    Tests data_cleaning: remove_cancellations on sample retail dataframe.
    :param sample_df: sample retail dataframe
    :return: None
    """

    sample_rows = sample_df.shape[0]
    # sum Trues in a boolean series
    cancel_count = sample_df['InvoiceNo'].str.startswith(CANCELLATION_PREFIX, na=False).sum()
    df = remove_cancellations(sample_df)

    assert df.shape[0] == sample_rows - cancel_count
    assert not df['InvoiceNo'].str.startswith(CANCELLATION_PREFIX, na=False).any()


def test_remove_duplicates(sample_df: pd.DataFrame) -> None:
    """
    Test data cleaning: remove_duplicates from sample retail dataframe.
    :param sample_df: sample retail dataframe
    :return: None
    """

    distinct_rows = len(sample_df.drop_duplicates())
    df = remove_duplicates(sample_df)

    assert df.shape[0] == distinct_rows


def test_remove_missing_customers(sample_df: pd.DataFrame) -> None:
    """
    Test data cleaning: remove_missing_customers from sample retail dataframe.
    :param sample_df: sample retail dataframe
    :return: None
    """

    customer_rows = len(sample_df.dropna(subset=['CustomerID']))
    df = remove_missing_customers(sample_df)

    assert df.shape[0] == customer_rows


def test_remove_invalid_values(sample_df: pd.DataFrame) -> None:
    """
    Test data cleaning: remove_invalid_values from sample retail dataframe.
    :param sample_df: sample retail dataframe
    :return: None
    """

    valid_rows = len(sample_df[(sample_df['Quantity'] >= MIN_QUANTITY) & (sample_df['UnitPrice'] >= MIN_UNIT_PRICE)])
    df = remove_invalid_values(sample_df)

    assert df.shape[0] == valid_rows


def test_remove_non_product_records(sample_df: pd.DataFrame) -> None:
    """
    Test data cleaning: remove_non_product_records from sample retail dataframe.
    :param sample_df: sample retail dataframe
    :return: None
    """

    product_rows = len(sample_df[sample_df['StockCode'].astype(str).str.match(r'^\d') \
                                 & (sample_df['UnitPrice'] >= MIN_UNIT_PRICE)])
    df = remove_non_product_records(sample_df)

    assert df.shape[0] == product_rows
