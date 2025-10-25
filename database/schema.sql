-- Campaigns and Ads Structure
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id TEXT PRIMARY KEY, campaign_name TEXT NOT NULL, platform TEXT NOT NULL,
    objective TEXT, funnel_stage TEXT
);

CREATE TABLE IF NOT EXISTS ad_sets (
    ad_set_id TEXT PRIMARY KEY, ad_set_name TEXT NOT NULL, campaign_id TEXT,
    targeting_criteria TEXT, FOREIGN KEY (campaign_id) REFERENCES campaigns (campaign_id)
);

CREATE TABLE IF NOT EXISTS ads (
    ad_id TEXT PRIMARY KEY, ad_name TEXT NOT NULL, ad_set_id TEXT,
    creative_type TEXT, creative_url TEXT, headline_text TEXT, body_text TEXT,
    test_id TEXT, -- For A/B Testing
    FOREIGN KEY (ad_set_id) REFERENCES ad_sets (ad_set_id)
);

-- Performance Data Tables
CREATE TABLE IF NOT EXISTS daily_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_date DATE NOT NULL, ad_id TEXT NOT NULL,
    campaign_id TEXT NOT NULL, impressions INTEGER, reach INTEGER, frequency REAL,
    clicks INTEGER, spend REAL, video_views INTEGER, add_to_carts INTEGER,
    conversions INTEGER, revenue REAL, UNIQUE(report_date, ad_id)
);

CREATE TABLE IF NOT EXISTS performance_by_segment (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_date DATE NOT NULL, ad_id TEXT NOT NULL,
    campaign_id TEXT NOT NULL, segment_type TEXT NOT NULL, segment_value TEXT NOT NULL,
    impressions INTEGER, clicks INTEGER, spend REAL, conversions INTEGER, revenue REAL,
    UNIQUE(report_date, ad_id, segment_type, segment_value)
);

CREATE TABLE IF NOT EXISTS performance_by_country (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_date DATE NOT NULL, platform TEXT NOT NULL,
    country TEXT NOT NULL, impressions INTEGER, clicks INTEGER, spend REAL,
    conversions INTEGER, revenue REAL, UNIQUE(report_date, platform, country)
);

-- User Management Tables
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles (role_id)
);

CREATE TABLE IF NOT EXISTS role_permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    page_name TEXT NOT NULL, -- e.g., 'Creative_Analysis', 'Budget_Pacing'
    FOREIGN KEY (role_id) REFERENCES roles (role_id),
    UNIQUE(role_id, page_name)
);


-- Feature-Specific Tables
CREATE TABLE IF NOT EXISTS campaign_budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT, campaign_id TEXT NOT NULL UNIQUE,
    start_date DATE NOT NULL, end_date DATE NOT NULL, total_budget REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS ab_tests (
    test_id TEXT PRIMARY KEY, test_name TEXT NOT NULL, hypothesis TEXT,
    start_date DATE, end_date DATE
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY, first_seen_date DATE
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT NOT NULL,
    sale_date DATE NOT NULL, sale_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, alert_date DATE NOT NULL, metric TEXT,
    ad_id TEXT, justification TEXT, status TEXT DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT, generation_date DATE NOT NULL, ad_id TEXT,
    recommendation_type TEXT, justification TEXT, status TEXT DEFAULT 'Active'
);