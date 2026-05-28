# ============================================================
# src/data_loader.py
# Ingests raw retail data from a xlsx file. Logs basic information
# such as shape, column names, and data types.
# ============================================================
import pandas as pd

from src.logger import get_logger
from src.config import DATA_FILE

logger = get_logger(__name__)

def load_data(filepath):
    """
    Ingests the raw retail xlsx data file.
    :param filepath: filepath to raw data for ingestion (xlsx)
    :return: df -ingested data (dataframe)
    """
    try:
        df = pd.read_excel(filepath)
        null_counts = df.isnull().sum()

        logger.info(f'Shape: {df.shape[0]} rows, {df.shape[1]} columns')
        # get string for the data types for readability
        logger.info(f"Dtypes: {df.dtypes.astype(str).to_dict()}")
        for col, count in null_counts.items():
            logger.info(f"Null count - {col}: {count}")
        logger.info(f'{DATA_FILE.name} was successfully loaded into a dataframe and returned.')
        return df

    except FileNotFoundError:
        logger.error(f'File not found: {filepath}')
        raise

