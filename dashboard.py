"""
Midas Furniture Campaign Analytics Dashboard — Platform‑Smart Metrics
Version: 5.0 (Modern UI + Per‑Platform Deep‑Dive Charts)

What's new
- Modern layout: tabs (Overview / Deep Dive / Top Campaigns), compact KPI grid, cleaner Plotly styling
- Global filters: date range + campaign multi‑select + platform selector (sidebar)
- Per‑platform deep‑dive: **two extra charts** tailored to each platform
- Non‑intrusive styling + accessibility labels + consistent number formats

Drop‑in replacement for your current Streamlit app.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import plotly.express as px
import plotly.graph_objects as go

# =============================
# PAGE CONFIG & LIGHT STYLES
# =============================

st.set_page_config(
    page_title="Midas Analytics Platform",
    page_icon="🛋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Small, safe CSS for tighter spacing & readable tables
st.markdown(
    """
    <style>
    .metric-card {padding: 0.5rem 0.75rem; border-radius: 12px; background: var(--background-color);}
    .metric-label {font-size: 0.85rem; color: #6b7280;}
    .metric-value {font-size: 1.2rem; font-weight: 700;}
    .block-caption {color:#6b7280; font-size:0.85rem}
    .stDataFrame table {font-size: 0.92rem}
    </style>
    """,
    unsafe_allow_html=True,
)

PLOTLY_TEMPLATE = "plotly_white"

# =============================
# DATA LOADING
# =============================

@st.cache_data(ttl=3600)
def load_campaign_data() -> pd.DataFrame:
    """Demo data with platform‑specific fields. Replace with production query/CSV."""
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

                # Platform‑specific synthetic fields
                if platform == "Meta":
                    base.update(
                        {
                            "quality_ranking": rng.choice(["Above Avg", "Average", "Below Avg"], p=[0.35, 0.45, 0.20]),
                            "engagement_rate_rank": rng.choice(["Above Avg", "Average", "Below Avg"], p=[0.3, 0.5, 0.2]),
                        }
                    )
                elif platform == "Google":
                    base.update(
                        {
                            "search_impr_share": round(rng.uniform(0.45, 0.92), 3),
                            "top_impr_share": round(rng.uniform(0.30, 0.85), 3),
                            "avg_pos_proxy": round(rng.uniform(1.2, 3.8), 2),
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
    df.loc[df.platform == "Meta", "cvr"] = (
        df.loc[df.platform == "Meta", "conversions"] / df.loc[df.platform == "Meta", "clicks"] * 100
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)

    df.loc[df.platform == "Google", "conv_value_cost"] = df.loc[df.platform == "Google", "roas"].round(2)

    if "views_3s" in df.columns:
        df["hook_rate_3s_pct"] = (df.get("views_3s", 0) / df["impressions"] * 100).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    if "views_6s" in df.columns:
        df["hold_rate_6s_pct"] = (df.get("views_6s", 0) / df["impressions"] * 100).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    if "story_opens" in df.columns:
        df["story_open_rate_pct"] = (df.get("story_opens", 0) / df["impressions"] * 100).replace([np.inf, -np.inf], 0).fillna(0).round(2)

    return df

# =============================
# PLATFORM METRIC CONFIG
# =============================

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
            ("Search Impression Share", "Impr / eligible impressions"),
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

# =============================
# FILTERS & SIDEBAR
# =============================

def render_sidebar(df: pd.DataFrame) -> Tuple[str, List[str], Tuple[pd.Timestamp, pd.Timestamp]]:
    st.sidebar.title("👤 Admin User")
    st.sidebar.caption("ADMINISTRATOR")
    st.sidebar.divider()

    platforms = ["All"] + sorted(df["platform"].unique().tolist())
    selected_platform = st.sidebar.selectbox("Select Platform", platforms, index=1)

    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple):
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    else:
        start_date, end_date = min_date, max_date

    campaigns = sorted(df["campaign_name"].unique().tolist())
    selected_campaigns = st.sidebar.multiselect("Campaigns", campaigns, default=campaigns)

    # Quick Stats (scoped)
    scope = df[(df["date"] >= start_date) & (df["date"] <= end_date) & (df["campaign_name"].isin(selected_campaigns))]
    scope = scope if selected_platform == "All" else scope[scope.platform == selected_platform]

    st.sidebar.subheader("⚡ Quick Stats")
    st.sidebar.metric("Active Campaigns", f"{scope['campaign_name'].nunique()}")
    st.sidebar.metric("Total Spend", f"${scope['spend'].sum():,.0f}")
    avg_roas = (scope["revenue"].sum() / scope["spend"].sum()) if scope["spend"].sum() > 0 else 0
    st.sidebar.metric("Avg ROAS", f"{avg_roas:.2f}x", delta="Target: 2.5x")

    st.sidebar.divider()
    st.sidebar.caption(f"🕐 Updated: {datetime.now().strftime('%H:%M:%S')}")

    return selected_platform, selected_campaigns, (start_date, end_date)

# =============================
# UI HELPERS
# =============================

def metric_cards(df: pd.DataFrame, platform: str):
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
    col_objs = st.columns(min(6, max(3, n)))

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
        with col_objs[i % len(col_objs)]:
            st.metric(label, text)

    extras = cfg.get("extras", [])
    extra_cols = [c for c in extras if c in df.columns]
    if extra_cols:
        st.caption("Additional diagnostics")
        st.dataframe(
            df[extra_cols].apply(pd.to_numeric, errors="ignore").describe(include="all").T,
            use_container_width=True,
            hide_index=False,
        )

# =============================
# CHARTS
# =============================

def shared_overview(scope_df: pd.DataFrame):
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Platform")
        plat_rev = scope_df.groupby("platform")["revenue"].sum().reset_index()
        fig = px.bar(plat_rev, x="platform", y="revenue", color="platform", template=PLOTLY_TEMPLATE)
        fig.update_layout(showlegend=False, height=400, yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Daily ROAS Trend")
        daily = scope_df.groupby("date").agg({"revenue": "sum", "spend": "sum"}).reset_index()
        daily["roas"] = (daily["revenue"] / daily["spend"]).replace([np.inf, -np.inf], 0).fillna(0)
        fig = px.line(daily, x="date", y="roas", template=PLOTLY_TEMPLATE)
        fig.add_hline(y=2.5, line_dash="dash", line_color="red", annotation_text="Target")
        fig.update_layout(height=400, yaxis_title="ROAS (x)")
        st.plotly_chart(fig, use_container_width=True)


def platform_deep_dive(scope_df: pd.DataFrame, platform: str):
    """Two extra charts per platform (latest standards)."""
    if platform == "Meta":
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("CTR vs CPM (bubble by Impr)")
            fig = px.scatter(
                scope_df,
                x="cpm",
                y="ctr",
                size="impressions",
                color="campaign_name",
                hover_data=["spend", "clicks", "conversions"],
                template=PLOTLY_TEMPLATE,
                labels={"cpm": "CPM ($)", "ctr": "CTR (%)"},
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("CVR Trend by Day")
            tmp = scope_df.assign(cvr=(scope_df["conversions"] / scope_df["clicks"] * 100).replace([np.inf, -np.inf], 0).fillna(0))
            daily = tmp.groupby("date")["cvr"].mean().reset_index()
            fig = px.line(daily, x="date", y="cvr", template=PLOTLY_TEMPLATE, labels={"cvr": "CVR (%)"})
            st.plotly_chart(fig, use_container_width=True)

    elif platform == "Google":
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Impr Share vs ROAS (bubble by Spend)")
            fig = px.scatter(
                scope_df,
                x="search_impr_share",
                y="roas",
                size="spend",
                color="campaign_name",
                template=PLOTLY_TEMPLATE,
                labels={"search_impr_share": "Search Impr Share", "roas": "ROAS (x)"},
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("CPC Distribution by Campaign")
            fig = px.box(scope_df, x="campaign_name", y="cpc", template=PLOTLY_TEMPLATE, labels={"cpc": "CPC ($)"})
            fig.update_layout(xaxis_title="Campaign", yaxis_title="CPC ($)")
            st.plotly_chart(fig, use_container_width=True)

    elif platform == "TikTok":
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Hook (3s) vs Hold (6s)")
            fig = px.scatter(
                scope_df,
                x="hook_rate_3s_pct",
                y="hold_rate_6s_pct",
                size="impressions",
                color="campaign_name",
                template=PLOTLY_TEMPLATE,
                labels={"hook_rate_3s_pct": "Hook 3s (%)", "hold_rate_6s_pct": "Hold 6s (%)"},
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Avg Watch Time by Day")
            daily = scope_df.groupby("date")["avg_watch_time_s"].mean().reset_index()
            fig = px.line(daily, x="date", y="avg_watch_time_s", template=PLOTLY_TEMPLATE, labels={"avg_watch_time_s": "Watch Time (s)"})
            st.plotly_chart(fig, use_container_width=True)

    elif platform == "Snapchat":
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Swipe‑Up vs Story Open Rate")
            fig = px.scatter(
                scope_df,
                x="ctr",
                y="story_open_rate_pct",
                size="impressions",
                color="campaign_name",
                template=PLOTLY_TEMPLATE,
                labels={"ctr": "Swipe‑Up Rate (%)", "story_open_rate_pct": "Story Open Rate (%)"},
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Avg Screen Time by Day")
            daily = scope_df.groupby("date")["avg_screen_time_s"].mean().reset_index()
            fig = px.line(daily, x="date", y="avg_screen_time_s", template=PLOTLY_TEMPLATE, labels={"avg_screen_time_s": "Screen Time (s)"})
            st.plotly_chart(fig, use_container_width=True)

# =============================
# MAIN VIEWS
# =============================

def render_dashboard(df: pd.DataFrame, selected_platform: str, campaigns: List[str], drange: Tuple[pd.Timestamp, pd.Timestamp]):
    st.title("🛋️ Midas Furniture Campaign Analytics")
    st.caption("Modern, platform‑aware KPIs with deep‑dive visuals.")
    st.markdown("---")

    start_date, end_date = drange
    scope_df = df[(df["date"] >= start_date) & (df["date"] <= end_date) & (df["campaign_name"].isin(campaigns))]
    scope_df = scope_df if selected_platform == "All" else scope_df[scope_df.platform == selected_platform]

    tabs = st.tabs(["Overview", "Platform Deep Dive", "Top Campaigns"])

    with tabs[0]:
        metric_cards(scope_df, selected_platform)
        st.markdown("---")
        shared_overview(scope_df)

    with tabs[1]:
        if selected_platform == "All":
            st.info("Select a specific platform in the sidebar to see deep‑dive charts.")
        else:
            platform_deep_dive(scope_df, selected_platform)
            # Glossary
            cfg = PLATFORM_CONFIG.get(selected_platform, {})
            glossary = cfg.get("glossary", [])
            with st.expander(f"ℹ️ {selected_platform} metrics glossary"):
                for name, desc in glossary:
                    st.markdown(f"**{name}:** {desc}")

    with tabs[2]:
        st.subheader("Top Performing Campaigns")
        top = scope_df.groupby("campaign_name").agg({"spend": "sum", "revenue": "sum", "conversions": "sum"}).reset_index()
        top["roas"] = (top["revenue"] / top["spend"]).replace([np.inf, -np.inf], 0).fillna(0).round(2)
        top = top.sort_values("revenue", ascending=False).head(10)
        st.dataframe(top, use_container_width=True, hide_index=True)

# =============================
# MAIN
# =============================

def main():
    with st.spinner("Loading data..."):
        df = load_campaign_data()

    selected_platform, selected_campaigns, drange = render_sidebar(df)
    render_dashboard(df, selected_platform, selected_campaigns, drange)


if __name__ == "__main__":
    main()
