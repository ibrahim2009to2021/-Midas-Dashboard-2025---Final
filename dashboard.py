"""
Midas Furniture Campaign Analytics Dashboard — Platform‑Smart Metrics
Version: 4.0 (platform selector drives platform‑specific KPIs)

Drop‑in replacement for your current single‑file Streamlit app.
- Sidebar select a platform → dashboard filters data + shows the relevant metric cards
- Adds per‑platform synthetic fields for demo; replace with real columns when wiring to your data source
- Keeps your original layout and charts, but scoped to selection
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any
import plotly.express as px

# ========================================
# PAGE CONFIGURATION
# ========================================

st.set_page_config(
    page_title="Midas Analytics Platform",
    page_icon="🛋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========================================
# DATA LOADING FUNCTIONS
# ========================================

@st.cache_data(ttl=3600)
def load_campaign_data() -> pd.DataFrame:
    """Load campaign performance data with some platform‑specific demo fields."""
    now = datetime.now()
    dates = pd.date_range(start=now - timedelta(days=90), end=now, freq="D")
    campaigns = [
        "Spring Sale 2025",
        "Summer Collection",
        "Bedroom Special",
        "Living Room Deals",
        "Office Furniture",
    ]
    platforms = ["Meta", "Google", "TikTok", "Snapchat"]

    rng = np.random.default_rng(42)
    rows = []

    for date in dates:
        for campaign in campaigns:
            for platform in platforms:
                spend = rng.uniform(500, 2000)
                impressions = int(spend * rng.uniform(800, 1200))
                clicks = max(1, int(impressions * rng.uniform(0.008, 0.035)))
                conversions = max(0, int(clicks * rng.uniform(0.02, 0.08)))
                revenue = conversions * rng.uniform(300, 800)

                base = {
                    "date": date,
                    "campaign_name": campaign,
                    "platform": platform,
                    "spend": round(spend, 2),
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "revenue": round(revenue, 2),
                }

                # --- Platform‑specific synthetic signals (replace with real columns when available) ---
                if platform == "Meta":
                    base.update(
                        {
                            "quality_ranking": rng.choice(
                                ["Above Avg", "Average", "Below Avg"], p=[0.35, 0.45, 0.20]
                            ),
                            "engagement_rate_rank": rng.choice(
                                ["Above Avg", "Average", "Below Avg"], p=[0.3, 0.5, 0.2]
                            ),
                        }
                    )
                elif platform == "Google":
                    base.update(
                        {
                            "search_impr_share": round(rng.uniform(0.45, 0.92), 3),
                            "top_impr_share": round(rng.uniform(0.30, 0.85), 3),
                            "avg_pos_proxy": round(rng.uniform(1.2, 3.8), 2),  # proxy only
                        }
                    )
                elif platform == "TikTok":
                    views_3s = int(impressions * rng.uniform(0.15, 0.45))
                    views_6s = int(impressions * rng.uniform(0.06, 0.25))
                    base.update(
                        {
                            "views_3s": views_3s,
                            "views_6s": views_6s,
                            "avg_watch_time_s": round(rng.uniform(2.0, 8.0), 1),
                        }
                    )
                elif platform == "Snapchat":
                    video_views = int(impressions * rng.uniform(0.10, 0.40))
                    story_opens = int(impressions * rng.uniform(0.05, 0.20))
                    base.update(
                        {
                            "video_views": video_views,
                            "story_opens": story_opens,
                            "avg_screen_time_s": round(rng.uniform(1.5, 6.5), 1),
                        }
                    )

                rows.append(base)

    df = pd.DataFrame(rows)

    # Shared derived metrics
    df["roas"] = (df["revenue"] / df["spend"]).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    df["cpa"] = (df["spend"] / df["conversions"]).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    df["ctr"] = (df["clicks"] / df["impressions"] * 100).replace([np.inf, -np.inf], 0).fillna(0).round(3)
    df["cpc"] = (df["spend"] / df["clicks"]).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    df["cpm"] = (df["spend"] / df["impressions"] * 1000).replace([np.inf, -np.inf], 0).fillna(0).round(2)

    # Platform‑specific derived metrics
    # Meta: CVR
    df.loc[df.platform == "Meta", "cvr"] = (
        df.loc[df.platform == "Meta", "conversions"]
        / df.loc[df.platform == "Meta", "clicks"]
        * 100
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)

    # Google: conv_value_cost (ROAS synonym), keep roas
    df.loc[df.platform == "Google", "conv_value_cost"] = df.loc[df.platform == "Google", "roas"].round(2)

    # TikTok: hook rates (3s/6s)
    if "views_3s" in df.columns:
        df["hook_rate_3s_pct"] = (
            df.get("views_3s", 0) / df["impressions"] * 100
        ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    if "views_6s" in df.columns:
        df["hold_rate_6s_pct"] = (
            df.get("views_6s", 0) / df["impressions"] * 100
        ).replace([np.inf, -np.inf], 0).fillna(0).round(2)

    # Snapchat: swipe up rate = CTR, story open rate
    if "story_opens" in df.columns:
        df["story_open_rate_pct"] = (
            df.get("story_opens", 0) / df["impressions"] * 100
        ).replace([np.inf, -np.inf], 0).fillna(0).round(2)

    return df

# ========================================
# PLATFORM METRIC CONFIG
# ========================================

PLATFORM_CONFIG: Dict[str, Dict[str, Any]] = {
    "Meta": {
        "cards": [
            ("CPM", "cpm", "${:,.2f}"),
            ("CPC", "cpc", "${:,.2f}"),
            ("CTR", "ctr", "{:.2f}%"),
            ("CVR", "cvr", "{:.2f}%"),
            ("CPA", "cpa", "${:,.2f}"),
            ("ROAS", "roas", "{:.2f}x"),
        ],
        "extras": ["quality_ranking", "engagement_rate_rank"],
        "glossary": [
            ("CPM", "Cost per 1,000 impressions = Spend/Impr*1000"),
            ("CPC", "Cost per click = Spend/Clicks"),
            ("CTR", "Click‑through rate = Clicks/Impr"),
            ("CVR", "Conversion rate = Conv/Clicks"),
            ("CPA", "Cost per acquisition = Spend/Conv"),
            ("ROAS", "Return on ad spend = Revenue/Spend"),
            ("Quality Ranking", "Meta delivery diagnostic: relative ad quality"),
        ],
    },
    "Google": {
        "cards": [
            ("CPM", "cpm", "${:,.2f}"),
            ("CPC", "cpc", "${:,.2f}"),
            ("CTR", "ctr", "{:.2f}%"),
            ("Conv Value/Cost", "conv_value_cost", "{:.2f}x"),
            ("CPA", "cpa", "${:,.2f}"),
            ("ROAS", "roas", "{:.2f}x"),
        ],
        "extras": ["search_impr_share", "top_impr_share", "avg_pos_proxy"],
        "glossary": [
            ("Search Impression Share", "Impr / Eligible impr share"),
            ("Top Impression Share", "% of impr that appeared above organic"),
            ("Avg Pos (proxy)", "Approximate average position for demo"),
        ],
    },
    "TikTok": {
        "cards": [
            ("CPM", "cpm", "${:,.2f}"),
            ("CTR", "ctr", "{:.2f}%"),
            ("Hook Rate 3s", "hook_rate_3s_pct", "{:.2f}%"),
            ("Hold Rate 6s", "hold_rate_6s_pct", "{:.2f}%"),
            ("CPA", "cpa", "${:,.2f}"),
            ("ROAS", "roas", "{:.2f}x"),
        ],
        "extras": ["avg_watch_time_s"],
        "glossary": [
            ("Hook Rate 3s", "3s views / impressions"),
            ("Hold Rate 6s", "6s views / impressions"),
            ("Avg Watch Time", "Average seconds watched per impression"),
        ],
    },
    "Snapchat": {
        "cards": [
            ("CPM", "cpm", "${:,.2f}"),
            ("Swipe‑Up Rate", "ctr", "{:.2f}%"),
            ("Story Open Rate", "story_open_rate_pct", "{:.2f}%"),
            ("CPA", "cpa", "${:,.2f}"),
            ("ROAS", "roas", "{:.2f}x"),
            ("CPC", "cpc", "${:,.2f}"),
        ],
        "extras": ["avg_screen_time_s"],
        "glossary": [
            ("Swipe‑Up Rate", "Equivalent to CTR on Snap placements"),
            ("Story Open Rate", "Story opens / impressions"),
            ("Avg Screen Time", "Avg seconds the ad was on screen"),
        ],
    },
}

# ========================================
# SIDEBAR
# ========================================

def render_sidebar(df: pd.DataFrame) -> str:
    st.sidebar.title("👤 Admin User")
    st.sidebar.caption("ADMINISTRATOR")
    st.sidebar.divider()

    # Platform selector (drives the whole page)
    platforms = ["All"] + sorted(df["platform"].unique().tolist())
    selected = st.sidebar.selectbox("Select Platform", platforms, index=1)

    # Quick Stats (for the selected scope)
    scope_df = df if selected == "All" else df[df.platform == selected]

    st.sidebar.subheader("⚡ Quick Stats")
    st.sidebar.metric("Active Campaigns", f"{scope_df['campaign_name'].nunique()}")
    st.sidebar.metric("Total Spend", f"${scope_df['spend'].sum():,.0f}")
    avg_roas = (scope_df["revenue"].sum() / scope_df["spend"].sum()) if scope_df["spend"].sum() > 0 else 0
    st.sidebar.metric("Avg ROAS", f"{avg_roas:.2f}x", delta="Target: 2.5x")

    st.sidebar.divider()
    st.sidebar.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

    return selected

# ========================================
# MAIN DASHBOARD
# ========================================

def metric_card_row(df: pd.DataFrame, platform: str):
    """Render platform‑specific KPI cards for the selected scope."""
    if platform == "All":
        cols = st.columns(4)
        with cols[0]:
            st.metric("Total Spend", f"${df['spend'].sum():,.0f}")
        with cols[1]:
            st.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
        with cols[2]:
            roas = (df["revenue"].sum() / df["spend"].sum()) if df["spend"].sum() > 0 else 0
            st.metric("ROAS", f"{roas:.2f}x")
        with cols[3]:
            st.metric("Conversions", f"{df['conversions'].sum():,.0f}")
        return

    cfg = PLATFORM_CONFIG.get(platform, {})
    cards = cfg.get("cards", [])
    n = len(cards)
    n_cols = 6 if n >= 6 else max(3, n)
    col_objs = st.columns(n_cols)

    # Aggregate to page scope
    agg = df.agg(
        {
            "spend": "sum",
            "revenue": "sum",
            "impressions": "sum",
            "clicks": "sum",
            "conversions": "sum",
            "roas": "mean",
            "cpa": "mean",
            "ctr": "mean",
            "cpc": "mean",
            "cpm": "mean",
            "cvr": "mean",
            "conv_value_cost": "mean",
            "hook_rate_3s_pct": "mean",
            "hold_rate_6s_pct": "mean",
            "story_open_rate_pct": "mean",
        }
    )

    for i, (label, col, fmt) in enumerate(cards):
        val = agg.get(col, np.nan)
        try:
            text = fmt.format(val)
        except Exception:
            text = str(val)
        with col_objs[i % n_cols]:
            st.metric(label, text)

    # Show optional extra diagnostics as a small table
    extras = cfg.get("extras", [])
    extra_cols = [c for c in extras if c in df.columns]
    if extra_cols:
        st.caption("Additional diagnostics")
        st.dataframe(
            df[extra_cols]
            .apply(pd.to_numeric, errors="ignore")
            .describe(include="all")
            .T,
            use_container_width=True,
            hide_index=False,
        )


def render_dashboard(df: pd.DataFrame, selected_platform: str):
    st.title("🛋️ Midas Furniture Campaign Analytics")
    st.markdown("Select a **platform** in the sidebar — KPIs and charts change accordingly.")
    st.markdown("---")

    scope_df = df if selected_platform == "All" else df[df.platform == selected_platform]

    # Platform‑aware KPI cards
    metric_card_row(scope_df, selected_platform)

    st.markdown("---")

    # Charts (scoped)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Platform")
        plat_rev = scope_df.groupby("platform")["revenue"].sum().reset_index()
        fig = px.bar(plat_rev, x="platform", y="revenue", color="platform")
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Daily ROAS Trend")
        daily = scope_df.groupby("date").agg({"revenue": "sum", "spend": "sum"}).reset_index()
        daily["roas"] = (daily["revenue"] / daily["spend"]).replace([np.inf, -np.inf], 0).fillna(0)
        fig = px.line(daily, x="date", y="roas")
        fig.add_hline(y=2.5, line_dash="dash", line_color="red", annotation_text="Target")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Top Campaigns Table (scoped)
    st.subheader("Top Performing Campaigns")
    top = (
        scope_df.groupby("campaign_name").agg({"spend": "sum", "revenue": "sum", "conversions": "sum"}).reset_index()
    )
    top["roas"] = (top["revenue"] / top["spend"]).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    top = top.sort_values("revenue", ascending=False).head(10)
    st.dataframe(top, use_container_width=True, hide_index=True)

    # Platform glossary
    if selected_platform != "All":
        cfg = PLATFORM_CONFIG.get(selected_platform, {})
        glossary = cfg.get("glossary", [])
        with st.expander(f"ℹ️ {selected_platform} metrics glossary"):
            for name, desc in glossary:
                st.markdown(f"**{name}:** {desc}")

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    with st.spinner("Loading data..."):
        df = load_campaign_data()

    selected_platform = render_sidebar(df)
    render_dashboard(df, selected_platform)


if __name__ == "__main__":
    main()
