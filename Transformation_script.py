import pandas as pd 
from loguru import logger 

logger.info("Starting Transformation module......") 

def data_quality_check(data):
    logger.info("Running Data quality check....")

    null_values = data.isnull().sum() 
    sum_null_values = null_values.sum() 

    if sum_null_values > 0:
        logger.info(f"Total null values found: {sum_null_values}")
        for column,count in null_values.items():
            if count > 0:
                logger.warning(f"columns {column} has {count} null values")
    else:
        logger.info("No null values found") 

    duplicate_values = data.duplicated().sum()
    if duplicate_values > 0:
        logger.warning(f"{duplicate_values} duplicates found in Data")
    else:
        logger.info("No duplicates found") 

    logger.info("Data quality check ended")
    return data 


def data_transformation(data):
    logger.info("Starting Data transformation......")

    df = data.copy()

    for col in df.select_dtypes(include=["object"]).columns:
        df[col]=df[col].str.strip()

    df.columns = df.columns.str.strip().str.lower() 

    for col in df.select_dtypes(include=["object"]).columns:
        df[col]= pd.to_numeric(df[col],errors='coerce')

    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(0)

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    if before != after:
        logger.info(f"{before-after} duplicate rows removed")
    
    df = df.reset_index(drop=True) 

    logger.info("Data transformation completed")
    return df 