"""
Export Data Page
Standalone page for data export functionality
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Export Data", page_icon="📤", layout="wide")

# Load data (same as dashboard)
@st.cache_data(ttl=3600)
def load_campaign_data():
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

@st.cache_data(ttl=3600)
def load_creative_data():
    """Load creative performance data"""
    creative_ids = [f"CR_{i:04d}" for i in range(1, 51)]
    formats = ['Video', 'Image', 'Carousel']
    
    data = []
    for creative_id in creative_ids:
        impressions = int(np.random.uniform(10000, 100000))
        clicks = int(impressions * np.random.uniform(0.01, 0.03))
        data.append({
            'creative_id': creative_id,
            'format': np.random.choice(formats),
            'impressions': impressions,
            'clicks': clicks,
            'conversions': int(clicks * np.random.uniform(0.02, 0.08)),
            'spend': round(np.random.uniform(200, 1500), 2),
            'revenue': round(np.random.uniform(500, 4000), 2),
            'ctr': round(clicks/impressions*100, 2)
        })
    
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_persona_data():
    """Load customer persona data"""
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

# Try to import export module
try:
    from export.export_page import render_export_page
    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False

# Load data
campaign_df = load_campaign_data()
creative_df = load_creative_data()
persona_df = load_persona_data()

# Render page
if EXPORT_AVAILABLE:
    render_export_page(campaign_df, creative_df, persona_df)
else:
    # Fallback export functionality
    st.title("📤 Export Data")
    st.markdown("---")
    st.info("💡 Basic CSV export functionality")
    
    data_type = st.selectbox("Select Data", ["Campaign Performance", "Creative Performance", "Customer Personas"])
    
    if data_type == "Campaign Performance":
        export_df = campaign_df
    elif data_type == "Creative Performance":
        export_df = creative_df
    else:
        export_df = persona_df
    
    st.dataframe(export_df.head(10), use_container_width=True)
    
    csv = export_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"midas_export_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
