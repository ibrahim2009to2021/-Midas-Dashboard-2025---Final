import pandas as pd, sqlite3
from config import DB_PATH
from datetime import date

def fetch_creative_performance(start_date: str, end_date: str):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT a.ad_id, a.ad_name, c.platform, a.creative_type, a.headline_text, SUM(dp.spend) as total_spend, SUM(dp.revenue) as total_revenue, SUM(dp.impressions) as total_impressions, SUM(dp.clicks) as total_clicks, SUM(dp.conversions) as total_conversions, AVG(dp.frequency) as avg_frequency FROM daily_performance dp JOIN ads a ON dp.ad_id = a.ad_id JOIN campaigns c ON dp.campaign_id = c.campaign_id WHERE dp.report_date BETWEEN ? AND ? GROUP BY a.ad_id, a.ad_name, c.platform, a.creative_type, a.headline_text"
    df = pd.read_sql_query(query, conn, params=[start_date, end_date])
    conn.close()
    if df.empty: return pd.DataFrame()
    df['roas'] = (df['total_revenue'] / df['total_spend']).where(df['total_spend'] > 0, 0)
    df['cpa'] = (df['total_spend'] / df['total_conversions']).where(df['total_conversions'] > 0, 0)
    df['ctr'] = (df['total_clicks'] / df['total_impressions']).where(df['total_impressions'] > 0, 0)
    df['fatigue_warning'] = (df['avg_frequency'] > 3) & (df['ctr'] < df['ctr'].quantile(0.4))
    return df

def generate_recommendations(df: pd.DataFrame, cpa_target: float):
    recs, today = [], date.today().strftime('%Y-%m-%d')
    for _, row in df[df['cpa'] > (cpa_target * 1.5)].iterrows():
        recs.append({'generation_date': today, 'ad_id': row['ad_id'], 'recommendation_type': 'Pause Ad', 'justification': f"High CPA: ${row['cpa']:.2f} is >150% of ${cpa_target:.2f} target."})
    for _, row in df[df['fatigue_warning'] == True].iterrows():
        recs.append({'generation_date': today, 'ad_id': row['ad_id'], 'recommendation_type': 'Creative Fatigue', 'justification': f"High Frequency ({row['avg_frequency']:.1f}) and low CTR ({row['ctr']:.2%})."})
    return recs

def save_recommendations(recs: list):
    if not recs: return
    conn = sqlite3.connect(DB_PATH)
    pd.DataFrame(recs).to_sql('recommendations', conn, if_exists='append', index=False)
    conn.close()