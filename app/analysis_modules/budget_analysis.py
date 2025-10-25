import pandas as pd, sqlite3
from config import DB_PATH
from datetime import datetime

def get_budget_pacing(campaign_id: str):
    conn = sqlite3.connect(DB_PATH)
    budget_df = pd.read_sql_query("SELECT start_date, end_date, total_budget FROM campaign_budgets WHERE campaign_id = ?", conn, params=[campaign_id])
    if budget_df.empty: return None
    spend_df = pd.read_sql_query("SELECT SUM(spend) as total_spend FROM daily_performance WHERE campaign_id = ?", conn, params=[campaign_id])
    conn.close()
    budget_info, total_spend = budget_df.iloc[0], spend_df['total_spend'].iloc[0] or 0
    start_date, end_date, today = datetime.strptime(budget_info['start_date'], '%Y-%m-%d').date(), datetime.strptime(budget_info['end_date'], '%Y-%m-%d').date(), datetime.now().date()
    total_days, days_elapsed = (end_date - start_date).days + 1, (today - start_date).days
    time_elapsed_pct = min(days_elapsed / total_days, 1.0) if total_days > 0 else 1.0
    budget_spent_pct = total_spend / budget_info['total_budget'] if budget_info['total_budget'] > 0 else 0
    ideal_spend = budget_info['total_budget'] * time_elapsed_pct
    pacing = (total_spend / ideal_spend) if ideal_spend > 0 else 0
    return {'total_budget': budget_info['total_budget'], 'total_spend': total_spend, 'time_elapsed_pct': time_elapsed_pct, 'budget_spent_pct': budget_spent_pct, 'pacing': pacing}