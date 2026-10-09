import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Khamenei Assessment | Iran Poll", page_icon="🎭", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#0891b2 0%,#0e7490 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #0891b2;padding-bottom:0.5rem;}
.insight-box{background:#cffafe;border-left:5px solid #0891b2;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#164e63;}
.insight-box strong{color:#0e7490;}
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
    <div class="hero-title">🎭 Khamenei Assassination Assessment</div>
    <div class="hero-sub">Public opinion on the assassination of Iran's Supreme Leader</div>
</div>
""", unsafe_allow_html=True)

# Data availability warning
st.markdown("""
<div style="background:#e0f2fe;border-left:5px solid#028090;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;">
<strong>📊 Data Availability:</strong> Q6 was asked in <strong>9 out of 17 countries</strong>. Countries where this question was <strong>not asked</strong>: Colombia, Croatia, Pakistan, Serbia, Slovenia, Turkey. Charts below show only the 9 countries with data.
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Question 6:** *What is your assessment of the assassination of Iran's top leader, Ayatollah Ali Khamenei?*

**Response Options:**
- 1 = Agree
- 2 = Disagree  
- 3 = Neither agree nor disagree
- 9 = Don't know / No response
""")

# Filters
st.sidebar.markdown("### 🌍 Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=sorted(df["Country"].dropna().unique()),
    default=sorted(df["Country"].dropna().unique())
)

df_filtered = df[df["Country"].isin(selected_countries)] if selected_countries else df
st.sidebar.metric("📊 Filtered Sample", f"{len(df_filtered):,}")

# ══════════════════════════════════════════════════════════════════
# OVERALL ASSESSMENT
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Overall Assessment</div>', unsafe_allow_html=True)

total_wgt = df_filtered[df_filtered['Q6'].notna()]['WGT'].sum()
agree_wgt = df_filtered[df_filtered['Q6'] == 'Agree']['WGT'].sum()
disagree_wgt = df_filtered[df_filtered['Q6'] == 'Disagree']['WGT'].sum()
neutral_wgt = df_filtered[df_filtered['Q6'] == 'Neither agree nor disagree']['WGT'].sum()
dk_wgt = df_filtered[df_filtered['Q6'] == "Don't know / No response"]['WGT'].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("✅ Agree", f"{(agree_wgt/total_wgt*100):.1f}%")
with col2:
    st.metric("❌ Disagree", f"{(disagree_wgt/total_wgt*100):.1f}%")
with col3:
    st.metric("⚖️ Neutral", f"{(neutral_wgt/total_wgt*100):.1f}%")
with col4:
    st.metric("❓ Don't Know", f"{(dk_wgt/total_wgt*100):.1f}%")

# Donut chart
col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(data=[go.Pie(
        labels=['Agree', 'Disagree', 'Neither', "Don't Know"],
        values=[agree_wgt, disagree_wgt, neutral_wgt, dk_wgt],
        marker=dict(colors=['#10b981', '#ef4444', '#f59e0b', '#94a3b8']),
        hole=0.4
    )])
    fig.update_layout(title="Global Distribution", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    labels = ['Agree', 'Disagree', 'Neither', "Don't Know"]
    values = [agree_wgt/total_wgt*100, disagree_wgt/total_wgt*100, neutral_wgt/total_wgt*100, dk_wgt/total_wgt*100]
    
    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation='h',
        marker_color=['#10b981', '#ef4444', '#f59e0b', '#94a3b8'],
        text=[f"{v:.1f}%" for v in values],
        textposition='outside'
    ))
    fig.update_layout(title="Assessment Breakdown", xaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# BY COUNTRY
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🌍 Assessment by Country</div>', unsafe_allow_html=True)

country_assessment = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q6'].notna())]
    c_total = cdf['WGT'].sum()
    
    if c_total > 0:
        country_assessment.append({
            'Country': country,
            'Agree %': (cdf[cdf['Q6'] == 'Agree']['WGT'].sum() / c_total * 100),
            'Disagree %': (cdf[cdf['Q6'] == 'Disagree']['WGT'].sum() / c_total * 100),
            'Neither %': (cdf[cdf['Q6'] == 'Neither agree nor disagree']['WGT'].sum() / c_total * 100),
            'Net Agreement': ((cdf[cdf['Q6'] == 'Agree']['WGT'].sum() - cdf[cdf['Q6'] == 'Disagree']['WGT'].sum()) / c_total * 100)
        })

country_df = pd.DataFrame(country_assessment).sort_values('Agree %', ascending=False)

# Stacked bar
fig = go.Figure()
fig.add_trace(go.Bar(name='Agree', y=country_df['Country'], x=country_df['Agree %'], orientation='h', marker_color='#10b981'))
fig.add_trace(go.Bar(name='Disagree', y=country_df['Country'], x=country_df['Disagree %'], orientation='h', marker_color='#ef4444'))
fig.add_trace(go.Bar(name='Neither', y=country_df['Country'], x=country_df['Neither %'], orientation='h', marker_color='#f59e0b'))
fig.update_layout(barmode='stack', title="Assessment by Country", height=600, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Net agreement
st.markdown("#### 📊 Net Agreement (Agree % - Disagree %)")

colors = ['#10b981' if x >= 0 else '#ef4444' for x in country_df['Net Agreement']]

fig = go.Figure(go.Bar(
    y=country_df['Country'],
    x=country_df['Net Agreement'],
    orientation='h',
    marker_color=colors,
    text=[f"{v:+.1f}%" for v in country_df['Net Agreement']],
    textposition='outside'
))
fig.update_layout(title="Net Agreement Score", xaxis_title="Net (%)", height=500, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# CORRELATION WITH WAR SUPPORT
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔗 Correlation with War Support</div>', unsafe_allow_html=True)

cross_df = df_filtered[(df_filtered['Q2'].notna()) & (df_filtered['Q6'].notna())]

support_assessment = []
support_map = {
    'USA-Israel coalition': 'Support USA-Israel',
    'Iran': 'Support Iran',
    'Neither of them': 'Support Neither'
}
for support_val, support_label in support_map.items():
    group = cross_df[cross_df['Q2'] == support_val]
    total = group['WGT'].sum()
    
    if total > 0:
        support_assessment.append({
            'Support': support_label,
            'Agree': (group[group['Q6'] == 'Agree']['WGT'].sum() / total * 100),
            'Disagree': (group[group['Q6'] == 'Disagree']['WGT'].sum() / total * 100),
            'Neither': (group[group['Q6'] == 'Neither agree nor disagree']['WGT'].sum() / total * 100)
        })

support_df = pd.DataFrame(support_assessment)

fig = go.Figure()
fig.add_trace(go.Bar(name='Agree', x=support_df['Support'], y=support_df['Agree'], marker_color='#10b981'))
fig.add_trace(go.Bar(name='Disagree', x=support_df['Support'], y=support_df['Disagree'], marker_color='#ef4444'))
fig.add_trace(go.Bar(name='Neither', x=support_df['Support'], y=support_df['Neither'], marker_color='#f59e0b'))
fig.update_layout(barmode='group', title="Khamenei Assessment by War Support Position", yaxis_title="Percentage (%)", height=400, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(support_df.round(1), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">👥 Demographics</div>', unsafe_allow_html=True)

# By Religion
st.markdown("#### ⛪ Assessment by Religion")

religion_map = {
    1: 'Catholic', 2: 'Orthodox', 3: 'Protestant', 4: 'Other Christian',
    5: 'Hindu', 6: 'Muslim', 7: 'Jewish', 8: 'Buddhist',
    9: 'Other', 10: 'Atheist/Agnostic'
}

religion_assessment = []
for rel_code, rel_name in religion_map.items():
    rel_df = df_filtered[(df_filtered['D6'] == rel_code) & (df_filtered['Q6'].notna())]
    total = rel_df['WGT'].sum()
    
    if total > 100:  # Minimum sample
        religion_assessment.append({
            'Religion': rel_name,
            'Agree %': (rel_df[rel_df['Q6'] == 'Agree']['WGT'].sum() / total * 100),
            'Sample': len(rel_df)
        })

if religion_assessment:
    rel_df = pd.DataFrame(religion_assessment).sort_values('Agree %', ascending=False)
    
    fig = go.Figure(go.Bar(
        y=rel_df['Religion'],
        x=rel_df['Agree %'],
        orientation='h',
        marker_color='#0891b2',
        text=[f"{v:.1f}%" for v in rel_df['Agree %']],
        textposition='outside'
    ))
    fig.update_layout(title="Agreement % by Religion", xaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#164e63 0%,#0e7490 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · Khamenei Assessment Analysis</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
