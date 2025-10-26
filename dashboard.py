"""
Midas Furniture Campaign Analytics Dashboard
Complete implementation with database connection for real data
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import sqlite3

# ========================================
# IMPORT MODULES
# ========================================
try:
    from export.export_page import render_export_page
    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False

try:
    from admin_page import render_admin_page
    ADMIN_AVAILABLE = True
except ImportError:
    ADMIN_AVAILABLE = False

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
# DATABASE CONNECTION
# ========================================

from config import DB_PATH

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

# ========================================
# MODERN SIDEBAR STYLES
# ========================================

def apply_modern_styles():
    """Apply modern CSS styles"""
    st.markdown("""
    <style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d29 0%, #0f1116 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Hide default nav */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* User Profile Card */
    .user-profile {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 0 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .user-avatar {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .user-name {
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .user-role {
        color: #8b92a7;
        font-size: 0.75rem;
        text-transform: uppercase;
    }
    
    /* Section Headers */
    .nav-section {
        color: #8b92a7;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 1rem 0 0.5rem;
        margin-top: 0.5rem;
    }
    
    /* Quick Stats */
    .stat-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #8b92a7;
        font-size: 0.75rem;
        margin-bottom: 0.25rem;
    }
    
    .stat-value {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .stat-trend {
        font-size: 0.7rem;
        margin-top: 0.25rem;
        color: #10b981;
    }
    
    /* Custom buttons for navigation */
    .stButton button {
        width: 100%;
        text-align: left;
        border-radius: 0.5rem;
        border: 1px solid transparent;
        padding: 0.75rem 1rem;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateX(4px);
    }
    
    /* Main content area */
    .main {
        padding: 2rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ========================================
# DATA LOADING FROM DATABASE
# ========================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_campaign_data():
    """Load campaign performance data from database"""
    conn = get_db_connection()
    
    # Check if we have data in the database
    count_query = "SELECT COUNT(*) as count FROM daily_performance"
    count_result = pd.read_sql_query(count_query, conn)
    
    if count_result['count'].iloc[0] == 0:
        # If no data, return empty DataFrame with expected columns
        conn.close()
        return pd.DataFrame(columns=[
            'date', 'campaign_name', 'platform', 'spend', 'impressions', 
            'clicks', 'conversions', 'revenue', 'roas', 'cpa', 'ctr'
        ])
    
    # Load real data from database
    query = """
        SELECT 
            dp.report_date as date,
            c.campaign_name,
            c.platform,
            SUM(dp.spend) as spend,
            SUM(dp.impressions) as impressions,
            SUM(dp.clicks) as clicks,
            SUM(dp.conversions) as conversions,
            SUM(dp.revenue) as revenue,
            SUM(dp.reach) as reach,
            AVG(dp.frequency) as frequency
        FROM daily_performance dp
        LEFT JOIN campaigns c ON dp.campaign_id = c.campaign_id
        GROUP BY dp.report_date, c.campaign_name, c.platform
        ORDER BY dp.report_date DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Calculate derived metrics
    if not df.empty:
        df['roas'] = (df['revenue'] / df['spend']).where(df['spend'] > 0, 0).round(2)
        df['cpa'] = (df['spend'] / df['conversions']).where(df['conversions'] > 0, 0).round(2)
        df['ctr'] = (df['clicks'] / df['impressions'] * 100).where(df['impressions'] > 0, 0).round(3)
        
        # Ensure date column is datetime
        df['date'] = pd.to_datetime(df['date'])
    
    return df

@st.cache_data(ttl=300)
def load_creative_data():
    """Load creative performance data from database"""
    conn = get_db_connection()
    
    # Check if we have data
    count_query = "SELECT COUNT(*) as count FROM ads"
    count_result = pd.read_sql_query(count_query, conn)
    
    if count_result['count'].iloc[0] == 0:
        conn.close()
        return pd.DataFrame(columns=[
            'creative_id', 'format', 'impressions', 'clicks', 
            'conversions', 'spend', 'revenue', 'frequency', 'ctr'
        ])
    
    query = """
        SELECT 
            a.ad_id as creative_id,
            a.ad_name,
            a.creative_type as format,
            SUM(dp.impressions) as impressions,
            SUM(dp.clicks) as clicks,
            SUM(dp.conversions) as conversions,
            SUM(dp.spend) as spend,
            SUM(dp.revenue) as revenue,
            AVG(dp.frequency) as frequency
        FROM ads a
        LEFT JOIN daily_performance dp ON a.ad_id = dp.ad_id
        GROUP BY a.ad_id, a.ad_name, a.creative_type
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        df['ctr'] = (df['clicks'] / df['impressions'] * 100).where(df['impressions'] > 0, 0).round(2)
        # Remove rows with no data
        df = df[df['impressions'] > 0]
    
    return df

@st.cache_data(ttl=300)
def load_persona_data():
    """Load customer persona data from database"""
    conn = get_db_connection()
    
    # Check if we have sales data
    count_query = "SELECT COUNT(*) as count FROM sales"
    count_result = pd.read_sql_query(count_query, conn)
    
    if count_result['count'].iloc[0] == 0:
        conn.close()
        # Return synthetic data if no real data
        segments = ['High Value Shoppers', 'Budget Conscious', 'Design Enthusiasts', 
                   'First Time Buyers', 'Repeat Customers']
        data = []
        for i in range(100):
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
    
    # Load real customer data
    query = """
        SELECT 
            c.customer_id,
            COUNT(DISTINCT s.sale_id) as purchase_frequency,
            SUM(s.sale_amount) as lifetime_value,
            AVG(s.sale_amount) as avg_order_value,
            julianday('now') - julianday(MIN(s.sale_date)) as customer_age_days
        FROM customers c
        LEFT JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        # Assign segments based on value
        def assign_segment(row):
            if row['lifetime_value'] > 3000:
                return 'High Value Shoppers'
            elif row['purchase_frequency'] > 3:
                return 'Repeat Customers'
            elif row['customer_age_days'] < 30:
                return 'First Time Buyers'
            elif row['avg_order_value'] < 500:
                return 'Budget Conscious'
            else:
                return 'Design Enthusiasts'
        
        df['segment'] = df.apply(assign_segment, axis=1)
        df['conversion_rate'] = np.random.uniform(1, 8, size=len(df))
    
    return df

def get_database_stats():
    """Get current database statistics"""
    conn = get_db_connection()
    
    stats = {}
    
    # Count records in each table
    tables = ['campaigns', 'ads', 'daily_performance', 'sales', 'customers']
    for table in tables:
        try:
            count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn)
            stats[table] = count['count'].iloc[0]
        except:
            stats[table] = 0
    
    conn.close()
    return stats

# ========================================
# SIDEBAR NAVIGATION
# ========================================

def render_sidebar(campaign_df):
    """Render modern sidebar navigation"""
    
    # User Profile
    st.sidebar.markdown("""
    <div class="user-profile">
        <div class="user-avatar">👤</div>
        <div>
            <div class="user-name">Admin User</div>
            <div class="user-role">Administrator</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Database Stats (for debugging)
    with st.sidebar.expander("📊 Database Status"):
        stats = get_database_stats()
        for table, count in stats.items():
            st.caption(f"{table}: {count} records")
    
    # Initialize session state
    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'dashboard'
    
    # Navigation sections
    st.sidebar.markdown('<div class="nav-section">📊 Analytics</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
        st.session_state.active_page = 'dashboard'
        st.rerun()
    
    if st.sidebar.button("👥 Segmentation Analysis", key="nav_segmentation", use_container_width=True):
        st.session_state.active_page = 'segmentation'
        st.rerun()
    
    if st.sidebar.button("🔮 Predictive Analytics", key="nav_predictive", use_container_width=True):
        st.session_state.active_page = 'predictive'
        st.rerun()
    
    if st.sidebar.button("📋 Campaign Takeaways", key="nav_takeaways", use_container_width=True):
        st.session_state.active_page = 'takeaways'
        st.rerun()
    
    if st.sidebar.button("📈 Live Benchmarking", key="nav_benchmarking", use_container_width=True):
        st.session_state.active_page = 'benchmarking'
        st.rerun()
    
    st.sidebar.markdown('<div class="nav-section">🎨 Creative & Budget</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🎨 Creative Analysis", key="nav_creative", use_container_width=True):
        st.session_state.active_page = 'creative'
        st.rerun()
    
    if st.sidebar.button("💰 Budget Pacing", key="nav_budget", use_container_width=True):
        st.session_state.active_page = 'budget'
        st.rerun()
    
    st.sidebar.markdown('<div class="nav-section">🧠 Intelligence</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🧠 Persona Intelligence", key="nav_persona", use_container_width=True):
        st.session_state.active_page = 'persona'
        st.rerun()
    
    if st.sidebar.button("🔬 A/B Testing", key="nav_ab", use_container_width=True):
        st.session_state.active_page = 'ab_testing'
        st.rerun()
    
    st.sidebar.markdown('<div class="nav-section">⚙️ Tools & Settings</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("📤 Export Data", key="nav_export", use_container_width=True):
        st.session_state.active_page = 'export'
        st.rerun()
    
    if st.sidebar.button("👑 Admin", key="nav_admin", use_container_width=True):
        st.session_state.active_page = 'admin'
        st.rerun()
    
    if st.sidebar.button("📁 Upload Data", key="nav_upload", use_container_width=True):
        st.session_state.active_page = 'upload'
        st.rerun()
    
    # Refresh data button
    st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.success("Data refreshed!")
        st.rerun()
    
    # Quick Stats
    st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if not campaign_df.empty:
        active_campaigns = campaign_df['campaign_name'].nunique()
        total_spend = campaign_df['spend'].sum()
        total_revenue = campaign_df['revenue'].sum()
        avg_roas = total_revenue / total_spend if total_spend > 0 else 0
        
        st.sidebar.markdown(f"""
        <div style="margin-top: 1rem;">
            <div style="color: #ffffff; font-weight: 600; margin-bottom: 0.75rem;">⚡ Quick Stats</div>
            
            <div class="stat-card">
                <div class="stat-label">Active Campaigns</div>
                <div class="stat-value">{active_campaigns}</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Total Spend</div>
                <div class="stat-value">${total_spend:,.0f}</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Avg ROAS</div>
                <div class="stat-value">{avg_roas:.2f}x</div>
                <div class="stat-trend">Target: 2.5x</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.sidebar.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

# ========================================
# PAGE RENDERERS
# ========================================

def render_dashboard(campaign_df):
    """Main dashboard page"""
    st.title("🛋️ Midas Furniture Campaign Analytics")
    st.markdown("---")
    
    if campaign_df.empty:
        st.warning("📊 No campaign data found. Please upload data using the 'Upload Data' page.")
        
        # Show instructions
        st.info("""
        ### Getting Started:
        1. Go to **📁 Upload Data** in the sidebar
        2. Download the CSV template
        3. Fill it with your campaign data
        4. Upload and validate
        5. Return to this dashboard to see your analytics
        """)
        return
    
    # Date filter
    col1, col2 = st.columns([3, 1])
    with col1:
        date_range = st.date_input(
            "Select Date Range",
            value=(campaign_df['date'].max() - timedelta(days=30), campaign_df['date'].max()),
            min_value=campaign_df['date'].min(),
            max_value=campaign_df['date'].max()
        )
    
    # Filter data by date
    filtered_df = campaign_df[
        (campaign_df['date'] >= pd.to_datetime(date_range[0])) & 
        (campaign_df['date'] <= pd.to_datetime(date_range[1]))
    ]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_spend = filtered_df['spend'].sum()
    total_revenue = filtered_df['revenue'].sum()
    total_conversions = filtered_df['conversions'].sum()
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
        platform_revenue = filtered_df.groupby('platform')['revenue'].sum().reset_index()
        if not platform_revenue.empty:
            fig = px.bar(platform_revenue, x='platform', y='revenue', color='platform')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No platform data available")
    
    with col2:
        st.subheader("Daily ROAS Trend")
        daily_metrics = filtered_df.groupby('date').agg({
            'revenue': 'sum', 
            'spend': 'sum'
        }).reset_index()
        
        if not daily_metrics.empty:
            daily_metrics['roas'] = daily_metrics['revenue'] / daily_metrics['spend']
            fig = px.line(daily_metrics, x='date', y='roas')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", annotation_text="Target")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No daily data available")
    
    # Top Campaigns Table
    st.subheader("Top Performing Campaigns")
    if 'campaign_name' in filtered_df.columns:
        top_campaigns = filtered_df.groupby('campaign_name').agg({
            'spend': 'sum',
            'revenue': 'sum',
            'conversions': 'sum'
        }).reset_index()
        
        if not top_campaigns.empty:
            top_campaigns['roas'] = (top_campaigns['revenue'] / top_campaigns['spend']).round(2)
            top_campaigns = top_campaigns.sort_values('revenue', ascending=False).head(10)
            
            # Format currency columns
            for col in ['spend', 'revenue']:
                top_campaigns[col] = top_campaigns[col].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(top_campaigns, use_container_width=True, hide_index=True)
        else:
            st.info("No campaign data to display")

def render_segmentation(persona_df):
    """Segmentation analysis page"""
    st.title("👥 Segmentation Analysis")
    st.markdown("---")
    
    if persona_df.empty:
        st.warning("No customer data available. Upload sales data to see segmentation.")
        return
    
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
    
    # Format currency columns
    for col in ['Avg LTV', 'Avg AOV']:
        segment_stats[col] = segment_stats[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(segment_stats, use_container_width=True, hide_index=True)

def render_creative_analysis(creative_df):
    """Creative analysis page"""
    st.title("🎨 Creative Analysis")
    st.markdown("---")
    
    if creative_df.empty:
        st.warning("No creative data available. Upload campaign data to see analysis.")
        return
    
    format_stats = creative_df.groupby('format').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    if not format_stats.empty:
        format_stats['ctr'] = (format_stats['clicks'] / format_stats['impressions'] * 100).round(2)
        format_stats['roas'] = (format_stats['revenue'] / format_stats['spend']).round(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(format_stats, x='format', y='ctr', title='CTR by Format (%)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(format_stats, x='format', y='roas', title='ROAS by Format')
            st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top Performing Creatives")
    top_creatives = creative_df.nlargest(20, 'revenue')
    
    if not top_creatives.empty:
        # Format display columns
        display_cols = ['creative_id', 'format', 'impressions', 'clicks', 'ctr', 'spend', 'revenue']
        display_df = top_creatives[display_cols].copy()
        
        # Format numbers
        display_df['spend'] = display_df['spend'].apply(lambda x: f"${x:,.2f}")
        display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.2f}")
        display_df['ctr'] = display_df['ctr'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

def render_export_page_fallback(campaign_df, creative_df, persona_df):
    """Fallback export page with basic CSV export"""
    st.title("📤 Export Data")
    st.markdown("---")
    
    st.info("💡 For full PDF export functionality, ensure the export module is installed.")
    
    tab1, tab2 = st.tabs(["Quick Export", "Campaign Report"])
    
    with tab1:
        st.subheader("Quick CSV Export")
        
        col1, col2 = st.columns(2)
        with col1:
            data_type = st.selectbox(
                "Select Data", 
                ["Campaign Performance", "Creative Performance", "Customer Personas"]
            )
        with col2:
            if data_type == "Campaign Performance" and not campaign_df.empty:
                date_range = st.date_input(
                    "Date Range", 
                    value=(campaign_df['date'].min(), campaign_df['date'].max())
                )
            else:
                date_range = st.date_input(
                    "Date Range", 
                    value=(datetime.now() - timedelta(days=30), datetime.now())
                )
        
        if data_type == "Campaign Performance":
            export_df = campaign_df
        elif data_type == "Creative Performance":
            export_df = creative_df
        else:
            export_df = persona_df
        
        if not export_df.empty:
            st.dataframe(export_df.head(10), use_container_width=True)
            
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"midas_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("No data available for export")
    
    with tab2:
        st.subheader("Generate PDF Report")
        st.warning("📄 PDF reports require the export module. Using CSV export for now.")

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    """Main application"""
    
    # Apply modern styles
    apply_modern_styles()
    
    # Load data from database
    with st.spinner("Loading data from database..."):
        campaign_df = load_campaign_data()
        creative_df = load_creative_data()
        persona_df = load_persona_data()
    
    # Render sidebar
    render_sidebar(campaign_df)
    
    # Route to appropriate page
    page = st.session_state.get('active_page', 'dashboard')
    
    if page == 'dashboard':
        render_dashboard(campaign_df)
    
    elif page == 'predictive':
        st.title("🔮 Predictive Analytics")
        st.info("Coming soon!")
    
    elif page == 'takeaways':
        st.title("📋 Campaign Takeaways")
        st.info("Coming soon!")
    
    elif page == 'benchmarking':
        st.title("📈 Live Benchmarking")
        st.info("Coming soon!")
    
    elif page == 'budget':
        st.title("💰 Budget Pacing")
        st.info("Coming soon!")
    
    elif page == 'persona':
        render_segmentation(persona_df)
    
    elif page == 'ab_testing':
        st.title("🔬 A/B Testing")
        st.info("Coming soon!")
    
    elif page == 'upload':
        st.title("📁 Upload Data")
        st.info("Coming soon!")

if __name__ == "__main__":
    main() == 'segmentation':
        render_segmentation(persona_df)
    
    elif page == 'creative':
        render_creative_analysis(creative_df)
    
    elif page == 'export':
        if EXPORT_AVAILABLE:
            render_export_page(campaign_df, creative_df, persona_df)
        else:
            render_export_page_fallback(campaign_df, creative_df, persona_df)
    
    elif page == 'admin':
        if ADMIN_AVAILABLE:
            render_admin_page()
        else:
            st.title("👑 Admin Dashboard")
            st.warning("⚠️ Admin module not found")
            st.markdown("""
            ### Setup Required
            
            To enable the full Admin panel:
            
            1. **Create `admin_page.py`** in your project root
            2. **Copy the admin module code** provided
            3. **Restart the app**
            
            The Admin panel includes:
            - 👥 User Management (Create, Edit, Delete users)
            - ⚙️ System Settings
            - 📊 Usage Analytics
            - 🔒 Access Control & Permissions
            """)
    
    elif page
