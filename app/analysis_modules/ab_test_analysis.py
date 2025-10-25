import pandas as pd, sqlite3
from config import DB_PATH
from scipy.stats import ttest_ind

def get_ab_test_results(test_id: str):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT a.ad_id, a.ad_name, SUM(dp.spend) as spend, SUM(dp.clicks) as clicks, SUM(dp.impressions) as impressions FROM daily_performance dp JOIN ads a ON dp.ad_id = a.ad_id WHERE a.test_id = ? GROUP BY a.ad_id, a.ad_name", conn, params=[test_id])
    daily_df = pd.read_sql_query("SELECT dp.report_date, a.ad_id, dp.clicks, dp.impressions FROM daily_performance dp JOIN ads a ON dp.ad_id = a.ad_id WHERE a.test_id = ?", conn, params=[test_id])
    conn.close()
    if df.empty or len(df) < 2: return None, None
    df['ctr'] = (df['clicks'] / df['impressions']).where(df['impressions'] > 0, 0)
    variants = daily_df['ad_id'].unique()
    variant_A_ctr = daily_df[daily_df['ad_id'] == variants[0]].apply(lambda r: r['clicks'] / r['impressions'] if r['impressions'] > 0 else 0, axis=1)
    variant_B_ctr = daily_df[daily_df['ad_id'] == variants[1]].apply(lambda r: r['clicks'] / r['impressions'] if r['impressions'] > 0 else 0, axis=1)
    stat, p_value = ttest_ind(variant_A_ctr, variant_B_ctr)
    return df, p_value