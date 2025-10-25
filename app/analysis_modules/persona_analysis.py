import pandas as pd, sqlite3
from config import DB_PATH
from datetime import datetime

def calculate_rfm():
    conn = sqlite3.connect(DB_PATH)
    sales_df = pd.read_sql_query("SELECT customer_id, sale_date, sale_amount FROM sales", conn)
    conn.close()
    if sales_df.empty: return pd.DataFrame()
    snapshot_date = datetime.strptime(sales_df['sale_date'].max(), '%Y-%m-%d') + pd.DateOffset(days=1)
    sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
    rfm = sales_df.groupby('customer_id').agg({'sale_date': lambda date: (snapshot_date - date.max()).days, 'sale_id': 'count', 'sale_amount': 'sum'}).rename(columns={'sale_date': 'Recency', 'sale_id': 'Frequency', 'sale_amount': 'Monetary'})
    rfm['R_Score'], rfm['F_Score'], rfm['M_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1]), pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]), pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    segment_map = {r'[3-4][3-4][3-4]': 'Champions', r'[2-4][1-2][3-4]': 'Potential Loyalists', r'[3-4][1-2][1-2]': 'New Customers', r'[1-2][3-4][3-4]': 'At Risk', r'1[1-2][1-2]': 'Hibernating'}
    rfm['Segment'] = rfm['RFM_Score'].replace(segment_map, regex=True)
    return rfm