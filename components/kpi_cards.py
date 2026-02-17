"""
Premium KPI Card Components
Saudi Royal theme: Deep Navy + Gold accents.
"""
import streamlit as st


def inject_card_styles():
    """Inject premium CSS for KPI cards and global dashboard styling."""
    st.markdown("""
    <style>
        /* ===== GLOBAL THEME ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@600;700;800&display=swap');
        
        .stApp {
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ===== DASHBOARD HEADER ===== */
        .dashboard-header {
            background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #1A365D 100%);
            padding: 28px 32px;
            border-radius: 16px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }
        .dashboard-header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(197,165,90,0.08) 0%, transparent 70%);
            border-radius: 50%;
        }
        .dashboard-header h1 {
            font-family: 'Playfair Display', serif;
            color: #C5A55A;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 4px 0;
            letter-spacing: 0.5px;
        }
        .dashboard-header p {
            color: #8892B0;
            font-size: 14px;
            margin: 0;
            font-weight: 400;
        }
        .dashboard-header .date-badge {
            color: #C5A55A;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: 8px;
        }
        
        /* ===== KPI CARDS ===== */
        .kpi-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 20px 24px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .kpi-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }
        .kpi-card .accent-bar {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
        }
        .kpi-card .kpi-label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: #8892B0;
            margin-bottom: 8px;
        }
        .kpi-card .kpi-value {
            font-size: 28px;
            font-weight: 800;
            color: #0A192F;
            line-height: 1.1;
            margin-bottom: 4px;
        }
        .kpi-card .kpi-sub {
            font-size: 12px;
            color: #64748B;
            font-weight: 500;
        }
        
        /* Color variants */
        .kpi-navy .accent-bar { background: linear-gradient(90deg, #0A192F, #1A365D); }
        .kpi-gold .accent-bar { background: linear-gradient(90deg, #C5A55A, #D4AF37); }
        .kpi-green .accent-bar { background: linear-gradient(90deg, #059669, #10B981); }
        .kpi-blue .accent-bar { background: linear-gradient(90deg, #2563EB, #3B82F6); }
        .kpi-red .accent-bar { background: linear-gradient(90deg, #DC2626, #EF4444); }
        .kpi-purple .accent-bar { background: linear-gradient(90deg, #7C3AED, #8B5CF6); }
        
        /* ===== SECTION HEADERS ===== */
        .section-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 28px 0 16px 0;
            padding-bottom: 12px;
            border-bottom: 2px solid #E2E8F0;
        }
        .section-header .icon-box {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        .section-header h2 {
            font-size: 18px;
            font-weight: 700;
            color: #0A192F;
            margin: 0;
        }
        .section-header .badge {
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            margin-left: auto;
        }
        
        /* ===== NEWS CARDS ===== */
        .news-card {
            background: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            transition: all 0.2s ease;
        }
        .news-card:hover {
            border-color: #C5A55A;
            box-shadow: 0 2px 8px rgba(197,165,90,0.12);
        }
        .news-card .news-title {
            font-size: 14px;
            font-weight: 600;
            color: #0A192F;
            margin-bottom: 6px;
            line-height: 1.4;
        }
        .news-card .news-title a {
            color: #0A192F;
            text-decoration: none;
        }
        .news-card .news-title a:hover {
            color: #C5A55A;
        }
        .news-card .news-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 11px;
            color: #64748B;
            margin-bottom: 8px;
        }
        .news-card .news-summary {
            font-size: 12px;
            color: #475569;
            line-height: 1.5;
        }
        
        /* ===== BADGES ===== */
        .badge-positive { background: #ECFDF5; color: #059669; }
        .badge-negative { background: #FEF2F2; color: #DC2626; }
        .badge-neutral { background: #F1F5F9; color: #475569; }
        .badge-gold { background: #FEF3C7; color: #B45309; }
        .badge-blue { background: #EFF6FF; color: #2563EB; }
        .badge-green { background: #ECFDF5; color: #059669; }
        .badge-red { background: #FEF2F2; color: #DC2626; }
        .badge-navy { background: #0A192F; color: #C5A55A; }
        
        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        
        /* ===== PROJECT CARDS ===== */
        .project-card {
            background: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 20px 24px;
            margin-bottom: 16px;
            transition: all 0.2s ease;
            position: relative;
        }
        .project-card:hover {
            border-color: #C5A55A;
            box-shadow: 0 4px 16px rgba(10,25,47,0.08);
        }
        .project-card .project-name {
            font-size: 16px;
            font-weight: 700;
            color: #0A192F;
            margin-bottom: 4px;
        }
        .project-card .project-developer {
            font-size: 12px;
            color: #64748B;
            margin-bottom: 12px;
        }
        .project-card .project-stats {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }
        .project-card .stat-item {
            font-size: 11px;
        }
        .project-card .stat-label {
            color: #8892B0;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .project-card .stat-value {
            color: #0A192F;
            font-weight: 700;
            font-size: 14px;
        }
        
        /* ===== LEAD CARDS ===== */
        .lead-card {
            background: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 10px;
            border-left: 4px solid;
            transition: all 0.2s ease;
        }
        .lead-card:hover {
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }
        .lead-prospect { border-left-color: #94A3B8; }
        .lead-qualified { border-left-color: #3B82F6; }
        .lead-proposal { border-left-color: #F59E0B; }
        .lead-negotiation { border-left-color: #8B5CF6; }
        .lead-won { border-left-color: #10B981; }
        .lead-lost { border-left-color: #EF4444; }
        
        /* ===== INTELLIGENCE PANEL ===== */
        .intel-panel {
            background: linear-gradient(135deg, #0A192F 0%, #112240 100%);
            border-radius: 14px;
            padding: 24px;
            color: #E2E8F0;
            margin-bottom: 16px;
        }
        .intel-panel h3 {
            color: #C5A55A;
            font-family: 'Playfair Display', serif;
            font-size: 18px;
            margin-bottom: 16px;
        }
        .intel-panel .insight-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            font-size: 13px;
            line-height: 1.6;
            color: #CBD5E1;
        }
        .intel-panel .insight-item:last-child {
            border-bottom: none;
        }
        .intel-panel .source-link {
            color: #C5A55A;
            text-decoration: none;
            font-size: 12px;
        }
        .intel-panel .source-link:hover {
            text-decoration: underline;
        }
        
        /* ===== TENDER TABLE ===== */
        .tender-row {
            background: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 16px;
            transition: all 0.2s ease;
        }
        .tender-row:hover {
            border-color: #C5A55A;
            background: #FFFBEB;
        }
        
        /* ===== SCORE INDICATOR ===== */
        .score-circle {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 800;
            color: white;
        }
        .score-high { background: linear-gradient(135deg, #059669, #10B981); }
        .score-medium { background: linear-gradient(135deg, #D97706, #F59E0B); }
        .score-low { background: linear-gradient(135deg, #DC2626, #EF4444); }
        
        /* ===== SIDEBAR STYLING ===== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A192F 0%, #112240 100%);
        }
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown label,
        section[data-testid="stSidebar"] .stMarkdown h1,
        section[data-testid="stSidebar"] .stMarkdown h2,
        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: #E2E8F0 !important;
        }
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: #F8FAFC;
            padding: 4px;
            border-radius: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
        }
        .stTabs [aria-selected="true"] {
            background: #0A192F !important;
            color: #C5A55A !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the premium dashboard header."""
    from datetime import datetime
    now = datetime.now()
    st.markdown(f"""
    <div class="dashboard-header">
        <h1>🇸🇦 Saudi Market Intelligence</h1>
        <p>Research Opportunities & Lead Generation Platform</p>
        <div class="date-badge">📅 {now.strftime('%A, %B %d, %Y')} • Live Intelligence</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi(label: str, value: str, sub: str = "", variant: str = "navy"):
    """Render a premium KPI card."""
    st.markdown(f"""
    <div class="kpi-card kpi-{variant}">
        <div class="accent-bar"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(icon: str, title: str, badge_text: str = "", badge_class: str = "badge-gold"):
    """Render a styled section header."""
    badge_html = f'<span class="badge {badge_class}">{badge_text}</span>' if badge_text else ""
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size: 22px;">{icon}</span>
        <h2>{title}</h2>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def format_sar(value: float) -> str:
    """Format SAR currency values."""
    if value >= 1e12:
        return f"SAR {value/1e12:.1f}T"
    elif value >= 1e9:
        return f"SAR {value/1e9:.1f}B"
    elif value >= 1e6:
        return f"SAR {value/1e6:.0f}M"
    elif value >= 1e3:
        return f"SAR {value/1e3:.0f}K"
    return f"SAR {value:,.0f}"


def format_usd(value: float) -> str:
    """Format USD currency values."""
    if value >= 1e12:
        return f"${value/1e12:.1f}T"
    elif value >= 1e9:
        return f"${value/1e9:.0f}B"
    elif value >= 1e6:
        return f"${value/1e6:.0f}M"
    elif value >= 1e3:
        return f"${value/1e3:.0f}K"
    return f"${value:,.0f}"
