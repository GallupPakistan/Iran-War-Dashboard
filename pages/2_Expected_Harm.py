import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="Expected Personal Harm | Iran Poll", page_icon="💥", layout="wide")

# ══════════════════════════════════════════════════════════════════
# STYLING
# ══════════════════════════════════════════════════════════════════

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#ef4444 0%,#dc2626 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #ef4444;padding-bottom:0.5rem;}
.insight-box{background:#fee2e2;border-left:5px solid #dc2626;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#7f1d1d;}
.insight-box strong{color:#991b1b;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:#002147;padding:.4rem;border-radius:12px;}
.stTabs [data-baseweb="tab"]{height:46px;padding:0 22px;background:rgba(255,255,255,.1);border-radius:9px;color:#90b8e8 !important;font-weight:700;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%) !important;color:white !important;font-weight:800 !important;}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    df = pd.read_excel("Iran_Snap_Poll_2026_-_Merged_Data_Working_File__17_Countries_.xlsx")
    
    # CountryID is already the country name in new data
    df["Country"] = df["CountryID"]
    # Armenia was screened via survey invitation (Q1 implicit Yes) - fill for correct analysis
    df.loc[df["CountryID"] == "Armenia", "Q1"] = "Yes"
    return df

df = load_data()

# ══════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-title">💥 Expected Personal Harm Analysis</div>
    <div class="hero-sub">Physical, financial, and emotional impact expectations if the war continues</div>
</div>
""", unsafe_allow_html=True)

# Data availability note
st.markdown("""
<div style="background:#e0f2fe;border-left:5px solid #028090;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;">
<strong>📊 Data Availability:</strong> Q3 was asked in <strong>11 out of 17 countries</strong>. Not asked in: Colombia, Croatia, Serbia, Slovenia. Charts below show only countries with data.
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Question 3:** *If this war continues, do you expect personal harm physically, financially or emotionally to yourself?*

**Response Options:**
- 1 = Strong harm expected
- 2 = Minor harm
- 3 = No harm
- 9 = Don't know / No response
""")

# ══════════════════════════════════════════════════════════════════
# FILTERS
# ══════════════════════════════════════════════════════════════════

st.sidebar.markdown("### 🌍 Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=sorted(df["Country"].dropna().unique()),
    default=sorted(df["Country"].dropna().unique())
)

df_filtered = df[df["Country"].isin(selected_countries)] if selected_countries else df

st.sidebar.metric("📊 Filtered Sample", f"{len(df_filtered):,}")
st.sidebar.metric("⚖️ Weighted N", f"{int(df_filtered['WGT'].sum()):,}")

# ══════════════════════════════════════════════════════════════════
# OVERALL HARM EXPECTATIONS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Overall Harm Expectations</div>', unsafe_allow_html=True)

harm_types = {
    'Q3_1': {'name': '🤕 Physical Harm', 'color': '#dc2626'},
    'Q3_2': {'name': '💰 Financial Harm', 'color': '#f59e0b'},
    'Q3_3': {'name': '😰 Emotional Harm', 'color': '#8b5cf6'}
}

# Calculate overall percentages
harm_summary = []

for q_code, info in harm_types.items():
    q_data = df_filtered[df_filtered[q_code].notna()]
    total_wgt = q_data['WGT'].sum()
    
    strong_wgt = q_data[q_data[q_code] == 'Strong harm expected']['WGT'].sum()
    minor_wgt = q_data[q_data[q_code] == 'Minor harm']['WGT'].sum()
    no_harm_wgt = q_data[q_data[q_code] == 'No harm expected']['WGT'].sum()
    
    harm_summary.append({
        'Type': info['name'],
        'Strong Harm': (strong_wgt / total_wgt * 100) if total_wgt > 0 else 0,
        'Minor Harm': (minor_wgt / total_wgt * 100) if total_wgt > 0 else 0,
        'No Harm': (no_harm_wgt / total_wgt * 100) if total_wgt > 0 else 0
    })

harm_df = pd.DataFrame(harm_summary)

# Metrics
col1, col2, col3 = st.columns(3)

for idx, (col, row) in enumerate(zip([col1, col2, col3], harm_summary)):
    with col:
        st.metric(
            row['Type'],
            f"{row['Strong Harm']:.1f}%",
            "Strong harm expected",
            delta_color="inverse"
        )

# Chart 1: Stacked Bar Comparison
st.markdown("#### ⚖️ Harm Expectation Comparison")

fig = go.Figure()

fig.add_trace(go.Bar(
    name='Strong Harm',
    y=harm_df['Type'],
    x=harm_df['Strong Harm'],
    orientation='h',
    marker_color='#dc2626',
    text=[f"{v:.1f}%" for v in harm_df['Strong Harm']],
    textposition='inside'
))

fig.add_trace(go.Bar(
    name='Minor Harm',
    y=harm_df['Type'],
    x=harm_df['Minor Harm'],
    orientation='h',
    marker_color='#f59e0b',
    text=[f"{v:.1f}%" for v in harm_df['Minor Harm']],
    textposition='inside'
))

fig.add_trace(go.Bar(
    name='No Harm',
    y=harm_df['Type'],
    x=harm_df['No Harm'],
    orientation='h',
    marker_color='#10b981',
    text=[f"{v:.1f}%" for v in harm_df['No Harm']],
    textposition='inside'
))

fig.update_layout(
    barmode='stack',
    title="Expected Harm Across All Three Dimensions",
    xaxis_title="Percentage (%)",
    height=400,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# DETAILED ANALYSIS BY HARM TYPE (TABS)
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔍 Detailed Analysis by Harm Type</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🤕 Physical Harm", "💰 Financial Harm", "😰 Emotional Harm"])

for tab, (q_code, info) in zip([tab1, tab2, tab3], harm_types.items()):
    with tab:
        st.markdown(f"### {info['name']}")
        
        # Country-by-country analysis
        country_harm = []
        
        for country in sorted(df_filtered['Country'].dropna().unique()):
            cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered[q_code].notna())]
            
            if len(cdf) > 0:
                c_total = cdf['WGT'].sum()
                
                country_harm.append({
                    'Country': country,
                    'Strong Harm %': (cdf[cdf[q_code] == 'Strong harm expected']['WGT'].sum() / c_total * 100) if c_total > 0 else 0,
                    'Minor Harm %': (cdf[cdf[q_code] == 'Minor harm']['WGT'].sum() / c_total * 100) if c_total > 0 else 0,
                    'No Harm %': (cdf[cdf[q_code] == 'No harm expected']['WGT'].sum() / c_total * 100) if c_total > 0 else 0,
                    'Sample': len(cdf)
                })
        
        if country_harm:
            country_df = pd.DataFrame(country_harm).sort_values('Strong Harm %', ascending=False)
            
            # Chart: Strong harm by country
            st.markdown("#### Countries Expecting Strong Harm")
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=country_df['Country'],
                x=country_df['Strong Harm %'],
                orientation='h',
                marker_color=info['color'],
                text=[f"{v:.1f}%" for v in country_df['Strong Harm %']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>%{x:.1f}%<br>Sample: %{customdata:,}<extra></extra>',
                customdata=country_df['Sample']
            ))
            
            fig.update_layout(
                title=f"% Expecting Strong {info['name'].split()[-1]}",
                xaxis_title="Percentage (%)",
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Stacked bar by country
            st.markdown("#### Complete Breakdown by Country")
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Strong Harm',
                y=country_df['Country'],
                x=country_df['Strong Harm %'],
                orientation='h',
                marker_color='#dc2626'
            ))
            
            fig.add_trace(go.Bar(
                name='Minor Harm',
                y=country_df['Country'],
                x=country_df['Minor Harm %'],
                orientation='h',
                marker_color='#f59e0b'
            ))
            
            fig.add_trace(go.Bar(
                name='No Harm',
                y=country_df['Country'],
                x=country_df['No Harm %'],
                orientation='h',
                marker_color='#10b981'
            ))
            
            fig.update_layout(
                barmode='stack',
                title=f"{info['name']} Expectations by Country",
                xaxis_title="Percentage (%)",
                height=600,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.dataframe(
                country_df.round(1),
                use_container_width=True,
                hide_index=True
            )

# ══════════════════════════════════════════════════════════════════
# COMPOSITE HARM INDEX
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📈 Composite Harm Index</div>', unsafe_allow_html=True)

st.markdown("**Composite Score:** Average of strong harm expectations across all three dimensions")

composite_scores = []

for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[df_filtered['Country'] == country]
    
    # Check if country has Q3 data
    has_data = cdf['Q3_1'].notna().any() or cdf['Q3_2'].notna().any() or cdf['Q3_3'].notna().any()
    
    if not has_data:
        continue  # Skip countries with no Q3 data
    
    scores = []
    for q_code in ['Q3_1', 'Q3_2', 'Q3_3']:
        q_data = cdf[cdf[q_code].notna()]
        total = q_data['WGT'].sum()
        strong = q_data[q_data[q_code] == 'Strong harm expected']['WGT'].sum()
        pct = (strong / total * 100) if total > 0 else 0
        scores.append(pct)
    
    composite_scores.append({
        'Country': country,
        'Composite Score': sum(scores) / 3,
        'Physical': scores[0],
        'Financial': scores[1],
        'Emotional': scores[2]
    })

composite_df = pd.DataFrame(composite_scores).sort_values('Composite Score', ascending=False)

# Composite index chart
fig = go.Figure()

fig.add_trace(go.Bar(
    y=composite_df['Country'],
    x=composite_df['Composite Score'],
    orientation='h',
    marker=dict(
        color=composite_df['Composite Score'],
        colorscale='Reds',
        showscale=True,
        colorbar=dict(title="Score")
    ),
    text=[f"{v:.1f}" for v in composite_df['Composite Score']],
    textposition='outside'
))

fig.update_layout(
    title="Composite Harm Index (Average Across All Three Types)",
    xaxis_title="Composite Score",
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

if len(composite_df) > 0:
    st.markdown('<div class="insight-box"><strong>💡 Key Insight:</strong> ' + 
                f"{composite_df.iloc[0]['Country']} has the highest composite harm expectation at {composite_df.iloc[0]['Composite Score']:.1f}, " +
                f"while {composite_df.iloc[-1]['Country']} has the lowest at {composite_df.iloc[-1]['Composite Score']:.1f}.</div>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# HEATMAP
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔥 Harm Expectations Heatmap</div>', unsafe_allow_html=True)

import numpy as np

heatmap_data = composite_df[['Physical', 'Financial', 'Emotional']].values

fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=['Physical', 'Financial', 'Emotional'],
    y=composite_df['Country'],
    colorscale='Reds',
    text=heatmap_data.round(1),
    texttemplate='%{text:.1f}%',
    textfont={"size": 11},
    colorbar=dict(title="% Strong<br>Harm")
))

fig.update_layout(
    title="Strong Harm Expectations: All Countries × All Types",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# DEMOGRAPHIC ANALYSIS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">👥 Demographics of Concern</div>', unsafe_allow_html=True)

# By Gender
st.markdown("#### 👫 Expected Harm by Gender")

gender_data = []
for gender_label in ['Male', 'Female']:
    gdf = df_filtered[df_filtered['D1'] == gender_label]
    
    for q_code, info in harm_types.items():
        q_data = gdf[gdf[q_code].notna()]
        total = q_data['WGT'].sum()
        strong = q_data[q_data[q_code] == 'Strong harm expected']['WGT'].sum()
        
        if total > 0:
            gender_data.append({
                'Gender': gender_label,
                'Harm Type': info['name'],
                'Strong Harm %': (strong / total * 100)
            })

if gender_data:
    gender_df = pd.DataFrame(gender_data)
    
    fig = go.Figure()
    
    for gender in ['Male', 'Female']:
        data = gender_df[gender_df['Gender'] == gender]
        fig.add_trace(go.Bar(
            name=gender,
            x=data['Harm Type'],
            y=data['Strong Harm %'],
            text=[f"{v:.1f}%" for v in data['Strong Harm %']],
            textposition='outside'
        ))
    
    fig.update_layout(
        barmode='group',
        title="Strong Harm Expectations by Gender",
        yaxis_title="Percentage (%)",
        height=400,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#7f1d1d 0%,#991b1b 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · Expected Personal Harm Analysis</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
