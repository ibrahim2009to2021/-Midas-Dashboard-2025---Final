import sqlite3
import pandas as pd
from datetime import date, timedelta
import os
import sys

# --- THIS BLOCK FIXES THE PATH FOR THIS SCRIPT ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --- END OF FIX ---

from config import DB_PATH
from database.db_setup import create_database, populate_sample_data
from app.data_integration.api_connectors import (
    fetch_meta_data, fetch_google_data, fetch_tiktok_data, fetch_snapchat_data,
    fetch_country_data, fetch_meta_segmented_data, fetch_google_segmented_data,
    fetch_tiktok_segmented_data, fetch_snapchat_segmented_data, fetch_customer_sales_data
)

def get_db_connection():
    """Get a connection to the database."""
    return sqlite3.connect(DB_PATH)

def run_ingestion_for_date(run_date_str: str, conn):
    """
    Fetches and saves data for a specific date using an existing connection.
    
    Args:
        run_date_str: Date string in 'YYYY-MM-DD' format
        conn: SQLite database connection
    """
    try:
        print(f"📊 Fetching data for {run_date_str}...")
        
        all_platform_data = pd.concat([
            fetch_meta_data(run_date_str, run_date_str), 
            fetch_google_data(run_date_str, run_date_str), 
            fetch_tiktok_data(run_date_str, run_date_str), 
            fetch_snapchat_data(run_date_str, run_date_str)
        ], ignore_index=True)
        
        all_segmented_data = pd.concat([
            fetch_meta_segmented_data(run_date_str, run_date_str), 
            fetch_google_segmented_data(run_date_str, run_date_str), 
            fetch_tiktok_segmented_data(run_date_str, run_date_str), 
            fetch_snapchat_segmented_data(run_date_str, run_date_str)
        ], ignore_index=True)
        
        country_df = fetch_country_data(run_date_str, run_date_str)
        sales_df = fetch_customer_sales_data(run_date_str)

        if not all_platform_data.empty: 
            all_platform_data.to_sql('daily_performance', conn, if_exists='append', index=False)
            print(f"✅ Saved {len(all_platform_data)} platform performance records")
            
        if not all_segmented_data.empty: 
            all_segmented_data.to_sql('performance_by_segment', conn, if_exists='append', index=False)
            print(f"✅ Saved {len(all_segmented_data)} segmented performance records")
            
        if not country_df.empty: 
            country_df.to_sql('performance_by_country', conn, if_exists='append', index=False)
            print(f"✅ Saved {len(country_df)} country performance records")
            
        if not sales_df.empty:
            sales_df.to_sql('sales', conn, if_exists='append', index=False)
            print(f"✅ Saved {len(sales_df)} sales records")
            
            unique_customers = pd.DataFrame({
                'customer_id': sales_df['customer_id'].unique(), 
                'first_seen_date': run_date_str
            })
            unique_customers.to_sql('new_cust', conn, if_exists='replace', index=False)
            
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO customers (customer_id, first_seen_date) "
                "SELECT customer_id, first_seen_date FROM new_cust "
                "WHERE customer_id NOT IN (SELECT customer_id FROM customers)"
            )
            conn.commit()
            print(f"✅ Updated customers table")
            
    except Exception as e:
        print(f"❌ An error occurred during data ingestion for {run_date_str}: {e}")
        raise

def run_full_setup(progress_bar):
    """
    Executes the entire database creation and data population process.
    
    Args:
        progress_bar: Streamlit progress bar object for UI updates
    """
    try:
        # Step 1: Create database schema
        print("🏗️  Creating database schema...")
        create_database()
        progress_bar.progress(10, text="Database schema created.")
        
        # Step 2: Populate base data
        print("📝 Populating base data and users...")
        populate_sample_data()  # This now creates the correctly hashed admin user
        progress_bar.progress(20, text="Base data and users populated.")
        
        # Step 3: Ingest performance data
        print("📊 Ingesting sample performance data...")
        conn = get_db_connection()
        
        try:
            yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            progress_bar.progress(50, text=f"Fetching data for {yesterday}...")
            
            run_ingestion_for_date(yesterday, conn)
            progress_bar.progress(90, text="Sample performance data ingested.")
            
        finally:
            conn.close()
        
        # Step 4: Complete
        progress_bar.progress(100, text="Setup complete! The app will now reload.")
        print("✅ Full setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        progress_bar.progress(0, text=f"Setup failed: {e}")
        raise