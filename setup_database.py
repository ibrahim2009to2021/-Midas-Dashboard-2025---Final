"""
One-Time Database Setup Script
================================

This script initializes the Midas Furniture Dashboard database with:
- Database schema (tables, relationships)
- Sample campaign data (Meta, Google, TikTok, Snapchat)
- Sample ads and performance data
- Admin user account
- Role-based access control

USAGE:
------
Run this script ONCE after deployment:

    python setup_database.py

DEFAULT ADMIN CREDENTIALS:
--------------------------
Username: admin
Password: admin123

IMPORTANT:
----------
- Only run this script ONCE to initialize the database
- To reset the database, delete 'furniture.db' and run this script again
- Change the default admin password immediately after first login
"""

import sys
import os
from datetime import datetime, timedelta

# Add project to path
sys.path.append(os.path.dirname(__file__))

try:
    from database.db_setup import create_database, populate_sample_data
    from config import DB_PATH
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you have created the 'database' folder and 'config.py' file")
    sys.exit(1)


def check_database_exists():
    """Check if database already exists"""
    if os.path.exists(DB_PATH):
        return True
    return False


def display_banner():
    """Display setup banner"""
    print("=" * 70)
    print("  🛋️  MIDAS FURNITURE DASHBOARD - DATABASE SETUP")
    print("=" * 70)
    print()


def display_summary():
    """Display setup summary"""
    print()
    print("=" * 70)
    print("  ✅ DATABASE SETUP COMPLETE!")
    print("=" * 70)
    print()
    print("📊 Database Created: furniture.db")
    print()
    print("📦 Sample Data Loaded:")
    print("   • 4 Campaigns (Meta, Google, TikTok, Snapchat)")
    print("   • 6 Sample Ads")
    print("   • A/B Test Campaign")
    print("   • Role-Based Access Control")
    print()
    print("👤 Default Admin User:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
    print()
    print("🚀 Next Steps:")
    print("   1. Run your dashboard: streamlit run dashboard.py")
    print("   2. Login with admin credentials")
    print("   3. Go to Admin page and change password")
    print()
    print("=" * 70)


def main():
    """Main setup function"""
    
    display_banner()
    
    # Check if database already exists
    if check_database_exists():
        print(f"⚠️  WARNING: Database '{DB_PATH}' already exists!")
        print()
        response = input("Do you want to DELETE and recreate it? (yes/no): ").lower()
        
        if response == 'yes':
            try:
                os.remove(DB_PATH)
                print(f"🗑️  Deleted existing database: {DB_PATH}")
                print()
            except Exception as e:
                print(f"❌ Error deleting database: {e}")
                sys.exit(1)
        else:
            print("❌ Setup cancelled. Database was not modified.")
            sys.exit(0)
    
    # Step 1: Create database schema
    print("📋 Step 1/2: Creating database schema...")
    try:
        create_database()
        print("   ✅ Database schema created successfully")
    except Exception as e:
        print(f"   ❌ Error creating schema: {e}")
        sys.exit(1)
    
    print()
    
    # Step 2: Populate with sample data
    print("📊 Step 2/2: Populating with sample data...")
    try:
        populate_sample_data()
        print("   ✅ Sample data loaded successfully")
    except Exception as e:
        print(f"   ❌ Error loading sample data: {e}")
        sys.exit(1)
    
    # Display summary
    display_summary()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)