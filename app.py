"""
🇸🇦 Saudi Market Intelligence Platform
Research Opportunities & Lead Generation Dashboard
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# Page config — must be first Streamlit call
st.set_page_config(
    page_title="Saudi Market Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Local imports
from components.kpi_cards import inject_card_styles, render_header, render_kpi, render_section_header, format_sar, format_usd
from components.charts import (
    sector_donut, value_bar, pipeline_funnel, timeline_chart,
    sentiment_gauge, opportunity_treemap, tender_value_by_sector,
)
from services.news_service import fetch_news, get_news_summary
from services.tenders_service import get_tenders_data, get_tenders_summary
from services.megaprojects_service import get_megaprojects_data, get_megaprojects_summary, get_opportunity_sectors
from services.leads_service import get_leads, add_lead, update_lead, delete_lead, get_pipeline_summary, calculate_lead_score
from services.ai_intelligence import get_ai_intelligence, get_available_sectors


# ─────────────────────────────────────────────
# INJECT STYLES & HEADER
# ─────────────────────────────────────────────
inject_card_styles()
render_header()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div style="font-size: 36px; margin-bottom: 8px;">🇸🇦</div>
        <div style="color: #C5A55A; font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 700;">Market Intelligence</div>
        <div style="color: #8892B0; font-size: 11px; margin-top: 4px;">Powered by AI & Live Data</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔍 Global Filters")
    
    # Sector filter
    all_sectors = ["All", "Construction", "Technology", "Energy", "Healthcare", "Tourism",
                   "Defense", "Transport", "Finance", "Entertainment", "Education", "Water"]
    selected_sector = st.selectbox("Sector Focus", all_sectors, index=0)
    
    # Region filter
    all_regions = ["All", "Riyadh", "Jeddah", "Tabuk", "Eastern Province", "Madinah",
                   "Makkah", "KAEC", "Multiple", "Arabian Gulf"]
    selected_region = st.selectbox("Region", all_regions, index=0)
    
    # Value range
    st.markdown("### 💰 Value Range (SAR)")
    min_value = st.number_input("Minimum (Millions)", min_value=0, value=0, step=10)
    max_value = st.number_input("Maximum (Millions)", min_value=0, value=10000, step=100)
    
    st.markdown("---")
    
    # AI Configuration
    st.markdown("### 🤖 AI Configuration")
    gemini_key = st.text_input("Gemini API Key (optional)", type="password", help="Enter your Google Gemini API key for live AI intelligence. Leave blank to use curated data.")
    if gemini_key:
        import os
        os.environ["GEMINI_API_KEY"] = gemini_key
        st.success("✅ AI Connected")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <div style="color: #475569; font-size: 10px;">Built with Streamlit • Data as of Feb 2026</div>
        <div style="color: #C5A55A; font-size: 10px; margin-top: 4px;">v1.0 • Saudi Market Intelligence</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Executive Overview",
    "📰 Market News",
    "📋 Tenders & RFPs",
    "🏗️ Mega Projects",
    "👤 Lead Tracker",
    "🤖 AI Intelligence",
])


# ═════════════════════════════════════════════
# TAB 1: EXECUTIVE OVERVIEW
# ═════════════════════════════════════════════
with tab1:
    # Load all data
    tenders_df = get_tenders_data()
    mega_df = get_megaprojects_data()
    leads = get_leads()
    tender_summary = get_tenders_summary(tenders_df)
    mega_summary = get_megaprojects_summary(mega_df)
    pipeline_summary = get_pipeline_summary(leads)
    opp_sectors = get_opportunity_sectors(mega_df)
    
    # KPI Row
    render_section_header("📊", "Market Snapshot", "LIVE", "badge-gold")
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        render_kpi("Open Tenders", str(tender_summary["open_tenders"]),
                  f"of {tender_summary['total_tenders']} total", "gold")
    with k2:
        render_kpi("Tender Value", format_sar(tender_summary["total_value"]),
                  "Active opportunities", "navy")
    with k3:
        render_kpi("Mega Projects", str(mega_summary["active_projects"]),
                  f"{format_usd(mega_summary['total_value_usd'])} total value", "blue")
    with k4:
        render_kpi("Pipeline Value", format_sar(pipeline_summary["total_pipeline_value"]),
                  f"{pipeline_summary['active_leads']} active leads", "green")
    with k5:
        render_kpi("Weighted Pipeline", format_sar(pipeline_summary["total_weighted_value"]),
                  f"{pipeline_summary['avg_probability']:.0f}% avg probability", "purple")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    c1, c2 = st.columns(2)
    with c1:
        fig = sector_donut(tender_summary["by_sector"], "Tender Value by Sector")
        st.plotly_chart(fig, use_container_width=True, key="overview_sector_donut")
    with c2:
        fig = value_bar(tender_summary["by_region"], "Tender Value by Region (SAR)")
        st.plotly_chart(fig, use_container_width=True, key="overview_region_bar")
    
    # Second Charts Row
    c3, c4 = st.columns(2)
    with c3:
        fig = pipeline_funnel(pipeline_summary["stages"])
        st.plotly_chart(fig, use_container_width=True, key="overview_pipeline_funnel")
    with c4:
        fig = opportunity_treemap(dict(list(opp_sectors.items())[:12]), "Top Opportunity Sectors Across Mega Projects")
        st.plotly_chart(fig, use_container_width=True, key="overview_opp_treemap")
    
    # Closing Soon Alert
    closing = tenders_df[tenders_df["status"] == "Closing Soon"].sort_values("deadline")
    if len(closing) > 0:
        render_section_header("⚠️", "Closing Soon — Urgent Tenders", f"{len(closing)} tenders", "badge-red")
        for _, t in closing.iterrows():
            days = t["days_left"]
            urgency = "🔴" if days <= 7 else "🟡"
            st.markdown(f"""
            <div class="tender-row" style="cursor: pointer;">
                <div style="font-size: 20px;">{urgency}</div>
                <div style="flex:1;">
                    <div style="font-weight: 700; color: #0A192F; font-size: 13px;">{t['title']}</div>
                    <div style="font-size: 11px; color: #64748B;">{t['entity']} • {t['region']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #DC2626; font-size: 13px;">{days} days left</div>
                    <div style="font-size: 11px; color: #64748B;">{format_sar(t['value_sar'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# TAB 2: MARKET NEWS
# ═════════════════════════════════════════════
with tab2:
    render_section_header("📰", "Live Saudi Business News", "RSS FEEDS", "badge-blue")
    
    with st.spinner("Fetching latest news from Saudi sources..."):
        news_items = fetch_news(max_per_source=12)
    
    news_summary = get_news_summary(news_items)
    
    # News KPIs
    nk1, nk2, nk3, nk4 = st.columns(4)
    with nk1:
        render_kpi("Total Articles", str(news_summary["total"]), "From all sources", "navy")
    with nk2:
        render_kpi("Sources Active", str(len(news_summary["sources"])), "RSS feeds", "blue")
    with nk3:
        pos_count = news_summary["sentiments"].get("Positive", 0)
        render_kpi("Positive Sentiment", str(pos_count), f"of {news_summary['total']} articles", "green")
    with nk4:
        top_cat = max(news_summary["categories"], key=news_summary["categories"].get) if news_summary["categories"] else "N/A"
        render_kpi("Trending Sector", top_cat, "Most mentioned", "gold")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sentiment Chart
    col_sent, col_cat = st.columns([1, 2])
    with col_sent:
        fig = sentiment_gauge(
            news_summary["sentiments"].get("Positive", 0),
            news_summary["sentiments"].get("Neutral", 0),
            news_summary["sentiments"].get("Negative", 0),
        )
        st.plotly_chart(fig, use_container_width=True, key="news_sentiment_gauge")
    with col_cat:
        if news_summary["categories"]:
            fig = sector_donut(news_summary["categories"], "News by Category")
            st.plotly_chart(fig, use_container_width=True, key="news_category_donut")
    
    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        cat_filter = st.selectbox("Category", ["All"] + list(news_summary["categories"].keys()), key="news_cat")
    with filter_col2:
        sent_filter = st.selectbox("Sentiment", ["All", "Positive", "Neutral", "Negative"], key="news_sent")
    with filter_col3:
        source_filter = st.selectbox("Source", ["All"] + list(news_summary["sources"].keys()), key="news_src")
    
    # Filter news
    filtered_news = news_items
    if cat_filter != "All":
        filtered_news = [n for n in filtered_news if n.category == cat_filter]
    if sent_filter != "All":
        filtered_news = [n for n in filtered_news if n.sentiment == sent_filter]
    if source_filter != "All":
        filtered_news = [n for n in filtered_news if n.source == source_filter]
    
    # News Cards
    st.markdown(f"**Showing {len(filtered_news)} articles**")
    for item in filtered_news:
        if item.category == "System":
            st.warning(f"**{item.title}** — {item.summary}")
            continue
        
        sent_badge = {"Positive": "badge-positive", "Negative": "badge-negative", "Neutral": "badge-neutral"}.get(item.sentiment, "badge-neutral")
        sent_emoji = {"Positive": "📈", "Negative": "📉", "Neutral": "📊"}.get(item.sentiment, "📊")
        
        link_html = f'<a href="{item.url}" target="_blank">{item.title}</a>' if item.url else item.title
        
        st.markdown(f"""
        <div class="news-card">
            <div class="news-title">{link_html}</div>
            <div class="news-meta">
                <span>📡 {item.source}</span>
                <span>📅 {item.date}</span>
                <span class="status-badge badge-gold">{item.category}</span>
                <span class="status-badge {sent_badge}">{sent_emoji} {item.sentiment}</span>
            </div>
            <div class="news-summary">{item.summary[:300]}{'...' if len(item.summary) > 300 else ''}</div>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# TAB 3: TENDERS & RFPs
# ═════════════════════════════════════════════
with tab3:
    render_section_header("📋", "Saudi Tenders & Procurement", "LIVE DATABASE", "badge-navy")
    
    tenders_df = get_tenders_data()
    
    # Apply global filters
    if selected_sector != "All":
        tenders_df = tenders_df[tenders_df["sector"] == selected_sector]
    if selected_region != "All":
        tenders_df = tenders_df[tenders_df["region"].str.contains(selected_region, case=False, na=False)]
    if min_value > 0:
        tenders_df = tenders_df[tenders_df["value_sar"] >= min_value * 1e6]
    if max_value < 10000:
        tenders_df = tenders_df[tenders_df["value_sar"] <= max_value * 1e6]
    
    tsummary = get_tenders_summary(tenders_df)
    
    # KPI Row
    tk1, tk2, tk3, tk4 = st.columns(4)
    with tk1:
        render_kpi("Active Tenders", str(tsummary["open_tenders"]), "Currently open", "green")
    with tk2:
        render_kpi("Total Value", format_sar(tsummary["total_value"]), "Open opportunities", "gold")
    with tk3:
        render_kpi("Closing Soon", str(tsummary["closing_soon"]), "Act now!", "red")
    with tk4:
        render_kpi("Avg Value", format_sar(tsummary["avg_value"]) if tsummary["avg_value"] > 0 else "N/A",
                  "Per tender", "blue")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    chart1, chart2 = st.columns(2)
    with chart1:
        if tsummary["by_sector"]:
            fig = tender_value_by_sector(tsummary["by_sector"])
            st.plotly_chart(fig, use_container_width=True, key="tenders_sector_bar")
    with chart2:
        if tsummary["by_region"]:
            fig = value_bar(tsummary["by_region"], "Tender Value by Region (SAR)")
            st.plotly_chart(fig, use_container_width=True, key="tenders_region_bar")
    
    # Tender Filter
    render_section_header("🔎", "Search Tenders")
    search_col1, search_col2, search_col3 = st.columns(3)
    with search_col1:
        search_query = st.text_input("🔍 Search tenders", placeholder="e.g., NEOM, cybersecurity, solar...")
    with search_col2:
        status_filter = st.selectbox("Status", ["All", "Open", "Closing Soon", "Awarded", "Closed"], key="tender_status")
    with search_col3:
        sort_by = st.selectbox("Sort By", ["Deadline (Nearest)", "Value (Highest)", "Value (Lowest)"], key="tender_sort")
    
    # Apply search and filters
    display_df = tenders_df.copy()
    if search_query:
        mask = display_df.apply(lambda row: search_query.lower() in f"{row['title']} {row['entity']} {row['description']}".lower(), axis=1)
        display_df = display_df[mask]
    if status_filter != "All":
        display_df = display_df[display_df["status"] == status_filter]
    
    if sort_by == "Deadline (Nearest)":
        display_df = display_df.sort_values("deadline")
    elif sort_by == "Value (Highest)":
        display_df = display_df.sort_values("value_sar", ascending=False)
    else:
        display_df = display_df.sort_values("value_sar", ascending=True)
    
    # Tender Cards
    st.markdown(f"**{len(display_df)} tenders found**")
    for _, t in display_df.iterrows():
        status_class = {
            "Open": "badge-green",
            "Closing Soon": "badge-red",
            "Awarded": "badge-blue",
            "Closed": "badge-neutral",
        }.get(t["status"], "badge-neutral")
        
        status_emoji = {
            "Open": "🟢",
            "Closing Soon": "🔴",
            "Awarded": "🏆",
            "Closed": "⬛",
        }.get(t["status"], "⬜")
        
        deadline_str = t["deadline"].strftime("%b %d, %Y") if pd.notna(t["deadline"]) else "TBD"
        days_left_str = f"{t['days_left']}d left" if t["days_left"] > 0 else "Expired"
        
        st.markdown(f"""
        <div class="project-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <div class="project-name">{t['title']}</div>
                    <div class="project-developer">{t['entity']} • {t['region']}</div>
                </div>
                <span class="status-badge {status_class}">{status_emoji} {t['status']}</span>
            </div>
            <div style="font-size: 12px; color: #475569; margin: 8px 0; line-height: 1.5;">{t['description']}</div>
            <div class="project-stats">
                <div class="stat-item">
                    <div class="stat-label">Value</div>
                    <div class="stat-value" style="color: #C5A55A;">{format_sar(t['value_sar'])}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Deadline</div>
                    <div class="stat-value">{deadline_str}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Time Left</div>
                    <div class="stat-value" style="color: {'#DC2626' if t['days_left'] <= 14 else '#059669'};">{days_left_str}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Sector</div>
                    <div class="stat-value">{t['sector']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">ID</div>
                    <div class="stat-value" style="font-family: monospace; font-size: 12px;">{t['id']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# TAB 4: MEGA PROJECTS
# ═════════════════════════════════════════════
with tab4:
    render_section_header("🏗️", "Vision 2030 Mega Projects", "19 PROJECTS", "badge-navy")
    
    mega_df = get_megaprojects_data()
    mega_summary = get_megaprojects_summary(mega_df)
    opp_sectors = get_opportunity_sectors(mega_df)
    
    # KPI Row
    mk1, mk2, mk3, mk4 = st.columns(4)
    with mk1:
        render_kpi("Total Projects", str(mega_summary["total_projects"]),
                  f"{mega_summary['active_projects']} active", "navy")
    with mk2:
        render_kpi("Total Value", format_usd(mega_summary["total_value_usd"]),
                  format_sar(mega_summary["total_value_sar"]), "gold")
    with mk3:
        under_const = mega_summary["by_status"].get("Under Construction", 0)
        render_kpi("Under Construction", str(under_const), "Active builds", "blue")
    with mk4:
        render_kpi("Opportunity Sectors", str(len(opp_sectors)),
                  "Across all projects", "green")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig = sector_donut(mega_summary["by_status"], "Projects by Status")
        st.plotly_chart(fig, use_container_width=True, key="mega_status_donut")
    with chart_col2:
        fig = opportunity_treemap(dict(list(opp_sectors.items())[:15]), "Opportunity Sectors Heatmap")
        st.plotly_chart(fig, use_container_width=True, key="mega_opp_treemap")
    
    # Timeline
    render_section_header("📅", "Project Timeline", "2024-2039", "badge-blue")
    fig = timeline_chart(mega_df.sort_values("estimated_value_usd", ascending=True), "Mega Projects — Completion Timeline")
    st.plotly_chart(fig, use_container_width=True, key="mega_timeline")
    
    # Project Cards
    render_section_header("🌍", "Project Directory")
    
    # Search and filter
    m_search = st.text_input("🔍 Search projects", placeholder="e.g., NEOM, tourism, construction...", key="mega_search")
    
    display_mega = mega_df.copy()
    if m_search:
        mask = display_mega.apply(
            lambda row: m_search.lower() in f"{row['name']} {row['sector']} {row['opportunity_sectors']} {row['description']}".lower(),
            axis=1
        )
        display_mega = display_mega[mask]
    
    if selected_sector != "All":
        display_mega = display_mega[
            display_mega["sector"].str.contains(selected_sector, case=False, na=False) |
            display_mega["opportunity_sectors"].str.contains(selected_sector, case=False, na=False)
        ]
    
    # Display project cards
    for _, proj in display_mega.sort_values("estimated_value_usd", ascending=False).iterrows():
        status_colors = {
            "Under Construction": "#2563EB",
            "Operational": "#10B981",
            "Partially Operational": "#059669",
            "Planning / Design": "#F59E0B",
            "Operational / Expanding": "#0891B2",
        }
        status_color = status_colors.get(proj["status"], "#94A3B8")
        
        # Opportunity chips
        opp_chips = ""
        for opp in proj["opportunity_sectors"].split(",")[:6]:
            opp = opp.strip()
            opp_chips += f'<span style="display:inline-block; background:#F1F5F9; color:#475569; padding:3px 8px; border-radius:12px; font-size:10px; font-weight:600; margin:2px;">{opp}</span>'
        
        st.markdown(f"""
        <div class="project-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                <div>
                    <div class="project-name">{proj['name']}</div>
                    <div class="project-developer">{proj['developer']} • {proj['region']}</div>
                </div>
                <span class="status-badge" style="background:{status_color}15; color:{status_color}; border: 1px solid {status_color}30;">{proj['status']}</span>
            </div>
            <div style="font-size: 12px; color: #475569; margin: 8px 0; line-height: 1.5;">{proj['description']}</div>
            <div class="project-stats" style="margin: 12px 0;">
                <div class="stat-item">
                    <div class="stat-label">Estimated Value</div>
                    <div class="stat-value" style="color: #C5A55A;">{format_usd(proj['estimated_value_usd'])}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">SAR Value</div>
                    <div class="stat-value">{format_sar(proj['estimated_value_sar'])}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Completion</div>
                    <div class="stat-value">{proj['completion_year']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Phase</div>
                    <div class="stat-value" style="font-size: 12px;">{proj['phase']}</div>
                </div>
            </div>
            <div style="font-size: 11px; color: #8892B0; font-weight: 600; margin-bottom: 6px;">KEY STATS</div>
            <div style="font-size: 12px; color: #475569; margin-bottom: 10px;">{proj['key_stats']}</div>
            <div style="font-size: 11px; color: #8892B0; font-weight: 600; margin-bottom: 6px;">OPPORTUNITY SECTORS</div>
            <div>{opp_chips}</div>
            <div style="margin-top: 10px;">
                <a href="{proj['website']}" target="_blank" style="color: #C5A55A; font-size: 12px; font-weight: 600; text-decoration: none;">🔗 Visit Website →</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# TAB 5: LEAD TRACKER
# ═════════════════════════════════════════════
with tab5:
    render_section_header("👤", "Lead & Opportunity Tracker", "CRM", "badge-navy")
    
    leads = get_leads()
    pipeline = get_pipeline_summary(leads)
    
    # KPI Row
    lk1, lk2, lk3, lk4 = st.columns(4)
    with lk1:
        render_kpi("Total Leads", str(pipeline["total_leads"]),
                  f"{pipeline['active_leads']} active", "navy")
    with lk2:
        render_kpi("Pipeline Value", format_sar(pipeline["total_pipeline_value"]),
                  "Gross value", "gold")
    with lk3:
        render_kpi("Weighted Value", format_sar(pipeline["total_weighted_value"]),
                  "Probability adjusted", "green")
    with lk4:
        render_kpi("Avg Probability", f"{pipeline['avg_probability']:.0f}%",
                  "Across all leads", "blue")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Funnel Chart
    fig = pipeline_funnel(pipeline["stages"])
    st.plotly_chart(fig, use_container_width=True, key="leads_pipeline_funnel")
    
    # Add New Lead
    render_section_header("➕", "Add New Lead")
    with st.expander("📝 New Lead Form", expanded=False):
        with st.form("new_lead_form"):
            fc1, fc2 = st.columns(2)
            with fc1:
                new_company = st.text_input("Company Name*")
                new_contact = st.text_input("Contact Name*")
                new_title = st.text_input("Contact Title")
                new_email = st.text_input("Contact Email")
                new_sector = st.selectbox("Sector", ["Construction", "Technology", "Energy", "Healthcare",
                                                      "Tourism", "Defense", "Transport", "Finance", "Entertainment", "Education", "Water"])
            with fc2:
                new_region = st.selectbox("Region", ["Riyadh", "Jeddah", "Eastern Province", "Tabuk",
                                                     "Madinah", "Makkah", "KAEC", "Multiple"])
                new_opportunity = st.text_input("Opportunity Description*")
                new_value = st.number_input("Estimated Value (SAR)", min_value=0, step=1000000)
                new_probability = st.slider("Win Probability (%)", 0, 100, 30)
                new_stage = st.selectbox("Pipeline Stage", ["Prospect", "Qualified", "Proposal", "Negotiation"])
            
            new_source = st.text_input("Lead Source", placeholder="e.g., Etimad, LEAP Conference, Referral")
            new_notes = st.text_area("Notes", placeholder="Key conversation points, requirements, etc.")
            new_next_action = st.text_input("Next Action", placeholder="e.g., Send proposal by March 1")
            
            submitted = st.form_submit_button("💾 Save Lead", use_container_width=True)
            if submitted and new_company and new_opportunity:
                new_lead = {
                    "company": new_company,
                    "contact_name": new_contact,
                    "contact_title": new_title,
                    "contact_email": new_email,
                    "sector": new_sector,
                    "region": new_region,
                    "opportunity": new_opportunity,
                    "estimated_value_sar": new_value,
                    "probability": new_probability,
                    "stage": new_stage,
                    "source": new_source,
                    "notes": new_notes,
                    "next_action": new_next_action,
                }
                add_lead(new_lead)
                st.success(f"✅ Lead added: {new_company} — {new_opportunity}")
                st.rerun()
    
    # Lead Cards
    render_section_header("📇", "Active Leads", f"{len(leads)} leads", "badge-gold")
    
    # Sort leads by score
    leads_with_scores = [(lead, calculate_lead_score(lead)) for lead in leads]
    leads_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    for lead, score in leads_with_scores:
        stage_class = f"lead-{lead.get('stage', 'prospect').lower()}"
        score_class = "score-high" if score >= 70 else ("score-medium" if score >= 40 else "score-low")
        
        stage_emoji = {
            "Prospect": "🔍", "Qualified": "✅", "Proposal": "📄",
            "Negotiation": "🤝", "Won": "🏆", "Lost": "❌"
        }.get(lead.get("stage", ""), "⬜")
        
        st.markdown(f"""
        <div class="lead-card {stage_class}">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div class="score-circle {score_class}">{score}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 700; color: #0A192F; font-size: 14px;">{lead.get('company', 'N/A')}</div>
                    <div style="font-size: 12px; color: #64748B;">{lead.get('opportunity', '')}</div>
                    <div style="font-size: 11px; color: #8892B0; margin-top: 4px;">
                        👤 {lead.get('contact_name', 'N/A')} • {lead.get('contact_title', '')}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #C5A55A; font-size: 15px;">{format_sar(lead.get('estimated_value_sar', 0))}</div>
                    <div style="font-size: 11px; color: #64748B;">
                        {stage_emoji} {lead.get('stage', 'N/A')} • {lead.get('probability', 0)}% prob
                    </div>
                    <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">
                        📅 Last: {lead.get('last_contact', 'N/A')} • 🎯 {lead.get('next_action', 'N/A')[:40]}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Expand for details and actions
        with st.expander(f"📋 Details — {lead.get('company', '')}"):
            dc1, dc2 = st.columns(2)
            with dc1:
                st.markdown(f"**Sector:** {lead.get('sector', 'N/A')}")
                st.markdown(f"**Region:** {lead.get('region', 'N/A')}")
                st.markdown(f"**Source:** {lead.get('source', 'N/A')}")
                st.markdown(f"**Email:** {lead.get('contact_email', 'N/A')}")
            with dc2:
                st.markdown(f"**Created:** {lead.get('created', 'N/A')}")
                st.markdown(f"**Next Action:** {lead.get('next_action', 'N/A')}")
            
            st.markdown(f"**Notes:** {lead.get('notes', 'No notes')}")
            
            # Quick actions
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                new_stage = st.selectbox("Update Stage", ["Prospect", "Qualified", "Proposal", "Negotiation", "Won", "Lost"],
                                        index=["Prospect", "Qualified", "Proposal", "Negotiation", "Won", "Lost"].index(lead.get("stage", "Prospect")),
                                        key=f"stage_{lead['id']}")
                if st.button("Update Stage", key=f"btn_stage_{lead['id']}"):
                    update_lead(lead["id"], {"stage": new_stage})
                    st.success("Stage updated!")
                    st.rerun()
            with col_b:
                new_prob = st.slider("Update Probability", 0, 100, lead.get("probability", 0), key=f"prob_{lead['id']}")
                if st.button("Update Probability", key=f"btn_prob_{lead['id']}"):
                    update_lead(lead["id"], {"probability": new_prob})
                    st.success("Probability updated!")
                    st.rerun()
            with col_c:
                if st.button("🗑️ Delete Lead", key=f"del_{lead['id']}"):
                    delete_lead(lead["id"])
                    st.warning("Lead deleted.")
                    st.rerun()


# ═════════════════════════════════════════════
# TAB 6: AI INTELLIGENCE
# ═════════════════════════════════════════════
with tab6:
    render_section_header("🤖", "AI-Powered Market Intelligence", "BETA", "badge-navy")
    
    ai_col1, ai_col2 = st.columns([2, 1])
    
    with ai_col2:
        available_sectors = get_available_sectors()
        selected_ai_sector = st.selectbox("Select Sector", available_sectors, key="ai_sector")
        
        custom_query = st.text_area("Custom Intelligence Query (optional)",
                                    placeholder="e.g., What are the latest construction tenders for data centers in Riyadh?",
                                    height=100, key="custom_ai_query")
        
        fetch_btn = st.button("🔍 Generate Intelligence Report", use_container_width=True)
        
        st.markdown("---")
        
        # Info box
        has_key = bool(gemini_key)
        if has_key:
            st.success("🤖 **AI Mode: Live Search**\nUsing Gemini + Google Search for real-time intelligence with grounded citations.")
        else:
            st.info("📚 **AI Mode: Curated Database**\nUsing pre-built intelligence reports. Add a Gemini API key in the sidebar for live AI search.")
    
    with ai_col1:
        # Auto-fetch or fetch on button click
        if fetch_btn or "ai_data" not in st.session_state:
            query = custom_query if custom_query else None
            with st.spinner("🔍 Analyzing Saudi market intelligence..."):
                intel = get_ai_intelligence(selected_ai_sector, query)
            st.session_state["ai_data"] = intel
        else:
            intel = st.session_state.get("ai_data", get_ai_intelligence(selected_ai_sector))
        
        # Render Intelligence Panel
        st.markdown(f"""
        <div class="intel-panel">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h3>{intel.get('title', 'Market Intelligence Report')}</h3>
                <span style="font-size: 10px; color: #8892B0;">{intel.get('powered_by', 'Unknown')} • {intel.get('fetched_at', '')}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Insights
        insights = intel.get("insights", [])
        for i, insight in enumerate(insights):
            st.markdown(f"""
            <div class="insight-item">
                <span style="color: #C5A55A; font-weight: 700; margin-right: 8px;">#{i+1}</span>
                {insight}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Key Opportunities
        opps = intel.get("key_opportunities", [])
        if opps:
            render_section_header("🎯", "Key Opportunities Identified")
            opp_cols = st.columns(min(len(opps), 3))
            for i, opp in enumerate(opps):
                with opp_cols[i % 3]:
                    st.markdown(f"""
                    <div style="background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; text-align: center;">
                        <div style="font-size: 20px; margin-bottom: 6px;">💡</div>
                        <div style="font-size: 13px; font-weight: 600; color: #0A192F;">{opp}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Risk Factors
        risks = intel.get("risk_factors", [])
        if risks:
            render_section_header("⚠️", "Risk Factors")
            for risk in risks:
                st.markdown(f"""
                <div style="background: #FEF2F2; border-left: 3px solid #EF4444; border-radius: 0 8px 8px 0; padding: 10px 16px; margin-bottom: 6px; font-size: 13px; color: #7F1D1D;">
                    ⚠️ {risk}
                </div>
                """, unsafe_allow_html=True)
        
        # Sources
        sources = intel.get("sources", [])
        if sources:
            render_section_header("📎", "Sources & References")
            for src in sources:
                uri = src.get("uri", "#")
                title = src.get("title", "Source")
                st.markdown(f"""
                <div style="padding: 6px 0;">
                    <a href="{uri}" target="_blank" class="source-link" style="color: #2563EB; text-decoration: none; font-size: 13px;">
                        🔗 {title}
                    </a>
                    <span style="color: #94A3B8; font-size: 11px; margin-left: 8px;">{uri[:60]}...</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Error notice
        if "error" in intel:
            st.warning(intel["error"])
