from loguru import logger
from datetime import datetime
import pandas as pd

logger.info("Starting Transformation...")

def data_quality_check(data):
    # Check for null values in each column
    null_counts = data.isnull().sum()

    for column, null_count in null_counts.items():
        if null_count > 0:
            logger.warning(f"Column '{column}' has {null_count} null values.")
        else:
            logger.info(f"Column '{column}' has no null values.")
    
    # Check for duplicates in each column
    df_dups = data.duplicated().sum()
    
    if df_dups > 0:
        logger.warning(f"{df_dups} duplicated values found.")
    else:
        logger.info(f"{df_dups} duplicated values found.")

    return data

def data_transformation(data):
    # Converts data type
    df = data.copy()

    for col in df.columns:
        # Check if column is object/string type
        if df[col].dtype == 'object':
            
            # Try converting to numeric
            converted = pd.to_numeric(df[col], errors='coerce')
            
            # If there are no NaN after conversion values became, it's fully numeric
            if not converted.isna().any():
                df[col] = converted.astype(int)
    
    # Remove dupliates if any
    df = df.drop_duplicates()
    return df