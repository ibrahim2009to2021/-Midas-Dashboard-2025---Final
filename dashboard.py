"""
Midas Furniture Campaign Analytics Dashboard
Simplified homepage for multi-page app
Version: 3.0 - Clean & Working
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Any
import plotly.graph_objects as go
import plotly.express as px

# ========================================
# PAGE CONFIGURATION
# ========================================

st.set_page_config(
    page_title="Midas Analytics Platform",
    page_icon="🛋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# DATA LOADING FUNCTIONS
# ========================================

@st.cache_data(ttl=3600)
def load_campaign_data() -> pd.DataFrame:
    """Load campaign performance data"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=90), end=datetime.now(), freq='D')
    campaigns = ['Spring Sale 2025', 'Summer Collection', 'Bedroom Special', 'Living Room Deals', 'Office Furniture']
    platforms = ['Meta', 'Google', 'TikTok', 'Snapchat']
    
    data = []
    for date in dates:
        for campaign in campaigns:
            for platform in platforms:
                spend = np.random.uniform(500, 2000)
                impressions = int(spend * np.random.uniform(800, 1200))
                clicks = int(impressions * np.random.uniform(0.01, 0.03))
                conversions = int(clicks * np.random.uniform(0.02, 0.08))
                revenue = conversions * np.random.uniform(300, 800)
                
                data.append({
                    'date': date,
                    'campaign_name': campaign,
                    'platform': platform,
                    'spend': round(spend, 2),
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'revenue': round(revenue, 2),
                    'roas': round(revenue/spend, 2) if spend > 0 else 0,
                    'cpa': round(spend/conversions, 2) if conversions > 0 else 0,
                    'ctr': round(clicks/impressions*100, 3) if impressions > 0 else 0
                })
    
    return pd.DataFrame(data)

# ========================================
# SIDEBAR
# ========================================

def render_sidebar(campaign_df: pd.DataFrame):
    """Render sidebar with quick stats"""
    
    st.sidebar.title("👤 Admin User")
    st.sidebar.caption("ADMINISTRATOR")
    st.sidebar.divider()
    
    # Quick Stats
    st.sidebar.subheader("⚡ Quick Stats")
    
    active_campaigns = campaign_df['campaign_name'].nunique()
    total_spend = campaign_df['spend'].sum()
    avg_roas = (campaign_df['revenue'].sum() / campaign_df['spend'].sum()) if campaign_df['spend'].sum() > 0 else 0
    
    st.sidebar.metric("Active Campaigns", f"{active_campaigns}")
    st.sidebar.metric("Total Spend", f"${total_spend:,.0f}")
    st.sidebar.metric("Avg ROAS", f"{avg_roas:.2f}x", delta="Target: 2.5x")
    
    st.sidebar.divider()
    st.sidebar.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

# ========================================
# MAIN DASHBOARD
# ========================================

def render_dashboard(campaign_df: pd.DataFrame):
    """Main dashboard page"""
    
    st.title("🛋️ Midas Furniture Campaign Analytics")
    st.markdown("Welcome to your analytics dashboard. Use the sidebar to navigate between pages.")
    st.markdown("---")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_spend = campaign_df['spend'].sum()
    total_revenue = campaign_df['revenue'].sum()
    total_conversions = campaign_df['conversions'].sum()
    overall_roas = total_revenue / total_spend if total_spend > 0 else 0
    
    with col1:
        st.metric("Total Spend", f"${total_spend:,.0f}")
    with col2:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    with col3:
        st.metric("ROAS", f"{overall_roas:.2f}x")
    with col4:
        st.metric("Conversions", f"{total_conversions:,.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Platform")
        platform_revenue = campaign_df.groupby('platform')['revenue'].sum().reset_index()
        fig = px.bar(platform_revenue, x='platform', y='revenue', color='platform')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Daily ROAS Trend")
        daily_metrics = campaign_df.groupby('date').agg({'revenue': 'sum', 'spend': 'sum'}).reset_index()
        daily_metrics['roas'] = daily_metrics['revenue'] / daily_metrics['spend']
        fig = px.line(daily_metrics, x='date', y='roas')
        fig.add_hline(y=2.5, line_dash="dash", line_color="red", annotation_text="Target")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Campaigns Table
    st.subheader("Top Performing Campaigns")
    top_campaigns = campaign_df.groupby('campaign_name').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'conversions': 'sum'
    }).reset_index()
    top_campaigns['roas'] = (top_campaigns['revenue'] / top_campaigns['spend']).round(2)
    top_campaigns = top_campaigns.sort_values('revenue', ascending=False).head(10)
    st.dataframe(top_campaigns, use_container_width=True, hide_index=True)
    
    # Navigation hint
    st.info("💡 **Tip:** Use the sidebar on the left to navigate to other analysis pages!")

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    """Main application"""
    
    # Load data
    with st.spinner("Loading data..."):
        campaign_df = load_campaign_data()
    
    # Render sidebar
    render_sidebar(campaign_df)
    
    # Show dashboard
    render_dashboard(campaign_df)

if __name__ == "__main__":
    main()
