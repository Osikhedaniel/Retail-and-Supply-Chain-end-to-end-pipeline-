import pandas as pd 
import requests 
import json 
from loguru import logger 
from pathlib import Path 

def extracting_csv(filepath):
    df = pd.read_csv(filepath)
    if df.empty:
        logger.error("No Data in the DataFrame")
    else:
        logger.info(f"Data in DataFrame contains {df.shape[0]} rows and {df.shape[1]} columns")
    return df 

def structure_json(source,from_api=False):
    try:
        if from_api:
            response = requests.get(source,timeout=30)
            response.raise_for_status()
            data = response.json()
        else:
            source = Path(source)
            with open(source,"r",encoding="utf-8") as f:
                data = json.load(f)
     
        if isinstance(data,list):
            df = pd.json_normalize(data)
        elif isinstance(data,dict):
            for value in data.values():
                if isinstance(value,list):
                    df = pd.json_normalize(value)
                    break 
            else:
                df = pd.json_normalize(data) 
        else:
            raise ValueError("JSON stucture could not be normalized")
    
        if df.empty:
            logger.error("JSON loaded but resulted in empty dataframe")
        else:
            logger.error(f"Data from JSON present in the DataFrame contains {df.shape[0]} rows and {df.shape[1]} columns")
    except Exception as e:
        logger.exception("Failed to structure JSON data")
        raise e 



    

    