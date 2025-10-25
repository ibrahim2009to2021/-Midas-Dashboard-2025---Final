import sqlite3, pandas as pd
from config import DB_PATH

def fetch_data_by_segment(start_date: str, end_date: str, platform: str, segment_type: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT segment_value, SUM(spend) as total_spend, SUM(revenue) as total_revenue, SUM(impressions) as total_impressions, SUM(clicks) as total_clicks, SUM(conversions) as total_conversions FROM performance_by_segment ps JOIN campaigns c ON ps.campaign_id = c.campaign_id WHERE ps.report_date BETWEEN ? AND ? AND c.platform = ? AND ps.segment_type = ? GROUP BY segment_value ORDER BY total_spend DESC"
    df = pd.read_sql_query(query, conn, params=[start_date, end_date, platform, segment_type])
    conn.close()
    if df.empty: return pd.DataFrame()
    df['roas'] = (df['total_revenue'] / df['total_spend']).where(df['total_spend'] > 0, 0)
    df['cpa'] = (df['total_spend'] / df['total_conversions']).where(df['total_conversions'] > 0, 0)
    df['ctr'] = (df['total_clicks'] / df['total_impressions']).where(df['total_impressions'] > 0, 0)
    return df