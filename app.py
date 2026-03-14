import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import load_data_from_db, data_analysis

st.set_page_config(
    page_title="Customer Analytics Dashboard",
    layout="wide"
)

st.title("Customer Analytics Dashboard")

# Load data
@st.cache_data
def load_analysis():
    customer_df, order_df = load_data_from_db()
    results = data_analysis(customer_df, order_df)
    return results

results = load_analysis()

customer_behavior = results["customer_behavior"]
demographic_summary = results["demographic_summary"]
churn_patterns = results["churn_patterns"]

# KPI Metrics
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    customer_behavior["customer_id"].nunique()
)

col2.metric(
    "Total Revenue",
    f"${customer_behavior['total_spent'].sum():,.0f}"
)

col3.metric(
    "Avg Order Value",
    f"${customer_behavior['avg_order_value'].mean():.2f}"
)

col4.metric(
    "High Risk Customers",
    churn_patterns["customer_id"].nunique()
)

# Customer Purchase Segments
st.subheader("Customer Purchase Segments")

segment_chart = (
    customer_behavior["purchase_segment"]
    .value_counts()
    .reset_index()
)

segment_chart.columns = ["purchase_segment", "count"]

fig = px.pie(
    segment_chart,
    names="purchase_segment",
    values="count",
    title="Customer Segmentation"
)

st.plotly_chart(fig, use_container_width=True)

# Revenue by Segment
st.subheader("Revenue by Customer Segment")

segment_revenue = (
    customer_behavior
    .groupby("purchase_segment")["total_spent"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    segment_revenue,
    x="purchase_segment",
    y="total_spent",
    color="purchase_segment",
    title="Revenue Contribution by Segment"
)

st.plotly_chart(fig2, use_container_width=True)

# Churn Risk Distribution
st.subheader("Churn Risk Distribution")

churn_chart = (
    customer_behavior["churn_risk"]
    .value_counts()
    .reset_index()
)

churn_chart.columns = ["churn_risk", "count"]

fig3 = px.bar(
    churn_chart,
    x="churn_risk",
    y="count",
    color="churn_risk",
    title="Churn Risk Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# Demographic Insights
st.subheader("Demographic Insights")

fig4 = px.sunburst(
    demographic_summary,
    path=["state", "gender", "purchase_segment"],
    values="customers",
    title="Customer Demographics"
)

st.plotly_chart(fig4, use_container_width=True)

# High Risk Customers Table
st.subheader("High Risk Customers")

st.dataframe(churn_patterns)