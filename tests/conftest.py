import pytest
import pandas as pd

@pytest.fixture
def sample_df() -> pd.DataFrame:
    """
    Sample retail DataFrame for unit testing.
    :return: sample retail DataFrame with 6 rows covering valid, cancellation, duplicate,
    null, and invalid value scenarios
    """

    df = pd.DataFrame({
        'InvoiceNo': ['536365', 'C536366', '536365', '536367', '536368', '536369'],  # valid row, cancellation, duplicate row, valid, valid
        'CustomerID': [17850.0, 17851.0, 17850.0,  None, 17852.0, 17853.0], # valid row, valid, duplicate row, null, valid, valid
        'Quantity': [3, 10, 3, 5, 0, 23],  # valid row, valid, duplicate row, valid, not valid, valid
        'UnitPrice': [1.25, 39.00, 1.25, -1.25, 4.99, 12.50], # valid row, valid, duplicate row, not valid, valid, valid
        'StockCode': ['60125', '60126', '60125', 'B', 'M', '60127'], # valid, valid, duplicate row, not valid, not valid, valid
        'Description': ['mug', 'bath mat', 'mug', 'wooden box', None, 'charm'], # valid, valid, duplicate row, valid, valid, valid
        'InvoiceDate': ['2011-01-01', '2011-02-15', '2011-01-01', '2012-03-22', '2012-08-28', '2012-11-10'], # valid, valid, duplicate row, valid, valid, valid
        'Country': ['United Kingdom', None,'United Kingdom','Spain','Japan', 'USA'] # valid, valid, duplicate row, valid, valid, valid
    })

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    return df