"""
Segmentation Analysis Page
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Segmentation Analysis", page_icon="👥", layout="wide")

@st.cache_data(ttl=3600)
def load_persona_data():
    segments = ['High Value Shoppers', 'Budget Conscious', 'Design Enthusiasts', 'First Time Buyers', 'Repeat Customers']
    data = []
    for i in range(1000):
        segment = np.random.choice(segments)
        ltv = np.random.uniform(500, 5000) if segment == 'High Value Shoppers' else np.random.uniform(300, 2000)
        data.append({
            'customer_id': f"CUST_{i:05d}",
            'segment': segment,
            'lifetime_value': round(ltv, 2),
            'avg_order_value': round(ltv/np.random.uniform(1, 5), 2),
            'purchase_frequency': round(np.random.uniform(1, 8), 1),
            'conversion_rate': round(np.random.uniform(1, 8), 2)
        })
    return pd.DataFrame(data)

st.title("👥 Segmentation Analysis")
st.markdown("---")

persona_df = load_persona_data()
segment_stats = persona_df.groupby('segment').agg({
    'customer_id': 'count',
    'lifetime_value': 'mean',
    'avg_order_value': 'mean',
    'purchase_frequency': 'mean'
}).reset_index()
segment_stats.columns = ['Segment', 'Customers', 'Avg LTV', 'Avg AOV', 'Avg Frequency']

col1, col2 = st.columns(2)
with col1:
    fig = px.pie(segment_stats, values='Customers', names='Segment', title='Customer Distribution')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.bar(segment_stats, x='Segment', y='Avg LTV', title='Average Lifetime Value by Segment')
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Segment Details")
st.dataframe(segment_stats, use_container_width=True, hide_index=True)
