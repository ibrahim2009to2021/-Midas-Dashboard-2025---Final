"""
File Upload Module for Campaign Data
Handles validation and insertion of CSV/Excel data into the database
"""

import pandas as pd
import sqlite3
from datetime import datetime
from config import DB_PATH
from io import StringIO

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_daily_performance_data(df: pd.DataFrame) -> tuple:
    """
    Validate daily performance data from CSV/Excel.
    
    Returns:
        tuple: (is_valid: bool, message: str, validated_df: pd.DataFrame or None)
    """
    # Required columns
    required_cols = [
        'report_date', 'ad_id', 'campaign_id', 
        'impressions', 'clicks', 'spend', 'conversions', 'revenue'
    ]
    
    # Check for missing columns
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}", None
    
    # Create a copy for validation
    validated_df = df.copy()
    
    # Validate date format
    try:
        validated_df['report_date'] = pd.to_datetime(validated_df['report_date']).dt.strftime('%Y-%m-%d')
    except Exception as e:
        return False, f"Invalid date format in 'report_date'. Use YYYY-MM-DD format. Error: {str(e)}", None
    
    # Validate numeric columns
    numeric_cols = ['impressions', 'clicks', 'spend', 'conversions', 'revenue']
    for col in numeric_cols:
        if col in validated_df.columns:
            try:
                validated_df[col] = pd.to_numeric(validated_df[col], errors='coerce')
                if validated_df[col].isna().any():
                    return False, f"Non-numeric values found in column '{col}'", None
            except Exception as e:
                return False, f"Error validating column '{col}': {str(e)}", None
    
    # Fill optional columns with defaults if missing
    optional_cols = {
        'reach': 0,
        'frequency': 1.0,
        'video_views': 0,
        'add_to_carts': 0
    }
    
    for col, default_value in optional_cols.items():
        if col not in validated_df.columns:
            validated_df[col] = default_value
    
    # Check if campaign_ids and ad_ids exist in database
    conn = sqlite3.connect(DB_PATH)
    existing_campaigns = pd.read_sql_query("SELECT campaign_id FROM campaigns", conn)['campaign_id'].tolist()
    existing_ads = pd.read_sql_query("SELECT ad_id FROM ads", conn)['ad_id'].tolist()
    conn.close()
    
    invalid_campaigns = validated_df[~validated_df['campaign_id'].isin(existing_campaigns)]['campaign_id'].unique()
    if len(invalid_campaigns) > 0:
        return False, f"Campaign IDs not found in database: {', '.join(map(str, invalid_campaigns))}", None
    
    invalid_ads = validated_df[~validated_df['ad_id'].isin(existing_ads)]['ad_id'].unique()
    if len(invalid_ads) > 0:
        return False, f"Ad IDs not found in database: {', '.join(map(str, invalid_ads))}", None
    
    return True, f"Validation successful! {len(validated_df)} rows ready to upload.", validated_df


def validate_segmented_data(df: pd.DataFrame) -> tuple:
    """
    Validate segmented performance data from CSV/Excel.
    
    Returns:
        tuple: (is_valid: bool, message: str, validated_df: pd.DataFrame or None)
    """
    required_cols = [
        'report_date', 'ad_id', 'campaign_id', 
        'segment_type', 'segment_value',
        'impressions', 'clicks', 'spend', 'conversions', 'revenue'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}", None
    
    validated_df = df.copy()
    
    # Validate date format
    try:
        validated_df['report_date'] = pd.to_datetime(validated_df['report_date']).dt.strftime('%Y-%m-%d')
    except Exception as e:
        return False, f"Invalid date format. Error: {str(e)}", None
    
    # Validate numeric columns
    numeric_cols = ['impressions', 'clicks', 'spend', 'conversions', 'revenue']
    for col in numeric_cols:
        try:
            validated_df[col] = pd.to_numeric(validated_df[col], errors='coerce')
            if validated_df[col].isna().any():
                return False, f"Non-numeric values in '{col}'", None
        except Exception as e:
            return False, f"Error validating '{col}': {str(e)}", None
    
    # Check foreign keys
    conn = sqlite3.connect(DB_PATH)
    existing_campaigns = pd.read_sql_query("SELECT campaign_id FROM campaigns", conn)['campaign_id'].tolist()
    existing_ads = pd.read_sql_query("SELECT ad_id FROM ads", conn)['ad_id'].tolist()
    conn.close()
    
    invalid_campaigns = validated_df[~validated_df['campaign_id'].isin(existing_campaigns)]['campaign_id'].unique()
    if len(invalid_campaigns) > 0:
        return False, f"Invalid campaign IDs: {', '.join(map(str, invalid_campaigns))}", None
    
    invalid_ads = validated_df[~validated_df['ad_id'].isin(existing_ads)]['ad_id'].unique()
    if len(invalid_ads) > 0:
        return False, f"Invalid ad IDs: {', '.join(map(str, invalid_ads))}", None
    
    return True, f"Validation successful! {len(validated_df)} rows ready to upload.", validated_df


