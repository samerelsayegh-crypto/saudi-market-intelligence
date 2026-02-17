"""
Chart Factory for Saudi Market Intelligence Dashboard
Plotly-based visualizations with Saudi Royal theme.
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Theme colors
NAVY = "#0A192F"
GOLD = "#C5A55A"
LIGHT_GOLD = "#D4AF37"
SLATE = "#475569"
LIGHT_SLATE = "#8892B0"
WHITE = "#FFFFFF"
BG = "#F8FAFC"

SECTOR_COLORS = [
    "#0A192F", "#C5A55A", "#2563EB", "#059669", "#DC2626",
    "#7C3AED", "#D97706", "#0891B2", "#BE185D", "#65A30D",
    "#6366F1", "#EA580C", "#0D9488", "#9333EA",
]

CHART_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color=SLATE),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(
        bgcolor=NAVY,
        font_size=12,
        font_color=WHITE,
        bordercolor=GOLD,
    ),
)


def sector_donut(data: dict, title: str = "Distribution by Sector") -> go.Figure:
    """Create a premium donut chart for sector distribution."""
    labels = list(data.keys())
    values = list(data.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=SECTOR_COLORS[:len(labels)], line=dict(color=WHITE, width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, family="Inter"),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
    )])
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=14, color=NAVY, family="Inter")),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        height=380,
    )
    
    return fig


def value_bar(data: dict, title: str = "Value by Region", orientation: str = "h", color: str = GOLD) -> go.Figure:
    """Create a horizontal/vertical bar chart for value distribution."""
    labels = list(data.keys())
    values = list(data.values())
    
    if orientation == "h":
        fig = go.Figure(data=[go.Bar(
            y=labels,
            x=values,
            orientation="h",
            marker=dict(
                color=values,
                colorscale=[[0, "#1A365D"], [0.5, GOLD], [1, LIGHT_GOLD]],
                line=dict(color=NAVY, width=0.5),
                cornerradius=4,
            ),
            hovertemplate="<b>%{y}</b><br>Value: %{x:,.0f}<extra></extra>",
        )])
    else:
        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker=dict(
                color=values,
                colorscale=[[0, "#1A365D"], [0.5, GOLD], [1, LIGHT_GOLD]],
                line=dict(color=NAVY, width=0.5),
                cornerradius=4,
            ),
            hovertemplate="<b>%{x}</b><br>Value: %{y:,.0f}<extra></extra>",
        )])
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=14, color=NAVY)),
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
        yaxis=dict(showgrid=False),
        height=380,
    )
    
    return fig


def pipeline_funnel(stage_data: dict) -> go.Figure:
    """Create a pipeline funnel chart for lead stages."""
    stages = ["Prospect", "Qualified", "Proposal", "Negotiation", "Won"]
    values = [stage_data.get(s, {}).get("count", 0) for s in stages]
    
    colors = ["#94A3B8", "#3B82F6", "#F59E0B", "#8B5CF6", "#10B981"]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        marker=dict(
            color=colors,
            line=dict(color=WHITE, width=2),
        ),
        connector=dict(line=dict(color="#E2E8F0", width=1)),
        hovertemplate="<b>%{y}</b><br>Leads: %{x}<br>Conversion: %{percentInitial}<extra></extra>",
    ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Lead Pipeline Funnel", font=dict(size=14, color=NAVY)),
        height=350,
    )
    
    return fig


def timeline_chart(df, title: str = "Project Timeline") -> go.Figure:
    """Create a Gantt-style timeline for mega projects."""
    import pandas as pd
    
    fig = go.Figure()
    
    status_colors = {
        "Under Construction": "#2563EB",
        "Operational": "#10B981",
        "Partially Operational": "#059669",
        "Planning / Design": "#F59E0B",
        "Operational / Expanding": "#0891B2",
    }
    
    for _, row in df.iterrows():
        color = status_colors.get(row["status"], "#94A3B8")
        fig.add_trace(go.Bar(
            x=[row["completion_year"] - 2024],
            y=[row["name"]],
            orientation="h",
            marker=dict(color=color, cornerradius=6, line=dict(color=WHITE, width=1)),
            text=f"{row['completion_year']}",
            textposition="inside",
            hovertemplate=f"<b>{row['name']}</b><br>Status: {row['status']}<br>Target: {row['completion_year']}<br>Value: {row['estimated_value_usd']/1e9:.0f}B USD<extra></extra>",
            showlegend=False,
        ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=14, color=NAVY)),
        xaxis=dict(title="Years from 2024", showgrid=True, gridcolor="#E2E8F0"),
        yaxis=dict(showgrid=False, autorange="reversed"),
        height=max(400, len(df) * 30),
        bargap=0.3,
    )
    
    return fig


def sentiment_gauge(positive: int, neutral: int, negative: int) -> go.Figure:
    """Create a sentiment breakdown bar."""
    total = positive + neutral + negative
    if total == 0:
        total = 1
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[positive], y=["Sentiment"],
        orientation="h", name="Positive",
        marker=dict(color="#10B981", cornerradius=4),
        text=f"😊 {positive}",
        textposition="inside",
    ))
    fig.add_trace(go.Bar(
        x=[neutral], y=["Sentiment"],
        orientation="h", name="Neutral",
        marker=dict(color="#94A3B8", cornerradius=4),
        text=f"😐 {neutral}",
        textposition="inside",
    ))
    fig.add_trace(go.Bar(
        x=[negative], y=["Sentiment"],
        orientation="h", name="Negative",
        marker=dict(color="#EF4444", cornerradius=4),
        text=f"😟 {negative}",
        textposition="inside",
    ))
    
    layout_overrides = {k: v for k, v in CHART_LAYOUT.items() if k != "margin"}
    fig.update_layout(
        **layout_overrides,
        barmode="stack",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
        height=120,
        margin=dict(l=10, r=10, t=10, b=40),
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False),
    )
    
    return fig


def opportunity_treemap(data: dict, title: str = "Opportunity Sectors Heatmap") -> go.Figure:
    """Create a treemap showing opportunities across sectors."""
    labels = list(data.keys())
    values = list(data.values())
    parents = ["" for _ in labels]
    
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        textinfo="label+value",
        marker=dict(
            colors=values,
            colorscale=[[0, "#1A365D"], [0.3, "#2563EB"], [0.6, GOLD], [1, LIGHT_GOLD]],
            line=dict(color=WHITE, width=2),
            cornerradius=6,
        ),
        hovertemplate="<b>%{label}</b><br>Project mentions: %{value}<extra></extra>",
    ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=14, color=NAVY)),
        height=400,
    )
    
    return fig


def tender_value_by_sector(data: dict, title: str = "Tender Value by Sector (SAR)") -> go.Figure:
    """Bar chart of tender values grouped by sector."""
    sectors = list(data.keys())
    values = [v / 1e9 for v in data.values()]  # Convert to billions
    
    fig = go.Figure(data=[go.Bar(
        x=sectors,
        y=values,
        marker=dict(
            color=SECTOR_COLORS[:len(sectors)],
            cornerradius=6,
            line=dict(color=WHITE, width=1),
        ),
        text=[f"{v:.1f}B" for v in values],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Value: SAR %{y:.1f}B<extra></extra>",
    )])
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=14, color=NAVY)),
        yaxis=dict(title="SAR (Billions)", showgrid=True, gridcolor="#E2E8F0"),
        xaxis=dict(showgrid=False),
        height=380,
    )
    
    return fig
