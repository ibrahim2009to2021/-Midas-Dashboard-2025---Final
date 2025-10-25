import pandas as pd, sqlite3
from config import DB_PATH

BENCHMARKS = {'ROAS': {'target': 4.5}, 'CTR': {'target': 0.018}, 'CPA': {'target': 35.0}}

def fetch_benchmark_data(start_date: str, end_date: str, countries: list, platforms: list) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query, params = "SELECT country, SUM(spend) as spend, SUM(revenue) as revenue, SUM(impressions) as impressions, SUM(clicks) as clicks, SUM(conversions) as conversions FROM performance_by_country WHERE report_date BETWEEN ? AND ?", [start_date, end_date]
    if countries: query += f" AND country IN ({','.join(['?']*len(countries))})"; params.extend(countries)
    if platforms: query += f" AND platform IN ({','.join(['?']*len(platforms))})"; params.extend(platforms)
    query += " GROUP BY country"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    if df.empty: return pd.DataFrame()
    df['ROAS'] = (df['revenue'] / df['spend']).where(df['spend'] > 0, 0)
    df['CTR'] = (df['clicks'] / df['impressions']).where(df['impressions'] > 0, 0)
    df['CPA'] = (df['spend'] / df['conversions']).where(df['conversions'] > 0, 0)
    return df