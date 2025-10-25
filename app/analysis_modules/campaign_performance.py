import sqlite3, pandas as pd
from config import DB_PATH

def get_db_connection(): return sqlite3.connect(DB_PATH)

def fetch_performance_data(start_date: str, end_date: str, platforms: list, campaigns: list) -> pd.DataFrame:
    conn = get_db_connection()
    query = "SELECT dp.report_date, c.platform, c.campaign_name, dp.impressions, dp.clicks, dp.spend, dp.conversions, dp.revenue FROM daily_performance dp JOIN campaigns c ON dp.campaign_id = c.campaign_id WHERE dp.report_date BETWEEN ? AND ?"
    params = [start_date, end_date]
    if platforms: query += f" AND c.platform IN ({','.join(['?']*len(platforms))})"; params.extend(platforms)
    if campaigns: query += f" AND c.campaign_name IN ({','.join(['?']*len(campaigns))})"; params.extend(campaigns)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_campaign_list() -> list:
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT DISTINCT campaign_name FROM campaigns ORDER BY campaign_name", conn)
    conn.close()
    return df['campaign_name'].tolist()