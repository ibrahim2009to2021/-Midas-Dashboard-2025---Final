"""
Admin Page
"""
import streamlit as st
import sys
sys.path.append('/mnt/user-data/outputs/FINAL_SYSTEM')

st.set_page_config(page_title="Admin", page_icon="👑", layout="wide")

try:
    from admin_page import render_admin_page
    render_admin_page()
except ImportError:
    st.title("👑 Admin Dashboard")
    st.warning("⚠️ Admin module not found")
    st.markdown("""
    ### Setup Required
    
    To enable the full Admin panel:
    1. Ensure `admin_page.py` exists in project root
    2. Restart the app
    
    The Admin panel includes:
    - 👥 User Management
    - ⚙️ System Settings
    - 📊 Usage Analytics
    """)
