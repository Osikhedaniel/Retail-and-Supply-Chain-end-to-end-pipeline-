import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import load_data_from_db, data_analysis

st.set_page_config(
    page_title="Customer Analytics Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    customer_df, order_df = load_data_from_db()
    results = data_analysis(customer_df, order_df)
    return results 

results = load_data()

customer_behavior = results["customer_behavior"]
demographic_summary = results["demographic_summary"]
churn_patterns = results["churn_patterns"]

st.sidebar.header("Filters")

segment_filter = st.sidebar.multiselect(
    "Purchase Segment",
    options=customer_behavior["purchase_segment"].unique(),
    default=customer_behavior["purchase_segment"].unique()
)

state_filter = st.sidebar.multiselect(
    "State",
    options=customer_behavior["state"].dropna().unique(),
    default=customer_behavior["state"].dropna().unique()
)

date_filter = st.sidebar.multiselect("Date",
    options = customer_behavior['last_purchase_date'].dropna().unique(),
    default = customer_behavior['last_purchase_date'].dropna().unique()
)

filtered_df = customer_behavior[
    (customer_behavior["purchase_segment"].isin(segment_filter)) &
    (customer_behavior["state"].isin(state_filter)) &
    (customer_behavior['last_purchase_date'].isin(date_filter))
]

st.title("📊 Customer Analytics Dashboard")

st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", filtered_df["customer_id"].nunique())
col2.metric("Total Revenue", f"${filtered_df['total_spent'].sum():,.0f}")
col3.metric("Avg Order Value", f"${filtered_df['avg_order_value'].mean():,.0f}")
col4.metric("Churn Rate",
            f"{(filtered_df['churn_risk'] == 'High Risk').mean() * 100:.2f}%")

st.subheader("👥 Customer Segmentation")

segment_chart = (
    filtered_df["purchase_segment"]
    .value_counts()
    .reset_index()
)

fig_segment = px.pie(
    segment_chart,
    names="purchase_segment",
    values="count",
    title="Customer Segments Distribution",
    hole=0.4
)

st.plotly_chart(fig_segment, use_container_width=True)

st.subheader("💰 Revenue by Segment")

revenue_chart = (
    filtered_df.groupby("purchase_segment")["total_spent"]
    .sum()
    .reset_index()
)

fig_revenue = px.bar(
    revenue_chart,
    x="purchase_segment",
    y="total_spent",
    color="purchase_segment",
    title="Revenue Contribution by Segment"
)

st.plotly_chart(fig_revenue, use_container_width=True)

st.subheader("⚠️ Churn Analysis")

churn_chart = (
    filtered_df["churn_risk"]
    .value_counts()
    .reset_index()
)

fig_churn = px.pie(
    churn_chart,
    names="churn_risk",
    values="count",
    title="Churn Distribution",
    color_discrete_sequence=["green", "red"]
)

st.plotly_chart(fig_churn, use_container_width=True)

st.write("### High Risk Customers")
st.dataframe(churn_patterns.head(20), use_container_width=True)

st.subheader("🌍 Demographic Insights")

fig_demo = px.bar(
    demographic_summary,
    x="state",
    y="customers",
    color="purchase_segment",
    barmode="group",
    title="Customers by State & Segment"
)

st.plotly_chart(fig_demo, use_container_width=True)

st.subheader("📈 Customer Behavior (Recency vs Spend)")

fig_scatter = px.scatter(
    filtered_df,
    x="days_since_last_purchase",
    y="total_spent",
    color="purchase_segment",
    size="total_orders",
    hover_data=["customer_id"],
    title="Recency vs Spending Behavior"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("📄 Data Explorer")

st.dataframe(filtered_df, use_container_width=True)

