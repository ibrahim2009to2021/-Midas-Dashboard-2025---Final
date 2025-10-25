"""
Data Exporter Module
Handles export to CSV, Excel, and PDF formats
"""

import pandas as pd
import io
from datetime import datetime
from typing import Dict, Any, Optional

class DataExporter:
    """Handles data export operations"""
    
    def __init__(self):
        self.export_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def to_csv(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """Export DataFrame to CSV format"""
        if filename is None:
            filename = f"midas_export_{self.export_timestamp}.csv"
        
        return df.to_csv(index=False)
    
    def to_excel(self, data_dict: Dict[str, pd.DataFrame], filename: Optional[str] = None) -> bytes:
        """Export multiple DataFrames to Excel with multiple sheets"""
        if filename is None:
            filename = f"midas_export_{self.export_timestamp}.xlsx"
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return output.getvalue()
    
    def prepare_campaign_export(self, campaign_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare campaign data for export"""
        export_df = campaign_df.copy()
        
        # Format dates
        if 'date' in export_df.columns:
            export_df['date'] = pd.to_datetime(export_df['date']).dt.strftime('%Y-%m-%d')
        
        # Round numeric columns
        numeric_columns = ['spend', 'revenue', 'roas', 'cpa', 'ctr']
        for col in numeric_columns:
            if col in export_df.columns:
                export_df[col] = export_df[col].round(2)
        
        return export_df
    
    def prepare_creative_export(self, creative_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare creative data for export"""
        export_df = creative_df.copy()
        
        # Round numeric columns
        numeric_columns = ['spend', 'revenue', 'ctr', 'frequency']
        for col in numeric_columns:
            if col in export_df.columns:
                export_df[col] = export_df[col].round(2)
        
        return export_df
    
    def prepare_persona_export(self, persona_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare persona data for export"""
        export_df = persona_df.copy()
        
        # Round numeric columns
        numeric_columns = ['lifetime_value', 'avg_order_value', 'purchase_frequency', 'conversion_rate']
        for col in numeric_columns:
            if col in export_df.columns:
                export_df[col] = export_df[col].round(2)
        
        return export_df
    
    def create_summary_stats(self, campaign_df: pd.DataFrame) -> Dict[str, Any]:
        """Create summary statistics for export"""
        return {
            'total_spend': campaign_df['spend'].sum(),
            'total_revenue': campaign_df['revenue'].sum(),
            'total_conversions': campaign_df['conversions'].sum(),
            'avg_roas': (campaign_df['revenue'].sum() / campaign_df['spend'].sum()) if campaign_df['spend'].sum() > 0 else 0,
            'date_range': {
                'start': campaign_df['date'].min(),
                'end': campaign_df['date'].max()
            },
            'campaigns_count': campaign_df['campaign_name'].nunique(),
            'platforms_count': campaign_df['platform'].nunique()
        }
