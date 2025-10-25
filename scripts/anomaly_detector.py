import pandas as pd
import sqlite3
from config import DB_PATH
from datetime import date, timedelta

def run_anomaly_detection():
    print("Running anomaly detection...")
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT report_date, ad_id, spend, conversions FROM daily_performance WHERE report_date >= '{(date.today() - timedelta(days=8)).strftime('%Y-%m-%d')}'"
    df = pd.read_sql_query(query, conn)
    if df.empty: conn.close(); return

    df['cpa'] = df['spend'] / df['conversions'].replace(0, 1)
    yesterday_str, alerts = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), []
    yesterday_data = df[df['report_date'] == yesterday_str]
    historical_data = df[df['report_date'] < yesterday_str]
    
    for ad in yesterday_data['ad_id'].unique():
        ad_yesterday = yesterday_data[yesterday_data['ad_id'] == ad]
        ad_historical = historical_data[historical_data['ad_id'] == ad]
        if ad_historical.empty: continue
        avg_hist_cpa, yesterday_cpa = ad_historical['cpa'].mean(), ad_yesterday['cpa'].iloc[0]
        if yesterday_cpa > (avg_hist_cpa * 2) and yesterday_cpa > 5:
            alerts.append({'alert_date': date.today(), 'metric': 'High CPA', 'ad_id': ad, 'justification': f"Yesterday's CPA (${yesterday_cpa:.2f}) is >200% of 7-day avg (${avg_hist_cpa:.2f})."})
    
    if alerts:
        pd.DataFrame(alerts).to_sql('alerts', conn, if_exists='append', index=False)
        print(f"Detected and saved {len(alerts)} new anomalies.")
    else:
        print("No anomalies detected.")
    conn.close()

if __name__ == '__main__':
    run_anomaly_detection()