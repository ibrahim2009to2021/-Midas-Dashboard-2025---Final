import sqlite3
import os
import sys
import bcrypt

# --- THIS BLOCK FIXES THE PATH FOR THIS SCRIPT ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --- END OF FIX ---
from config import DB_PATH

SCHEMA_FILE = 'schema.sql'

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt for secure storage.
    This method is consistent across deployments.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_database():
    """Creates the database and tables from the schema file."""
    schema_path = os.path.join(os.path.dirname(__file__), SCHEMA_FILE)
    
    if not os.path.exists(schema_path):
        print(f"❌ Schema file not found at: {schema_path}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.close()
    print("✅ Tables created or verified successfully.")

def populate_sample_data():
    """Populates the database with all sample data, including a correctly hashed admin user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # (Keep all existing data for campaigns, ads, budgets, etc.)
    campaigns_data = [
        ('META_C01', 'Fall Collection Showcase - TOF', 'Meta', 'Awareness', 'TOF'), 
        ('GOOG_C02', 'Modern Living Room Search - BOF', 'Google', 'Sales', 'BOF'), 
        ('TIKTOK_C03', 'Dorm Room Decor - MOF', 'TikTok', 'Consideration', 'MOF'), 
        ('SNAP_C04', 'AR Sofa Preview - TOF', 'Snapchat', 'Awareness', 'TOF')
    ]
    
    ad_sets_data = [
        ('META_AS01', 'US-25-45-Interest:InteriorDesign', 'META_C01', '{}'), 
        ('GOOG_AS02', 'Keyword: "buy leather sofa"', 'GOOG_C02', '{}'), 
        ('TIKTOK_AS03', 'US-18-24-Hashtag:CollegeLife', 'TIKTOK_C03', '{}'), 
        ('SNAP_AS04', 'US-16-22-LensUsers', 'SNAP_C04', '{}')
    ]
    
    ads_data = [
        ('META_AD01', 'Elegant Sofa Video Ad', 'META_AS01', 'Video', '', 'Modern Living, Timeless Comfort', 'Discover our new fall collection.', None), 
        ('GOOG_AD02', 'Leather Sofa Search Ad', 'GOOG_AS02', 'Image', '', 'Premium Leather Sofas', 'Shop now and get free delivery.', None), 
        ('TIKTOK_AD03', '5-Second Room Makeover', 'TIKTOK_AS03', 'Video', '', 'Upgrade Your Space!', '#dormdecor #midasfurniture', None), 
        ('SNAP_AD04', 'Place our couch in your room!', 'SNAP_AS04', 'AR Lens', '', 'Try Before You Buy', 'Use our AR lens to see it live.', None), 
        ('META_AD05_A', 'A/B Test Ad - Blue BG', 'META_AS01', 'Image', '', 'New Sofa, New Vibe.', 'Click to see our vibrant colors!', 'TEST01'), 
        ('META_AD05_B', 'A/B Test Ad - Green BG', 'META_AS01', 'Image', '', 'Your Perfect Sofa Awaits.', 'Find your perfect match today!', 'TEST01')
    ]
    
    budgets_data = [
        ('META_C01', '2025-10-01', '2025-10-31', 10000.0)
    ]
    
    ab_tests_data = [
        ('TEST01', 'Blue vs Green Background', 'Test if a green background improves CTR over blue.', '2025-10-01', '2025-10-31')
    ]
        
    try:
        cursor.executemany("INSERT OR IGNORE INTO campaigns VALUES (?, ?, ?, ?, ?)", campaigns_data)
        cursor.executemany("INSERT OR IGNORE INTO ad_sets VALUES (?, ?, ?, ?)", ad_sets_data)
        cursor.executemany("INSERT OR IGNORE INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ads_data)
        cursor.executemany("INSERT OR IGNORE INTO campaign_budgets (campaign_id, start_date, end_date, total_budget) VALUES (?, ?, ?, ?)", budgets_data)
        cursor.executemany("INSERT OR IGNORE INTO ab_tests VALUES (?, ?, ?, ?, ?)", ab_tests_data)
        
        # Populate Roles, Users, and Permissions
        roles_data = [('Admin',), ('Viewer',)]
        cursor.executemany("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", roles_data)
        
        # Generate a hashed password for 'admin123' using bcrypt directly
        print("🔐 Hashing admin password with bcrypt...")
        hashed_password = hash_password('admin123')
        print(f"✅ Password hashed successfully (length: {len(hashed_password)})")
        
        users_data = [('admin', 'Admin User', hashed_password, 1)]  # role_id 1 is Admin
        cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", users_data)
        
        admin_permissions = [
            (1, 'Segmentation_Analysis'), 
            (1, 'Predictive_Analytics'), 
            (1, 'Campaign_Takeaways'), 
            (1, 'Live_Benchmarking'), 
            (1, 'Creative_Analysis'), 
            (1, 'Budget_Pacing'), 
            (1, 'Persona_Intelligence'), 
            (1, 'AB_Testing'), 
            (1, 'Admin')
        ]
        
        viewer_permissions = [
            (2, 'Live_Benchmarking'), 
            (2, 'Creative_Analysis')
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO role_permissions (role_id, page_name) VALUES (?, ?)", admin_permissions)
        cursor.executemany("INSERT OR IGNORE INTO role_permissions (role_id, page_name) VALUES (?, ?)", viewer_permissions)
        
        conn.commit()
        print("✅ Sample data, roles, and permissions populated.")
        
    except sqlite3.Error as e:
        print(f"❌ Error populating data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  Removed existing database")
    
    print("🚀 Setting up the database...")
    create_database()
    populate_sample_data()
    print("✅ Database setup complete.")