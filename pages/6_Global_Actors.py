import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(page_title="Global Actors' Policies | Iran Poll", page_icon="🌐", layout="wide")

# ══════════════════════════════════════════════════════════════════
# STYLING
# ══════════════════════════════════════════════════════════════════

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#10b981 0%,#059669 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid#10b981;padding-bottom:0.5rem;}
.insight-box{background:#d1fae5;border-left:5px solid #059669;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#065f46;}
.insight-box strong{color:#064e3b;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:#002147;padding:.4rem;border-radius:12px;}
.stTabs [data-baseweb="tab"]{height:46px;padding:0 22px;background:rgba(255,255,255,.1);border-radius:9px;color:#90b8e8 !important;font-weight:700;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#10b981 0%,#059669 100%) !important;color:white !important;font-weight:800 !important;}
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
    <div class="hero-title">🌐 Global Actors' Policies Analysis</div>
    <div class="hero-sub">Satisfaction with UN, EU, major powers, and regional actors' responses to the war</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Question 8:** *Are you on the whole, satisfied or dissatisfied with the policy and actions of the following on this war?*

**Actors Evaluated:** UN, EU, UK, France, Russia, China, Turkey, Arab Countries, Spain
""")

# Data availability note
st.markdown("""
<div style="background:#e0f2fe;border-left:5px solid #028090;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;">
<strong>📊 Data Availability:</strong> Q8 was asked in <strong>11 out of 17 countries</strong>. Not asked in: Colombia, Croatia, Serbia, Slovenia.
</div>
""", unsafe_allow_html=True)

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
# ACTOR MAPPING
# ══════════════════════════════════════════════════════════════════

actors = {
    'Q8_1': {'name': '🇺🇳 United Nations', 'short': 'UN'},
    'Q8_2': {'name': '🇪🇺 European Union', 'short': 'EU'},
    'Q8_3': {'name': '🇬🇧 United Kingdom', 'short': 'UK'},
    'Q8_4': {'name': '🇫🇷 France', 'short': 'France'},
    'Q8_5': {'name': '🇷🇺 Russia', 'short': 'Russia'},
    'Q8_6': {'name': '🇨🇳 China', 'short': 'China'},
    'Q8_7': {'name': '🇹🇷 Turkey', 'short': 'Turkey'},
    'Q8_8': {'name': '🌍 Arab Countries', 'short': 'Arab Countries'},
    'Q8_9': {'name': '🇪🇸 Spain', 'short': 'Spain'}
}

# ══════════════════════════════════════════════════════════════════
# OVERALL SATISFACTION SUMMARY
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Overall Satisfaction Summary</div>', unsafe_allow_html=True)

satisfaction_summary = []

for q_code, actor_info in actors.items():
    satisfied_wgt = df_filtered[df_filtered[q_code] == 'Satisfied']['WGT'].sum()
    dissatisfied_wgt = df_filtered[df_filtered[q_code] == 'Dissatisfied']['WGT'].sum()
    
    total = satisfied_wgt + dissatisfied_wgt
    
    satisfaction_summary.append({
        'Actor': actor_info['short'],
        'Satisfied %': (satisfied_wgt / total * 100) if total > 0 else 0,
        'Dissatisfied %': (dissatisfied_wgt / total * 100) if total > 0 else 0,
        'Net Satisfaction': ((satisfied_wgt - dissatisfied_wgt) / total * 100) if total > 0 else 0
    })

summary_df = pd.DataFrame(satisfaction_summary).sort_values('Net Satisfaction', ascending=False)

# Metrics row
cols = st.columns(3)
with cols[0]:
    top_actor = summary_df.iloc[0]
    st.metric(
        "🏆 Most Satisfied With",
        top_actor['Actor'],
        f"+{top_actor['Net Satisfaction']:.1f}% net"
    )

with cols[1]:
    bottom_actor = summary_df.iloc[-1]
    st.metric(
        "📉 Least Satisfied With",
        bottom_actor['Actor'],
        f"{bottom_actor['Net Satisfaction']:.1f}% net",
        delta_color="inverse"
    )

with cols[2]:
    avg_net = summary_df['Net Satisfaction'].mean()
    st.metric(
        "📊 Average Net Satisfaction",
        f"{avg_net:.1f}%"
    )

# Chart 1: Net Satisfaction Rankings
st.markdown("#### 🏆 Net Satisfaction Rankings")

colors = ['#10b981' if x >= 0 else '#ef4444' for x in summary_df['Net Satisfaction']]

fig = go.Figure()
fig.add_trace(go.Bar(
    y=summary_df['Actor'],
    x=summary_df['Net Satisfaction'],
    orientation='h',
    marker_color=colors,
    text=[f"{v:+.1f}%" for v in summary_df['Net Satisfaction']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Net: %{x:+.1f}%<extra></extra>'
))

fig.update_layout(
    title="Net Satisfaction Score (Satisfied % - Dissatisfied %)",
    xaxis_title="Net Satisfaction (%)",
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Chart 2: Satisfaction vs Dissatisfaction
st.markdown("#### ⚖️ Satisfaction vs Dissatisfaction Comparison")

fig = go.Figure()

fig.add_trace(go.Bar(
    name='Satisfied',
    y=summary_df['Actor'],
    x=summary_df['Satisfied %'],
    orientation='h',
    marker_color='#10b981',
    text=[f"{v:.1f}%" for v in summary_df['Satisfied %']],
    textposition='inside'
))

fig.add_trace(go.Bar(
    name='Dissatisfied',
    y=summary_df['Actor'],
    x=-summary_df['Dissatisfied %'],  # Negative for diverging chart
    orientation='h',
    marker_color='#ef4444',
    text=[f"{v:.1f}%" for v in summary_df['Dissatisfied %']],
    textposition='inside'
))

fig.update_layout(
    title="Satisfaction (Green) vs Dissatisfaction (Red)",
    xaxis_title="Percentage (%)",
    barmode='relative',
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# COMPREHENSIVE HEATMAP
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔥 Satisfaction Heatmap: All Actors × All Countries</div>', unsafe_allow_html=True)

# Build heatmap data
heatmap_data = []
countries_list = sorted(df_filtered['Country'].dropna().unique())

for country in countries_list:
    cdf = df_filtered[df_filtered['Country'] == country]
    row = []
    
    for q_code in actors.keys():
        c_satisfied_wgt = cdf[cdf[q_code] == 'Satisfied']['WGT'].sum()
        c_dissatisfied_wgt = cdf[cdf[q_code] == 'Dissatisfied']['WGT'].sum()
        
        total = c_satisfied_wgt + c_dissatisfied_wgt
        net = ((c_satisfied_wgt - c_dissatisfied_wgt) / total * 100) if total > 0 else 0
        row.append(net)
    
    heatmap_data.append(row)

heatmap_array = np.array(heatmap_data)

fig = go.Figure(data=go.Heatmap(
    z=heatmap_array,
    x=[actors[q]['short'] for q in actors.keys()],
    y=countries_list,
    colorscale='RdYlGn',
    zmid=0,
    text=heatmap_array.round(1),
    texttemplate='%{text:.0f}',
    textfont={"size": 10},
    colorbar=dict(title="Net<br>Satisfaction<br>(%)")
))

fig.update_layout(
    title="Net Satisfaction by Country and Actor (Green = Satisfied, Red = Dissatisfied)",
    xaxis_title="Global Actor",
    yaxis_title="Country",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="insight-box"><strong>💡 How to read:</strong> Green cells indicate net satisfaction (more people satisfied than dissatisfied). Red cells indicate net dissatisfaction. Darker colors = stronger sentiment.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# INDIVIDUAL ACTOR ANALYSIS (TABS)
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔍 Individual Actor Deep Dive</div>', unsafe_allow_html=True)

tabs = st.tabs([actors[q]['short'] for q in actors.keys()])

for idx, (q_code, actor_info) in enumerate(actors.items()):
    with tabs[idx]:
        st.markdown(f"### {actor_info['name']}")
        
        # Country-by-country breakdown
        actor_country_data = []
        
        for country in sorted(df_filtered['Country'].dropna().unique()):
            cdf = df_filtered[df_filtered['Country'] == country]
            
            c_satisfied = cdf[cdf[q_code] == 'Satisfied']['WGT'].sum()
            c_dissatisfied = cdf[cdf[q_code] == 'Dissatisfied']['WGT'].sum()
            c_dk = cdf[cdf[q_code] == "Don't know / No response"]['WGT'].sum()
            
            total = c_satisfied + c_dissatisfied + c_dk
            
            if total > 0:
                actor_country_data.append({
                    'Country': country,
                    'Satisfied %': (c_satisfied / total * 100),
                    'Dissatisfied %': (c_dissatisfied / total * 100),
                    "Don't Know %": (c_dk / total * 100),
                    'Net': ((c_satisfied - c_dissatisfied) / total * 100)
                })
        
        if actor_country_data:
            actor_df = pd.DataFrame(actor_country_data).sort_values('Net', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Stacked bar
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Satisfied',
                    y=actor_df['Country'],
                    x=actor_df['Satisfied %'],
                    orientation='h',
                    marker_color='#10b981'
                ))
                
                fig.add_trace(go.Bar(
                    name='Dissatisfied',
                    y=actor_df['Country'],
                    x=actor_df['Dissatisfied %'],
                    orientation='h',
                    marker_color='#ef4444'
                ))
                
                fig.add_trace(go.Bar(
                    name="Don't Know",
                    y=actor_df['Country'],
                    x=actor_df["Don't Know %"],
                    orientation='h',
                    marker_color='#94a3b8'
                ))
                
                fig.update_layout(
                    barmode='stack',
                    title=f"Satisfaction Breakdown by Country",
                    xaxis_title="Percentage (%)",
                    height=500,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Net satisfaction
                colors_net = ['#10b981' if x >= 0 else '#ef4444' for x in actor_df['Net']]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    y=actor_df['Country'],
                    x=actor_df['Net'],
                    orientation='h',
                    marker_color=colors_net,
                    text=[f"{v:+.1f}%" for v in actor_df['Net']],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    title=f"Net Satisfaction Score",
                    xaxis_title="Net (%)",
                    height=500,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.dataframe(
                actor_df.round(1),
                use_container_width=True,
                hide_index=True
            )

# ══════════════════════════════════════════════════════════════════
# CLUSTER ANALYSIS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Pattern Analysis</div>', unsafe_allow_html=True)

st.markdown("#### 🔗 Which countries have similar views?")

st.markdown("""
This heatmap shows how similar each pair of countries is in their satisfaction ratings across all 9 global actors.
Darker colors indicate more similar patterns of satisfaction/dissatisfaction.
""")

# Calculate correlation between countries
country_satisfaction_profiles = []

for country in countries_list:
    cdf = df_filtered[df_filtered['Country'] == country]
    profile = []
    
    for q_code in actors.keys():
        c_satisfied = cdf[cdf[q_code] == 'Satisfied']['WGT'].sum()
        c_dissatisfied = cdf[cdf[q_code] == 'Dissatisfied']['WGT'].sum()
        total = c_satisfied + c_dissatisfied
        net = ((c_satisfied - c_dissatisfied) / total * 100) if total > 0 else 0
        profile.append(net)
    
    country_satisfaction_profiles.append(profile)

profile_df = pd.DataFrame(country_satisfaction_profiles, index=countries_list)
correlation_matrix = profile_df.T.corr()

fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale='Viridis',
    text=correlation_matrix.values.round(2),
    texttemplate='%{text:.2f}',
    textfont={"size": 8},
    colorbar=dict(title="Similarity")
))

fig.update_layout(
    title="Country Similarity Matrix (Based on Actor Satisfaction Patterns)",
    xaxis_tickangle=-45,
    height=700,
    width=700
)

st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# REGIONAL PATTERNS
# ══════════════════════════════════════════════════════════════════

st.markdown("#### 🌍 Regional Patterns")

region_map = {
    'Colombia': 'Latin America', 'Mexico': 'Latin America',
    'Croatia': 'Europe', 'Germany': 'Europe', 'Portugal': 'Europe', 
    'Serbia': 'Europe', 'Slovenia': 'Europe', 'Spain': 'Europe', 
    'Sweden': 'Europe', 'Switzerland': 'Europe',
    'Japan': 'Asia-Pacific', 'South Korea': 'Asia-Pacific', 'Philippines': 'Asia-Pacific',
    'Pakistan': 'South Asia',
    'Turkey': 'Middle East'
}

df_filtered['Region'] = df_filtered['Country'].map(region_map)

regional_satisfaction = []

for region in ['Europe', 'Asia-Pacific', 'Latin America']:
    rdf = df_filtered[df_filtered['Region'] == region]
    
    row_data = {'Region': region}
    
    for q_code, actor_info in actors.items():
        r_satisfied = rdf[rdf[q_code] == 'Satisfied']['WGT'].sum()
        r_dissatisfied = rdf[rdf[q_code] == 'Dissatisfied']['WGT'].sum()
        total = r_satisfied + r_dissatisfied
        
        row_data[actor_info['short']] = ((r_satisfied - r_dissatisfied) / total * 100) if total > 0 else 0
    
    regional_satisfaction.append(row_data)

regional_df = pd.DataFrame(regional_satisfaction)

fig = go.Figure()

for region in regional_df['Region']:
    row = regional_df[regional_df['Region'] == region].iloc[0]
    values = [row[actors[q]['short']] for q in actors.keys()]
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=[actors[q]['short'] for q in actors.keys()],
        name=region,
        fill='toself'
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    title="Regional Satisfaction Patterns (Radar Chart)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#065f46 0%,#047857 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · Global Actors' Policies Analysis</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
