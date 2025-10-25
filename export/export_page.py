"""
Export Page Module
Provides UI for exporting data in various formats
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from .data_exporter import DataExporter

def render_export_page(campaign_df: pd.DataFrame, creative_df: pd.DataFrame, persona_df: pd.DataFrame):
    """Render the export page interface"""
    
    st.title("📤 Export Data")
    st.markdown("Export your analytics data in multiple formats")
    st.markdown("---")
    
    # Initialize exporter
    exporter = DataExporter()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Quick Export", "📁 Multi-Sheet Export", "📈 Summary Report"])
    
    with tab1:
        render_quick_export(campaign_df, creative_df, persona_df, exporter)
    
    with tab2:
        render_multi_sheet_export(campaign_df, creative_df, persona_df, exporter)
    
    with tab3:
        render_summary_report(campaign_df, exporter)

def render_quick_export(campaign_df: pd.DataFrame, creative_df: pd.DataFrame, 
                        persona_df: pd.DataFrame, exporter: DataExporter):
    """Render quick export tab"""
    
    st.subheader("📊 Quick Single-File Export")
    st.info("Export a single dataset to CSV format")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_type = st.selectbox(
            "Select Data Type",
            ["Campaign Performance", "Creative Performance", "Customer Personas"]
        )
    
    with col2:
        date_filter = st.selectbox(
            "Date Range",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"]
        )
    
    # Filter data based on selection
    if data_type == "Campaign Performance":
        export_df = exporter.prepare_campaign_export(campaign_df)
        filename = "campaign_data"
    elif data_type == "Creative Performance":
        export_df = exporter.prepare_creative_export(creative_df)
        filename = "creative_data"
    else:
        export_df = exporter.prepare_persona_export(persona_df)
        filename = "persona_data"
    
    # Apply date filter for campaign data
    if data_type == "Campaign Performance" and 'date' in export_df.columns:
        today = datetime.now()
        if date_filter == "Last 7 Days":
            cutoff = today - timedelta(days=7)
            export_df['date'] = pd.to_datetime(export_df['date'])
            export_df = export_df[export_df['date'] >= cutoff]
            export_df['date'] = export_df['date'].dt.strftime('%Y-%m-%d')
        elif date_filter == "Last 30 Days":
            cutoff = today - timedelta(days=30)
            export_df['date'] = pd.to_datetime(export_df['date'])
            export_df = export_df[export_df['date'] >= cutoff]
            export_df['date'] = export_df['date'].dt.strftime('%Y-%m-%d')
        elif date_filter == "Last 90 Days":
            cutoff = today - timedelta(days=90)
            export_df['date'] = pd.to_datetime(export_df['date'])
            export_df = export_df[export_df['date'] >= cutoff]
            export_df['date'] = export_df['date'].dt.strftime('%Y-%m-%d')
    
    st.markdown("---")
    st.markdown("### 👀 Data Preview")
    st.dataframe(export_df.head(10), use_container_width=True)
    
    st.info(f"📊 Total rows: {len(export_df):,}")
    
    # Export buttons
    st.markdown("---")
    st.markdown("### 💾 Download")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = exporter.to_csv(export_df)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"{filename}_{exporter.export_timestamp}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        excel_data = exporter.to_excel({filename: export_df})
        st.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name=f"{filename}_{exporter.export_timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

def render_multi_sheet_export(campaign_df: pd.DataFrame, creative_df: pd.DataFrame,
                              persona_df: pd.DataFrame, exporter: DataExporter):
    """Render multi-sheet export tab"""
    
    st.subheader("📁 Multi-Sheet Excel Export")
    st.info("Export all datasets to a single Excel file with multiple sheets")
    
    # Prepare all data
    campaign_export = exporter.prepare_campaign_export(campaign_df)
    creative_export = exporter.prepare_creative_export(creative_df)
    persona_export = exporter.prepare_persona_export(persona_df)
    
    # Summary stats
    st.markdown("### 📊 Export Contents")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Campaign Records", f"{len(campaign_export):,}")
    
    with col2:
        st.metric("Creative Records", f"{len(creative_export):,}")
    
    with col3:
        st.metric("Customer Records", f"{len(persona_export):,}")
    
    st.markdown("---")
    
    # Sheet selection
    st.markdown("### 📄 Select Sheets to Include")
    
    include_campaign = st.checkbox("Campaign Performance", value=True)
    include_creative = st.checkbox("Creative Performance", value=True)
    include_persona = st.checkbox("Customer Personas", value=True)
    
    # Build export dictionary
    export_dict = {}
    if include_campaign:
        export_dict["Campaigns"] = campaign_export
    if include_creative:
        export_dict["Creatives"] = creative_export
    if include_persona:
        export_dict["Personas"] = persona_export
    
    if not export_dict:
        st.warning("⚠️ Please select at least one sheet to export")
    else:
        st.success(f"✅ Ready to export {len(export_dict)} sheet(s)")
        
        st.markdown("---")
        
        # Export button
        excel_data = exporter.to_excel(export_dict)
        st.download_button(
            label=f"📊 Download Excel Workbook ({len(export_dict)} sheets)",
            data=excel_data,
            file_name=f"midas_complete_{exporter.export_timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

def render_summary_report(campaign_df: pd.DataFrame, exporter: DataExporter):
    """Render summary report tab"""
    
    st.subheader("📈 Summary Report")
    st.info("Generate a summary report with key metrics and insights")
    
    # Get summary stats
    stats = exporter.create_summary_stats(campaign_df)
    
    # Display summary
    st.markdown("### 📊 Campaign Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Spend", f"${stats['total_spend']:,.0f}")
    
    with col2:
        st.metric("Total Revenue", f"${stats['total_revenue']:,.0f}")
    
    with col3:
        st.metric("Total Conversions", f"{stats['total_conversions']:,.0f}")
    
    with col4:
        st.metric("Avg ROAS", f"{stats['avg_roas']:.2f}x")
    
    st.markdown("---")
    
    # Additional details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Date Range:**")
        st.write(f"From {stats['date_range']['start']} to {stats['date_range']['end']}")
    
    with col2:
        st.markdown("**📊 Coverage:**")
        st.write(f"• {stats['campaigns_count']} campaigns")
        st.write(f"• {stats['platforms_count']} platforms")
    
    st.markdown("---")
    
    # Create summary DataFrame
    summary_data = {
        'Metric': ['Total Spend', 'Total Revenue', 'Total Conversions', 'Average ROAS', 'Campaigns', 'Platforms'],
        'Value': [
            f"${stats['total_spend']:,.2f}",
            f"${stats['total_revenue']:,.2f}",
            f"{stats['total_conversions']:,}",
            f"{stats['avg_roas']:.2f}x",
            stats['campaigns_count'],
            stats['platforms_count']
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    
    st.markdown("### 📄 Summary Table")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Export summary
    csv_data = exporter.to_csv(summary_df)
    st.download_button(
        label="📥 Download Summary Report (CSV)",
        data=csv_data,
        file_name=f"midas_summary_{exporter.export_timestamp}.csv",
        mime="text/csv",
        use_container_width=True
    )
