\# 🛋️ Midas Furniture Campaign Analytics Dashboard



A powerful, production-ready analytics platform for digital marketing campaigns across Meta, Google, TikTok, and Snapchat.



!\[Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-success)

!\[Python](https://img.shields.io/badge/Python-3.8+-blue)

!\[Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

!\[License](https://img.shields.io/badge/License-MIT-green)



---



\## 🎯 Overview



\*\*Midas Furniture Dashboard\*\* is a comprehensive analytics platform designed for digital marketing teams to track, analyze, and optimize multi-platform advertising campaigns. Built with Streamlit and SQLite, it provides real-time insights, user management, and data export capabilities.



\### ✨ Key Features



\- 📊 \*\*Multi-Platform Analytics\*\* - Track campaigns across Meta, Google, TikTok, and Snapchat

\- 🎨 \*\*Creative Performance Analysis\*\* - Monitor ad creative effectiveness and detect fatigue

\- 👥 \*\*Customer Segmentation\*\* - RFM analysis and persona intelligence

\- 💰 \*\*Budget Pacing\*\* - Real-time budget tracking with automated alerts

\- 🔬 \*\*A/B Testing\*\* - Statistical significance testing for ad variants

\- 📤 \*\*Data Export\*\* - CSV, Excel, and PDF export functionality

\- 👑 \*\*Admin Dashboard\*\* - User management with role-based access control

\- 🔐 \*\*Secure Authentication\*\* - Bcrypt password hashing and session management

\- 🤖 \*\*ML Predictions\*\* - Machine learning-powered conversion predictions (optional)

\- ⚠️ \*\*Anomaly Detection\*\* - Automated performance anomaly alerts (optional)



---



\## 🚀 Quick Start



\### Prerequisites



\- Python 3.8 or higher

\- Git

\- Streamlit Cloud account (for deployment) OR local Python environment



\### Installation



\#### Option 1: Deploy to Streamlit Cloud (Recommended)



1\. \*\*Fork/Clone this repository\*\*

&nbsp;  ```bash

&nbsp;  git clone https://github.com/yourusername/midas-furniture-dashboard-final.git

&nbsp;  cd midas-furniture-dashboard-final

&nbsp;  ```



2\. \*\*Connect to Streamlit Cloud\*\*

&nbsp;  - Go to \[Streamlit Cloud](https://streamlit.io/cloud)

&nbsp;  - Deploy from your GitHub repository

&nbsp;  - Wait for initial deployment



3\. \*\*Initialize Database\*\*

&nbsp;  ```bash

&nbsp;  # In Streamlit Cloud terminal OR locally:

&nbsp;  python setup\_database.py

&nbsp;  ```



4\. \*\*Access Your Dashboard\*\*

&nbsp;  - URL: `https://your-app-name.streamlit.app`

&nbsp;  - Login: `admin` / `admin123`

&nbsp;  - \*\*⚠️ Change default password immediately!\*\*



\#### Option 2: Run Locally



1\. \*\*Clone and Install\*\*

&nbsp;  ```bash

&nbsp;  git clone https://github.com/yourusername/midas-furniture-dashboard-final.git

&nbsp;  cd midas-furniture-dashboard-final

&nbsp;  pip install -r requirements.txt

&nbsp;  ```



2\. \*\*Initialize Database\*\*

&nbsp;  ```bash

&nbsp;  python setup\_database.py

&nbsp;  ```



3\. \*\*Run Dashboard\*\*

&nbsp;  ```bash

&nbsp;  streamlit run dashboard.py

&nbsp;  ```



4\. \*\*Access Dashboard\*\*

&nbsp;  - Open browser to `http://localhost:8501`

&nbsp;  - Login: `admin` / `admin123`



---



\## 📁 Project Structure



```

midas-furniture-dashboard-final/

├── dashboard.py                 # Main application

├── admin\_page.py               # User management interface

├── config.py                   # Configuration settings

├── setup\_database.py           # Database initialization script

├── requirements.txt            # Python dependencies

│

├── export/                     # Data export functionality

│   ├── \_\_init\_\_.py

│   ├── data\_exporter.py       # Export logic

│   └── export\_page.py         # Export UI

│

├── database/                   # Database layer

│   ├── schema.sql             # Database structure

│   ├── db\_setup.py            # Setup and population

│   └── base.py                # SQLAlchemy configuration

│

├── app/                        # Advanced modules (optional)

│   ├── analysis\_modules/      # Analysis engines

│   ├── data\_integration/      # API connectors

│   ├── predictive\_engine/     # ML models

│   └── ui\_components/         # UI widgets

│

└── scripts/                    # Automation scripts (optional)

&nbsp;   ├── app\_setup.py           # Full setup automation

&nbsp;   └── anomaly\_detector.py    # Automated anomaly detection

```



---



\## 🗄️ Database Schema



The dashboard uses SQLite with the following core tables:



\### Core Tables

\- \*\*campaigns\*\* - Campaign metadata (platform, objective, funnel stage)

\- \*\*ad\_sets\*\* - Ad set details with targeting criteria

\- \*\*ads\*\* - Individual ad creatives

\- \*\*daily\_performance\*\* - Daily metrics (spend, revenue, conversions, etc.)

\- \*\*performance\_by\_segment\*\* - Demographic breakdowns

\- \*\*performance\_by\_country\*\* - Geographic performance data



\### User Management

\- \*\*users\*\* - User accounts with hashed passwords

\- \*\*roles\*\* - User roles (Admin, Viewer, etc.)

\- \*\*role\_permissions\*\* - Page-level access control



\### Advanced Features

\- \*\*ab\_tests\*\* - A/B test definitions and results

\- \*\*campaign\_budgets\*\* - Budget tracking and pacing

\- \*\*customers\*\* - Customer profiles

\- \*\*sales\*\* - Transaction history

\- \*\*alerts\*\* - Automated anomaly alerts

\- \*\*recommendations\*\* - AI-generated optimization suggestions



---



\## 📊 Sample Data



After running `setup\_database.py`, you'll have:



\### Campaigns (4)

\- \*\*META\_C01\*\* - Fall Collection Showcase (Meta, TOF)

\- \*\*GOOG\_C02\*\* - Modern Living Room Search (Google, BOF)

\- \*\*TIKTOK\_C03\*\* - Dorm Room Decor (TikTok, MOF)

\- \*\*SNAP\_C04\*\* - AR Sofa Preview (Snapchat, TOF)



\### Ads (6)

\- 4 regular ads (one per platform)

\- 2 A/B test variants (Meta)



\### Users (1)

\- \*\*admin\*\* - Administrator with full access



---



\## 🔐 Security



\### Authentication

\- Bcrypt password hashing (cost factor: 12)

\- Session-based authentication

\- Role-based access control (RBAC)



\### Default Credentials

```

Username: admin

Password: admin123

```



\*\*⚠️ CRITICAL: Change the default password immediately after first login!\*\*



\### Changing Admin Password

1\. Login to dashboard

2\. Navigate to Admin page

3\. Click "Edit" on admin user

4\. Enter new password

5\. Save changes



---



\## ⚙️ Configuration



\### config.py Settings



```python

\# Database

DB\_PATH = 'furniture.db'



\# Performance Thresholds

ROAS\_TARGET = 2.5

CPA\_TARGET = 35.0

CTR\_TARGET = 1.8



\# Feature Flags

ENABLE\_ML\_PREDICTIONS = True

ENABLE\_ANOMALY\_DETECTION = True

ENABLE\_AUTO\_RECOMMENDATIONS = True

```



\### API Configuration (Optional)



For live data integration, add API credentials to Streamlit Secrets or environment variables:



```toml

\# .streamlit/secrets.toml

META\_ACCESS\_TOKEN = "your\_token\_here"

GOOGLE\_DEVELOPER\_TOKEN = "your\_token\_here"

TIKTOK\_ACCESS\_TOKEN = "your\_token\_here"

SNAPCHAT\_ACCESS\_TOKEN = "your\_token\_here"

```



---



\## 📖 User Guide



\### Dashboard Pages



\#### 📊 Dashboard

\- Overview of all campaigns

\- Key performance metrics (ROAS, CPA, conversions)

\- Revenue by platform

\- Daily ROAS trends

\- Top performing campaigns



\#### 👥 Segmentation Analysis

\- Customer segment distribution

\- Lifetime value by segment

\- Average order value analysis

\- Purchase frequency metrics



\#### 🎨 Creative Analysis

\- Ad creative performance

\- CTR and ROAS by format

\- Creative fatigue detection

\- Top performing creatives



\#### 💰 Budget Pacing

\- Campaign budget vs. spend

\- Time-based pacing analysis

\- Budget utilization alerts

\- Forecasted spend



\#### 🔬 A/B Testing

\- Statistical significance testing

\- Variant performance comparison

\- CTR and conversion analysis

\- Winner determination



\#### 📤 Export Data

\- CSV export (all data types)

\- Excel export with formatting

\- PDF report generation

\- Custom date ranges



\#### 👑 Admin Dashboard

\- User management (create, edit, delete)

\- Role assignment

\- Permission management

\- System settings



---



\## 🔧 Advanced Features (Optional)



\### Live API Integration



Connect real advertising platforms:



1\. Obtain API credentials from platforms

2\. Add credentials to `config.py` or Streamlit Secrets

3\. Uncomment API integrations in `requirements.txt`:

&nbsp;  ```txt

&nbsp;  facebook-business>=17.0.0

&nbsp;  google-ads>=22.0.0

&nbsp;  ```

4\. Use `app/data\_integration/api\_connectors.py` to fetch live data



\### Machine Learning



Enable ML-powered conversion predictions:



1\. Ensure `scikit-learn` is installed

2\. Run model training:

&nbsp;  ```bash

&nbsp;  python app/predictive\_engine/model\_trainer.py

&nbsp;  ```

3\. Set `ENABLE\_ML\_PREDICTIONS = True` in config.py



\### Automated Anomaly Detection



Set up daily anomaly detection:



1\. Configure anomaly thresholds in config.py

2\. Schedule daily runs:

&nbsp;  ```bash

&nbsp;  python scripts/anomaly\_detector.py

&nbsp;  ```

3\. View alerts in dashboard



---



\## 🐛 Troubleshooting



\### Common Issues



\#### Database Not Found

```

Error: No such file: furniture.db

```

\*\*Solution:\*\* Run `python setup\_database.py`



\#### Import Errors

```

ModuleNotFoundError: No module named 'config'

```

\*\*Solution:\*\* Ensure `config.py` exists in project root



\#### Login Fails

```

Invalid credentials

```

\*\*Solution:\*\* 

\- Verify exact credentials: `admin` / `admin123`

\- Delete `furniture.db` and re-run setup

\- Check bcrypt is installed



\#### Missing Dependencies

```

ModuleNotFoundError: No module named 'bcrypt'

```

\*\*Solution:\*\* 

\- Update `requirements.txt`

\- Run `pip install -r requirements.txt`



---



\## 📈 Performance



\### Optimizations

\- ✅ Data caching with `@st.cache\_data` (1-hour TTL)

\- ✅ Efficient SQL queries with proper indexes

\- ✅ Lazy loading of advanced modules

\- ✅ Optimized chart rendering with Plotly



\### Scalability

\- \*\*Current:\*\* Handles 100K+ daily performance records

\- \*\*Database:\*\* SQLite suitable for <100GB data

\- \*\*Upgrade Path:\*\* Easy migration to PostgreSQL/MySQL if needed



---



\## 🔄 Updating



\### Adding New Campaigns

1\. Use Admin panel to add campaigns

2\. OR insert directly into database:

&nbsp;  ```sql

&nbsp;  INSERT INTO campaigns VALUES 

&nbsp;  ('CAMP\_ID', 'Campaign Name', 'Platform', 'Objective', 'Funnel Stage');

&nbsp;  ```



\### Importing Real Data

1\. Use file uploader in dashboard

2\. OR use API connectors in `app/data\_integration/`

3\. OR import CSV via `app/data\_integration/file\_uploader.py`



\### Database Migrations

1\. Backup current database: `cp furniture.db furniture.db.backup`

2\. Modify `database/schema.sql`

3\. Delete `furniture.db`

4\. Run `python setup\_database.py`

5\. Import data from backup if needed



---



\## 🤝 Contributing



\### Development Setup

```bash

\# Clone repository

git clone https://github.com/yourusername/midas-furniture-dashboard-final.git



\# Create virtual environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate



\# Install dependencies

pip install -r requirements.txt



\# Run tests (optional)

pytest tests/

```



\### Code Style

\- Follow PEP 8 guidelines

\- Use meaningful variable names

\- Add docstrings to functions

\- Comment complex logic



---



\## 📝 Changelog



\### Version 2.0 (Current)

\- ✅ Added SQLite database integration

\- ✅ Implemented user authentication

\- ✅ Added role-based access control

\- ✅ Enhanced export functionality

\- ✅ Added admin dashboard

\- ✅ Improved UI/UX with modern sidebar



\### Version 1.0

\- ✅ Initial dashboard with mock data

\- ✅ Basic campaign analytics

\- ✅ Simple CSV export



---



\## 📄 License



MIT License - See LICENSE file for details



---



\## 👨‍💻 Support



\### Documentation

\- 📖 \[Quick Deployment Guide](QUICK\_DEPLOYMENT\_CHECKLIST.md)

\- 📖 \[File Organization Guide](FILE\_ORGANIZATION\_GUIDE.md)

\- 📖 \[Complete Integration Plan](COMPLETE\_INTEGRATION\_PLAN.md)



\### Getting Help

\- 🐛 Report issues on GitHub

\- 💬 Check troubleshooting section above

\- 📧 Contact your development team



---



\## 🎯 Roadmap



\### Planned Features

\- \[ ] Multi-tenant support

\- \[ ] Advanced forecasting models

\- \[ ] Real-time data streaming

\- \[ ] Mobile responsive design

\- \[ ] Email alert notifications

\- \[ ] Slack/Teams integrations

\- \[ ] Custom dashboard builder

\- \[ ] API endpoint for external integrations



---



\## 🙏 Acknowledgments



Built with:

\- \[Streamlit](https://streamlit.io/) - Web framework

\- \[Plotly](https://plotly.com/) - Interactive charts

\- \[SQLAlchemy](https://www.sqlalchemy.org/) - ORM

\- \[bcrypt](https://github.com/pyca/bcrypt/) - Password hashing

\- \[scikit-learn](https://scikit-learn.org/) - Machine learning



---



\## 📞 Quick Links



\- 🏠 \[Dashboard Home](https://your-app.streamlit.app)

\- 📊 \[Documentation](./docs/)

\- 🐛 \[Issue Tracker](https://github.com/yourusername/repo/issues)

\- 💬 \[Discussions](https://github.com/yourusername/repo/discussions)



---



\*\*Built with ❤️ for digital marketing teams\*\*



---



\## 🚀 Get Started Now!



1\. \*\*Clone this repo\*\*

2\. \*\*Run `python setup\_database.py`\*\*

3\. \*\*Launch with `streamlit run dashboard.py`\*\*

4\. \*\*Login with `admin` / `admin123`\*\*

5\. \*\*Start analyzing your campaigns!\*\*



\*\*Questions?\*\* Check the \[Quick Deployment Guide](QUICK\_DEPLOYMENT\_CHECKLIST.md) 📖

