import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Government Satisfaction | Iran Poll", page_icon="🏛️", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#db2777 0%,#be185d 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #db2777;padding-bottom:0.5rem;}
.insight-box{background:#fce7f3;border-left:5px solid #db2777;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#831843;}
.insight-box strong{color:#9f1239;}
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
    <div class="hero-title">🏛️ Government Policy Satisfaction</div>
    <div class="hero-sub">How satisfied are citizens with their own government's policy on the war?</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Question 7:** *Are you on the whole, satisfied or dissatisfied with the policy of your government on this war?*

**Response Options:**
- 1 = Satisfied
- 2 = Dissatisfied
- 3 = Neither satisfied nor dissatisfied
- 9 = Don't know / No response
""")

# Data availability note
st.markdown("""
<div style="background:#e0f2fe;border-left:5px solid #028090;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;">
<strong>📊 Data Availability:</strong> Q7 was asked in <strong>11 out of 17 countries</strong>. Not asked in: Colombia, Croatia, Serbia, Slovenia.
</div>
""", unsafe_allow_html=True)

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
# OVERALL SATISFACTION
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Overall Satisfaction</div>', unsafe_allow_html=True)

total_wgt = df_filtered[df_filtered['Q7'].notna()]['WGT'].sum()
satisfied_wgt = df_filtered[df_filtered['Q7'] == 'Satisfied']['WGT'].sum()
dissatisfied_wgt = df_filtered[df_filtered['Q7'] == 'Dissatisfied']['WGT'].sum()
neither_wgt = df_filtered[df_filtered['Q7'] == 'Neither satisfied nor dissatisfied']['WGT'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("😊 Satisfied", f"{(satisfied_wgt/total_wgt*100):.1f}%")
with col2:
    st.metric("😠 Dissatisfied", f"{(dissatisfied_wgt/total_wgt*100):.1f}%")
with col3:
    st.metric("😐 Neither", f"{(neither_wgt/total_wgt*100):.1f}%")

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(data=[go.Pie(
        labels=['Satisfied', 'Dissatisfied', 'Neither'],
        values=[satisfied_wgt, dissatisfied_wgt, neither_wgt],
        marker=dict(colors=['#10b981', '#ef4444', '#f59e0b']),
        hole=0.4
    )])
    fig.update_layout(title="Global Distribution", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    labels = ['Satisfied', 'Dissatisfied', 'Neither']
    values = [satisfied_wgt/total_wgt*100, dissatisfied_wgt/total_wgt*100, neither_wgt/total_wgt*100]
    
    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation='h',
        marker_color=['#10b981', '#ef4444', '#f59e0b'],
        text=[f"{v:.1f}%" for v in values],
        textposition='outside'
    ))
    fig.update_layout(title="Satisfaction Breakdown", xaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# BY COUNTRY
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🌍 Satisfaction by Country</div>', unsafe_allow_html=True)

country_satisfaction = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q7'].notna())]
    c_total = cdf['WGT'].sum()
    
    if c_total > 0:
        country_satisfaction.append({
            'Country': country,
            'Satisfied %': (cdf[cdf['Q7'] == 'Satisfied']['WGT'].sum() / c_total * 100),
            'Dissatisfied %': (cdf[cdf['Q7'] == 'Dissatisfied']['WGT'].sum() / c_total * 100),
            'Neither %': (cdf[cdf['Q7'] == 'Neither satisfied nor dissatisfied']['WGT'].sum() / c_total * 100),
            'Net Satisfaction': ((cdf[cdf['Q7'] == 'Satisfied']['WGT'].sum() - cdf[cdf['Q7'] == 'Dissatisfied']['WGT'].sum()) / c_total * 100)
        })

country_df = pd.DataFrame(country_satisfaction).sort_values('Satisfied %', ascending=False)

# Stacked bar
fig = go.Figure()
fig.add_trace(go.Bar(name='Satisfied', y=country_df['Country'], x=country_df['Satisfied %'], orientation='h', marker_color='#10b981'))
fig.add_trace(go.Bar(name='Dissatisfied', y=country_df['Country'], x=country_df['Dissatisfied %'], orientation='h', marker_color='#ef4444'))
fig.add_trace(go.Bar(name='Neither', y=country_df['Country'], x=country_df['Neither %'], orientation='h', marker_color='#f59e0b'))
fig.update_layout(barmode='stack', title="Government Policy Satisfaction by Country", height=600, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Net satisfaction
st.markdown("#### 📊 Net Satisfaction (Satisfied % - Dissatisfied %)")

colors = ['#10b981' if x >= 0 else '#ef4444' for x in country_df['Net Satisfaction']]

fig = go.Figure(go.Bar(
    y=country_df['Country'],
    x=country_df['Net Satisfaction'],
    orientation='h',
    marker_color=colors,
    text=[f"{v:+.1f}%" for v in country_df['Net Satisfaction']],
    textposition='outside'
))
fig.update_layout(title="Net Government Satisfaction Score", xaxis_title="Net (%)", height=500, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="insight-box"><strong>💡 Key Insight:</strong> ' + 
            f"{country_df.iloc[0]['Country']} has the highest government satisfaction at {country_df.iloc[0]['Satisfied %']:.1f}%, " +
            f"while {country_df.iloc[-1]['Country']} has the lowest at {country_df.iloc[-1]['Satisfied %']:.1f}%.</div>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# CROSS-TAB WITH SUPPORT
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔗 Government Satisfaction vs War Support</div>', unsafe_allow_html=True)

cross_df = df_filtered[(df_filtered['Q2'].notna()) & (df_filtered['Q7'].notna())]

support_gov = []
support_map = {
    'USA-Israel coalition': 'Support USA-Israel',
    'Iran': 'Support Iran',
    'Neither of them': 'Support Neither'
}
for support_val, support_label in support_map.items():
    group = cross_df[cross_df['Q2'] == support_val]
    total = group['WGT'].sum()
    
    if total > 0:
        support_gov.append({
            'War Support': support_label,
            'Satisfied with Gov': (group[group['Q7'] == 'Satisfied']['WGT'].sum() / total * 100),
            'Dissatisfied with Gov': (group[group['Q7'] == 'Dissatisfied']['WGT'].sum() / total * 100),
            'Neither': (group[group['Q7'] == 'Neither satisfied nor dissatisfied']['WGT'].sum() / total * 100)
        })

support_gov_df = pd.DataFrame(support_gov)

fig = go.Figure()
fig.add_trace(go.Bar(name='Satisfied', x=support_gov_df['War Support'], y=support_gov_df['Satisfied with Gov'], marker_color='#10b981'))
fig.add_trace(go.Bar(name='Dissatisfied', x=support_gov_df['War Support'], y=support_gov_df['Dissatisfied with Gov'], marker_color='#ef4444'))
fig.add_trace(go.Bar(name='Neither', x=support_gov_df['War Support'], y=support_gov_df['Neither'], marker_color='#f59e0b'))
fig.update_layout(barmode='group', title="Government Satisfaction by War Support Position", yaxis_title="Percentage (%)", height=400, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(support_gov_df.round(1), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">👥 Demographics</div>', unsafe_allow_html=True)

# By Age
st.markdown("#### 📅 Satisfaction by Age Group")

age_labels = ['18 – 24', '25 – 34', '35 – 44', '45 – 54', '55 – 64', '65+']
age_satisfaction = []

for age_label in age_labels:
    adf = df_filtered[(df_filtered['D2B'] == age_label) & (df_filtered['Q7'].notna())]
    total = adf['WGT'].sum()
    
    if total > 100:
        age_satisfaction.append({
            'Age Group': age_label,
            'Satisfied %': (adf[adf['Q7'] == 'Satisfied']['WGT'].sum() / total * 100)
        })

if age_satisfaction:
    age_df = pd.DataFrame(age_satisfaction)
    
    fig = go.Figure(go.Scatter(
        x=age_df['Age Group'],
        y=age_df['Satisfied %'],
        mode='lines+markers',
        marker=dict(size=12, color='#db2777'),
        line=dict(width=3, color='#db2777')
    ))
    fig.update_layout(title="Government Satisfaction Across Age Groups", yaxis_title="Satisfied %", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#831843 0%,#9f1239 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · Government Policy Satisfaction</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