def validate_country_data(df: pd.DataFrame) -> tuple:
    """
    Validate country performance data from CSV/Excel.
    
    Returns:
        tuple: (is_valid: bool, message: str, validated_df: pd.DataFrame or None)
    """
    required_cols = [
        'report_date', 'platform', 'country',
        'impressions', 'clicks', 'spend', 'conversions', 'revenue'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}", None
    
    validated_df = df.copy()
    
    # Validate date format
    try:
        validated_df['report_date'] = pd.to_datetime(validated_df['report_date']).dt.strftime('%Y-%m-%d')
    except Exception as e:
        return False, f"Invalid date format. Error: {str(e)}", None
    
    # Validate platform values
    valid_platforms = ['Meta', 'Google', 'TikTok', 'Snapchat']
    invalid_platforms = validated_df[~validated_df['platform'].isin(valid_platforms)]['platform'].unique()
    if len(invalid_platforms) > 0:
        return False, f"Invalid platforms: {', '.join(map(str, invalid_platforms))}. Valid values: {', '.join(valid_platforms)}", None
    
    # Validate numeric columns
    numeric_cols = ['impressions', 'clicks', 'spend', 'conversions', 'revenue']
    for col in numeric_cols:
        try:
            validated_df[col] = pd.to_numeric(validated_df[col], errors='coerce')
            if validated_df[col].isna().any():
                return False, f"Non-numeric values in '{col}'", None
        except Exception as e:
            return False, f"Error validating '{col}': {str(e)}", None
    
    return True, f"Validation successful! {len(validated_df)} rows ready to upload.", validated_df


# ============================================================================
# DATABASE INSERTION FUNCTIONS
# ============================================================================

def insert_daily_performance(df: pd.DataFrame) -> tuple:
    """
    Insert daily performance data into the database.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        inserted_count = 0
        skipped_count = 0
        
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO daily_performance 
                    (report_date, ad_id, campaign_id, impressions, reach, frequency, 
                     clicks, spend, video_views, add_to_carts, conversions, revenue)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['report_date'], row['ad_id'], row['campaign_id'],
                    int(row['impressions']), int(row.get('reach', 0)), float(row.get('frequency', 1.0)),
                    int(row['clicks']), float(row['spend']), 
                    int(row.get('video_views', 0)), int(row.get('add_to_carts', 0)),
                    int(row['conversions']), float(row['revenue'])
                ))
                inserted_count += 1
            except sqlite3.IntegrityError:
                # Skip duplicate records (same date + ad_id)
                skipped_count += 1
                continue
        
        conn.commit()
        conn.close()
        
        message = f"Successfully inserted {inserted_count} rows."
        if skipped_count > 0:
            message += f" Skipped {skipped_count} duplicate records."
        
        return True, message
        
    except Exception as e:
        return False, f"Database error: {str(e)}"


def insert_segmented_data(df: pd.DataFrame) -> tuple:
    """
    Insert segmented performance data into the database.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        inserted_count = 0
        skipped_count = 0
        
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO performance_by_segment 
                    (report_date, ad_id, campaign_id, segment_type, segment_value,
                     impressions, clicks, spend, conversions, revenue)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['report_date'], row['ad_id'], row['campaign_id'],
                    row['segment_type'], row['segment_value'],
                    int(row['impressions']), int(row['clicks']), float(row['spend']),
                    int(row['conversions']), float(row['revenue'])
                ))
                inserted_count += 1
            except sqlite3.IntegrityError:
                skipped_count += 1
                continue
        
        conn.commit()
        conn.close()
        
        message = f"Successfully inserted {inserted_count} rows."
        if skipped_count > 0:
            message += f" Skipped {skipped_count} duplicate records."
        
        return True, message
        
    except Exception as e:
        return False, f"Database error: {str(e)}"


def insert_country_data(df: pd.DataFrame) -> tuple:
    """
    Insert country performance data into the database.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        inserted_count = 0
        skipped_count = 0
        
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO performance_by_country 
                    (report_date, platform, country, impressions, clicks, 
                     spend, conversions, revenue)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['report_date'], row['platform'], row['country'],
                    int(row['impressions']), int(row['clicks']), float(row['spend']),
                    int(row['conversions']), float(row['revenue'])
                ))
                inserted_count += 1
            except sqlite3.IntegrityError:
                skipped_count += 1
                continue
        
        conn.commit()
        conn.close()
        
        message = f"Successfully inserted {inserted_count} rows."
        if skipped_count > 0:
            message += f" Skipped {skipped_count} duplicate records."
        
        return True, message
        
    except Exception as e:
        return False, f"Database error: {str(e)}"


# ============================================================================
# TEMPLATE GENERATION
# ============================================================================

def generate_template_csv(data_type: str) -> str:
    """
    Generate CSV template for different data types.
    
    Args:
        data_type: One of 'daily_performance', 'segmented', 'country'
    
    Returns:
        str: CSV content as string
    """
    if data_type == "daily_performance":
        template_data = {
            'report_date': ['2025-10-20'],
            'ad_id': ['META_AD01'],
            'campaign_id': ['META_C01'],
            'impressions': [10000],
            'reach': [8000],
            'frequency': [1.25],
            'clicks': [150],
            'spend': [250.50],
            'video_views': [500],
            'add_to_carts': [10],
            'conversions': [5],
            'revenue': [1250.00]
        }
    
    elif data_type == "segmented":
        template_data = {
            'report_date': ['2025-10-20'],
            'ad_id': ['META_AD01'],
            'campaign_id': ['META_C01'],
            'segment_type': ['Age'],
            'segment_value': ['25-34'],
            'impressions': [5000],
            'clicks': [75],
            'spend': [125.25],
            'conversions': [3],
            'revenue': [625.00]
        }
    
    elif data_type == "country":
        template_data = {
            'report_date': ['2025-10-20'],
            'platform': ['Meta'],
            'country': ['KSA'],
            'impressions': [20000],
            'clicks': [300],
            'spend': [500.00],
            'conversions': [15],
            'revenue': [3000.00]
        }
    
    else:
        return ""
    
    df = pd.DataFrame(template_data)
    return df.to_csv(index=False)