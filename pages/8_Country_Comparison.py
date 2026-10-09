import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Country Comparison | Iran Poll", page_icon="🔍", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#0ea5e9 0%,#0284c7 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #0ea5e9;padding-bottom:0.5rem;}
.insight-box{background:#e0f2fe;border-left:5px solid #0ea5e9;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#075985;}
.insight-box strong{color:#0369a1;}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("Iran_Snap_Poll_2026_-_Merged_Data_Working_File__17_Countries_.xlsx")
    # CountryID is already the country name in new data
    df["Country"] = df["CountryID"]
    # Armenia was screened via survey invitation (Q1 implicit Yes) - fill for correct analysis
    df.loc[df["CountryID"] == "Armenia", "Q1"] = "Yes"
    return df

df = load_data()

st.markdown("""
<div class="hero">
    <div class="hero-title">🔍 Country Comparison Tool</div>
    <div class="hero-sub">Interactive side-by-side comparison across all survey dimensions</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# COUNTRY SELECTION
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🌍 Select Countries to Compare</div>', unsafe_allow_html=True)

all_countries = sorted(df["Country"].dropna().unique())

selected_countries = st.multiselect(
    "Choose 2-5 countries for comparison:",
    options=all_countries,
    default=all_countries[:3] if len(all_countries) >= 3 else all_countries,
    max_selections=5
)

if len(selected_countries) < 2:
    st.warning("⚠️ Please select at least 2 countries to compare")
    st.stop()

df_comp = df[df["Country"].isin(selected_countries)]

st.success(f"✅ Comparing {len(selected_countries)} countries: {', '.join(selected_countries)}")

# ══════════════════════════════════════════════════════════════════
# OVERVIEW METRICS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Overview Metrics</div>', unsafe_allow_html=True)

cols = st.columns(len(selected_countries))

for idx, country in enumerate(selected_countries):
    cdf = df_comp[df_comp["Country"] == country]
    
    with cols[idx]:
        st.markdown(f"### {country}")
        st.metric("Sample Size", f"{len(cdf):,}")
        st.metric("Weighted N", f"{int(cdf['WGT'].sum()):,}")

# ══════════════════════════════════════════════════════════════════
# WAR SUPPORT COMPARISON
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🎯 War Support Comparison</div>', unsafe_allow_html=True)

support_comp = []
for country in selected_countries:
    cdf = df_comp[(df_comp["Country"] == country) & (df_comp['Q2'].notna())]
    total = cdf['WGT'].sum()
    
    if total > 0:
        support_comp.append({
            'Country': country,
            'USA-Israel': (cdf[cdf['Q2'] == 'USA-Israel coalition']['WGT'].sum() / total * 100),
            'Iran': (cdf[cdf['Q2'] == 'Iran']['WGT'].sum() / total * 100),
            'Neither': (cdf[cdf['Q2'] == 'Neither of them']['WGT'].sum() / total * 100)
        })

if support_comp:
    support_df = pd.DataFrame(support_comp)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='USA-Israel', x=support_df['Country'], y=support_df['USA-Israel'], marker_color='#3b82f6'))
    fig.add_trace(go.Bar(name='Iran', x=support_df['Country'], y=support_df['Iran'], marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Neither', x=support_df['Country'], y=support_df['Neither'], marker_color='#f59e0b'))
    fig.update_layout(barmode='group', title="War Support by Country", yaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# HARM EXPECTATIONS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">💥 Expected Harm Comparison</div>', unsafe_allow_html=True)

harm_comp = []
for country in selected_countries:
    cdf = df_comp[df_comp["Country"] == country]
    
    row = {'Country': country}
    
    for q_code, label in [('Q3_1', 'Physical'), ('Q3_2', 'Financial'), ('Q3_3', 'Emotional')]:
        q_data = cdf[cdf[q_code].notna()]
        total = q_data['WGT'].sum()
        strong = q_data[q_data[q_code] == 'Strong harm expected']['WGT'].sum()
        row[label] = (strong / total * 100) if total > 0 else 0
    
    harm_comp.append(row)

if harm_comp:
    harm_df = pd.DataFrame(harm_comp)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Physical', x=harm_df['Country'], y=harm_df['Physical'], marker_color='#ef4444'))
    fig.add_trace(go.Bar(name='Financial', x=harm_df['Country'], y=harm_df['Financial'], marker_color='#f59e0b'))
    fig.add_trace(go.Bar(name='Emotional', x=harm_df['Country'], y=harm_df['Emotional'], marker_color='#8b5cf6'))
    fig.update_layout(barmode='group', title="Strong Harm Expectations (%) by Type", yaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PREDICTIONS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🏆 Winner Predictions</div>', unsafe_allow_html=True)

pred_comp = []
for country in selected_countries:
    cdf = df_comp[(df_comp["Country"] == country) & (df_comp['Q4'].notna())]
    total = cdf['WGT'].sum()
    
    if total > 0:
        pred_comp.append({
            'Country': country,
            'USA-Israel Win': (cdf[cdf['Q4'] == 'USA-Israel coalition']['WGT'].sum() / total * 100),
            'Iran Win': (cdf[cdf['Q4'] == 'Iran']['WGT'].sum() / total * 100),
            'Neither Win': (cdf[cdf['Q4'] == 'Neither of them']['WGT'].sum() / total * 100)
        })

if pred_comp:
    pred_df = pd.DataFrame(pred_comp)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='USA-Israel', x=pred_df['Country'], y=pred_df['USA-Israel Win'], marker_color='#3b82f6'))
    fig.add_trace(go.Bar(name='Iran', x=pred_df['Country'], y=pred_df['Iran Win'], marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Neither', x=pred_df['Country'], y=pred_df['Neither Win'], marker_color='#f59e0b'))
    fig.update_layout(barmode='group', title="Who Will Win? Predictions by Country", yaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# GOVERNMENT SATISFACTION
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🏛️ Government Policy Satisfaction</div>', unsafe_allow_html=True)

gov_comp = []
for country in selected_countries:
    cdf = df_comp[(df_comp["Country"] == country) & (df_comp['Q7'].notna())]
    total = cdf['WGT'].sum()
    
    if total > 0:
        satisfied = cdf[cdf['Q7'] == 'Satisfied']['WGT'].sum()
        dissatisfied = cdf[cdf['Q7'] == 'Dissatisfied']['WGT'].sum()
        gov_comp.append({
            'Country': country,
            'Satisfied': (satisfied / total * 100),
            'Dissatisfied': (dissatisfied / total * 100),
            'Net': ((satisfied - dissatisfied) / total * 100)
        })

if gov_comp:
    gov_df = pd.DataFrame(gov_comp)
    
    colors = ['#10b981' if x >= 0 else '#ef4444' for x in gov_df['Net']]
    
    fig = go.Figure(go.Bar(
        x=gov_df['Country'],
        y=gov_df['Net'],
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in gov_df['Net']],
        textposition='outside'
    ))
    fig.update_layout(title="Net Government Satisfaction (Satisfied % - Dissatisfied %)", yaxis_title="Net %", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# RADAR CHART - MULTIDIMENSIONAL
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🎯 Multidimensional Comparison (Radar Chart)</div>', unsafe_allow_html=True)

radar_data = []

# Updated dimensions with string label comparisons
dimensions = [
    ("Q2", 'USA-Israel coalition', 'Support USA-Israel'),
    ("Q2", 'Iran', 'Support Iran'),
    ("Q3_1", 'Strong harm expected', 'Physical Harm Fear'),
    ("Q4", 'USA-Israel coalition', 'Predict USA-Israel Win'),
    ("Q7", 'Satisfied', 'Gov Satisfaction'),
    ("Q6", 'Agree', 'Agree Khamenei Death')
]

for country in selected_countries:
    cdf = df_comp[df_comp["Country"] == country]
    
    values = []
    for q_code, value_label, display_label in dimensions:
        q_data = cdf[cdf[q_code].notna()]
        total = q_data['WGT'].sum()
        count = q_data[q_data[q_code] == value_label]['WGT'].sum()
        pct = (count / total * 100) if total > 0 else 0
        values.append(pct)
    
    radar_data.append({
        'country': country,
        'values': values
    })

fig = go.Figure()

for item in radar_data:
    fig.add_trace(go.Scatterpolar(
        r=item['values'],
        theta=[d[2] for d in dimensions],  # Use display_label (index 2)
        name=item['country'],
        fill='toself'
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    title="Multidimensional Country Comparison",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# DATA TABLE
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📋 Complete Comparison Table</div>', unsafe_allow_html=True)

table_data = []

for country in selected_countries:
    cdf = df_comp[df_comp["Country"] == country]
    
    # Calculate all metrics
    q2_data = cdf[cdf['Q2'].notna()]
    q2_total = q2_data['WGT'].sum()
    
    q4_data = cdf[cdf['Q4'].notna()]
    q4_total = q4_data['WGT'].sum()
    
    q7_data = cdf[cdf['Q7'].notna()]
    q7_total = q7_data['WGT'].sum()
    
    table_data.append({
        'Country': country,
        'Sample': len(cdf),
        'Support USA-Israel %': (cdf[cdf['Q2'] == 'USA-Israel coalition']['WGT'].sum() / q2_total * 100) if q2_total > 0 else 0,
        'Support Iran %': (cdf[cdf['Q2'] == 'Iran']['WGT'].sum() / q2_total * 100) if q2_total > 0 else 0,
        'Predict USA Win %': (cdf[cdf['Q4'] == 'USA-Israel coalition']['WGT'].sum() / q4_total * 100) if q4_total > 0 else 0,
        'Gov Satisfied %': (cdf[cdf['Q7'] == 'Satisfied']['WGT'].sum() / q7_total * 100) if q7_total > 0 else 0,
        'Physical Harm %': (cdf[cdf['Q3_1'] == 'Strong harm expected']['WGT'].sum() / cdf[cdf['Q3_1'].notna()]['WGT'].sum() * 100) if cdf[cdf['Q3_1'].notna()]['WGT'].sum() > 0 else 0
    })

table_df = pd.DataFrame(table_data)

st.dataframe(
    table_df.round(1),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Country": st.column_config.TextColumn("Country", width="medium"),
        "Sample": st.column_config.NumberColumn("Sample", format="%d"),
        "Support USA-Israel %": st.column_config.NumberColumn("Support USA-Israel", format="%.1f%%"),
        "Support Iran %": st.column_config.NumberColumn("Support Iran", format="%.1f%%"),
        "Predict USA Win %": st.column_config.NumberColumn("Predict USA Win", format="%.1f%%"),
        "Gov Satisfied %": st.column_config.NumberColumn("Gov Satisfied", format="%.1f%%"),
        "Physical Harm %": st.column_config.NumberColumn("Physical Harm Fear", format="%.1f%%")
    }
)

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#075985 0%,#0369a1 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · Country Comparison Tool</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
