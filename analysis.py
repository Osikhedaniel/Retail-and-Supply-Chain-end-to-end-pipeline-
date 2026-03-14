from loguru import logger
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime
import os

load_dotenv()

logger.info("Starting analysis...")

DATABASE_URL = os.getenv("DATABASE_URL")


def load_data_from_db():
    """Load customers and orders tables from PostgreSQL"""

    logger.info("Connecting to database...")

    conn = psycopg2.connect(DATABASE_URL)

    try:
        logger.info("Loading customers table...")
        customer_df = pd.read_sql_query(
            "SELECT * FROM customer_data_zion",
            conn
        )

        logger.info("Loading orders table...")
        order_df = pd.read_sql_query(
            "SELECT * FROM order_data_zion",
            conn
        )

        logger.success("Data loaded successfully!")

        return customer_df, order_df

    except Exception as e:
        logger.error(f"Database error: {e}")
        raise

    finally:
        conn.close()
        logger.info("Database connection closed.")


def data_analysis(customer_df, orders_df):

    df_customers = customer_df.copy()
    df_orders = orders_df.copy()

    logger.info("Converting dates...")
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
    df_orders['delivery_date'] = pd.to_datetime(df_orders['delivery_date'])

    logger.info("Merging customer and order datasets...")
    df = pd.merge(df_orders, df_customers, on='customer_id', how='left')

    logger.info("Calculating purchase frequency...")
    purchase_frequency = (
        df.groupby('customer_id')
        .agg(
            total_orders=('order_id','count'),
            total_spent=('order_amount','sum'),
            avg_order_value=('order_amount','mean')
        )
        .reset_index()
    )

    logger.info("Calculating recency...")
    latest_date = df['order_date'].max()

    recency = (
        df.groupby('customer_id')['order_date']
        .max()
        .reset_index()
    )

    recency['days_since_last_purchase'] = (
        latest_date - recency['order_date']
    ).dt.days

    recency.drop(columns=['order_date'], inplace=True)

    logger.info("Calculating tenure...")
    tenure = (
        df.groupby('customer_id')['order_date']
        .min()
        .reset_index()
    )

    tenure['tenure_days'] = (latest_date - tenure['order_date']).dt.days
    tenure.drop(columns=['order_date'], inplace=True)

    logger.info("Analyzing cancellations and failures...")
    order_status = (
        df.groupby(['customer_id','order_status'])
        .size()
        .reset_index()
    )

    payment_pattern = (
        df.groupby(['customer_id','payment_method'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    logger.info("Building customer behavior table...")
    analysis_df = (
        purchase_frequency
        .merge(recency, on='customer_id')
        .merge(tenure, on='customer_id')
        .merge(order_status, on='customer_id', how='left')
        .merge(payment_pattern, on='customer_id', how='left')
        .merge(df_customers, on='customer_id', how='left')
    )

    logger.info("Segmenting customers by frequency...")

    def frequency_segment(x):
        if x >= 20:
            return "Loyal"
        elif x >= 10:
            return "Regular"
        elif x >= 3:
            return "Occasional"
        else:
            return "One-time"

    analysis_df['purchase_segment'] = analysis_df['total_orders'].apply(frequency_segment)

    logger.info("Identifying potential churn customers...")

    churn_threshold = 90

    analysis_df['churn_risk'] = np.where(
        analysis_df['days_since_last_purchase'] > churn_threshold,
        "High Risk",
        "Active"
    )

    logger.info("Aggregating demographic insights...")

    demographic_summary = (
        analysis_df
        .groupby(['state','gender','purchase_segment'])
        .agg(
            customers=('customer_id','count'),
            avg_spent=('total_spent','mean'),
            avg_orders=('total_orders','mean')
        )
        .reset_index()
    )

    logger.info("Detecting churn patterns...")

    churn_patterns = analysis_df[
        analysis_df['churn_risk'] == "High Risk"
    ][[
        'customer_id',
        'total_orders',
        'total_spent',
        'days_since_last_purchase',
        'tenure_days',
        'purchase_segment',
        'order_status'
    ]]

    logger.success("Analysis completed successfully!")

    return {
        "customer_behavior": analysis_df,
        "demographic_summary": demographic_summary,
        "churn_patterns": churn_patterns
    }

# Load data from database
customer_df, order_df = load_data_from_db()

# Run analysis
results = data_analysis(customer_df, order_df)

customer_behavior = results['customer_behavior']
demographic_summary = results['demographic_summary']
churn_patterns = results['churn_patterns']

print("Customer Behavior")
print(customer_behavior.head(10))

print("Demographic Summary")
print(demographic_summary.head(10))

print("Churn Patterns")
print(churn_patterns.head(10))