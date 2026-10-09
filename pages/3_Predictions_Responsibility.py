import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="War Predictions & Responsibility | Iran Poll", page_icon="⚔️", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#7c3aed 0%,#6d28d9 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #7c3aed;padding-bottom:0.5rem;}
.insight-box{background:#ede9fe;border-left:5px solid #7c3aed;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#5b21b6;}
.insight-box strong{color:#6d28d9;}
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
    <div class="hero-title">⚔️ War Predictions & Responsibility</div>
    <div class="hero-sub">Who will win? Who started it? Global perspectives on the conflict</div>
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
# Q4: WHO WILL WIN?
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🏆 Q4: Who Will Win This War?</div>', unsafe_allow_html=True)

# Overall prediction
total_wgt = df_filtered[df_filtered['Q4'].notna()]['WGT'].sum()
usa_israel_win = df_filtered[df_filtered['Q4'] == 'USA-Israel coalition']['WGT'].sum()
iran_win = df_filtered[df_filtered['Q4'] == 'Iran']['WGT'].sum()
neither_win = df_filtered[df_filtered['Q4'] == 'Neither of them']['WGT'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🇺🇸🇮🇱 USA-Israel Will Win", f"{(usa_israel_win/total_wgt*100):.1f}%")
with col2:
    st.metric("🇮🇷 Iran Will Win", f"{(iran_win/total_wgt*100):.1f}%")
with col3:
    st.metric("⚖️ Neither Will Win", f"{(neither_win/total_wgt*100):.1f}%")

# Pie chart
fig = go.Figure(data=[go.Pie(
    labels=['USA-Israel', 'Iran', 'Neither'],
    values=[usa_israel_win, iran_win, neither_win],
    marker=dict(colors=['#3b82f6', '#10b981', '#f59e0b']),
    hole=0.4
)])
fig.update_layout(title="Global Prediction: Who Will Win?", height=400)
st.plotly_chart(fig, use_container_width=True)

# By country
st.markdown("#### 🌍 Predictions by Country")

prediction_by_country = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q4'].notna())]
    c_total = cdf['WGT'].sum()
    
    if c_total > 0:
        prediction_by_country.append({
            'Country': country,
            'USA-Israel %': (cdf[cdf['Q4'] == 'USA-Israel coalition']['WGT'].sum() / c_total * 100),
            'Iran %': (cdf[cdf['Q4'] == 'Iran']['WGT'].sum() / c_total * 100),
            'Neither %': (cdf[cdf['Q4'] == 'Neither of them']['WGT'].sum() / c_total * 100)
        })

pred_df = pd.DataFrame(prediction_by_country)

fig = go.Figure()
fig.add_trace(go.Bar(name='USA-Israel', y=pred_df['Country'], x=pred_df['USA-Israel %'], orientation='h', marker_color='#3b82f6'))
fig.add_trace(go.Bar(name='Iran', y=pred_df['Country'], x=pred_df['Iran %'], orientation='h', marker_color='#10b981'))
fig.add_trace(go.Bar(name='Neither', y=pred_df['Country'], x=pred_df['Neither %'], orientation='h', marker_color='#f59e0b'))
fig.update_layout(barmode='stack', title="Winner Predictions by Country", height=600, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# Q5: WHO IS RESPONSIBLE?
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🎯 Q5: Who Is Responsible for Starting This War?</div>', unsafe_allow_html=True)

resp_total = df_filtered[df_filtered['Q5'].notna()]['WGT'].sum()
usa_resp = df_filtered[df_filtered['Q5'] == 'USA']['WGT'].sum()
israel_resp = df_filtered[df_filtered['Q5'] == 'Israel']['WGT'].sum()
both_resp = df_filtered[df_filtered['Q5'] == 'USA and Israel are equally responsible']['WGT'].sum()
iran_resp = df_filtered[df_filtered['Q5'] == 'Iran']['WGT'].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🇺🇸 USA", f"{(usa_resp/resp_total*100):.1f}%")
with col2:
    st.metric("🇮🇱 Israel", f"{(israel_resp/resp_total*100):.1f}%")
with col3:
    st.metric("🤝 Both Equally", f"{(both_resp/resp_total*100):.1f}%")
with col4:
    st.metric("🇮🇷 Iran", f"{(iran_resp/resp_total*100):.1f}%")

# Horizontal bar
labels = ['USA', 'Israel', 'USA & Israel Equally', 'Iran']
values = [usa_resp, israel_resp, both_resp, iran_resp]
pcts = [(v/resp_total*100) for v in values]

fig = go.Figure(go.Bar(
    y=labels,
    x=pcts,
    orientation='h',
    marker_color=['#3b82f6', '#60a5fa', '#f59e0b', '#10b981'],
    text=[f"{p:.1f}%" for p in pcts],
    textposition='outside'
))
fig.update_layout(title="Global Attribution of Responsibility", xaxis_title="Percentage (%)", height=400, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# By country
st.markdown("#### 🌍 Responsibility Attribution by Country")

resp_by_country = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q5'].notna())]
    c_total = cdf['WGT'].sum()
    
    if c_total > 0:
        resp_by_country.append({
            'Country': country,
            'USA': (cdf[cdf['Q5'] == 'USA']['WGT'].sum() / c_total * 100),
            'Israel': (cdf[cdf['Q5'] == 'Israel']['WGT'].sum() / c_total * 100),
            'Both': (cdf[cdf['Q5'] == 'USA and Israel are equally responsible']['WGT'].sum() / c_total * 100),
            'Iran': (cdf[cdf['Q5'] == 'Iran']['WGT'].sum() / c_total * 100)
        })

resp_country_df = pd.DataFrame(resp_by_country)

fig = go.Figure()
fig.add_trace(go.Bar(name='USA', y=resp_country_df['Country'], x=resp_country_df['USA'], orientation='h', marker_color='#3b82f6'))
fig.add_trace(go.Bar(name='Israel', y=resp_country_df['Country'], x=resp_country_df['Israel'], orientation='h', marker_color='#60a5fa'))
fig.add_trace(go.Bar(name='Both', y=resp_country_df['Country'], x=resp_country_df['Both'], orientation='h', marker_color='#f59e0b'))
fig.add_trace(go.Bar(name='Iran', y=resp_country_df['Country'], x=resp_country_df['Iran'], orientation='h', marker_color='#10b981'))
fig.update_layout(barmode='stack', title="Responsibility Attribution by Country", height=600, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# CROSS-TABULATION
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Support vs Prediction Cross-Analysis</div>', unsafe_allow_html=True)

st.markdown("**Do people who support a side also predict that side will win?**")

# Filter to those who answered both Q2 and Q4
cross_df = df_filtered[(df_filtered['Q2'].notna()) & (df_filtered['Q4'].notna())]

cross_tab = []
support_map = {
    'USA-Israel coalition': 'Support USA-Israel',
    'Iran': 'Support Iran',
    'Neither of them': 'Support Neither'
}
for support_val, support_label in support_map.items():
    support_group = cross_df[cross_df['Q2'] == support_val]
    total = support_group['WGT'].sum()
    
    if total > 0:
        cross_tab.append({
            'Support': support_label,
            'Predict USA-Israel Win': (support_group[support_group['Q4'] == 'USA-Israel coalition']['WGT'].sum() / total * 100),
            'Predict Iran Win': (support_group[support_group['Q4'] == 'Iran']['WGT'].sum() / total * 100),
            'Predict Neither Win': (support_group[support_group['Q4'] == 'Neither of them']['WGT'].sum() / total * 100)
        })

cross_df_display = pd.DataFrame(cross_tab)

fig = go.Figure()
fig.add_trace(go.Bar(name='Predict USA-Israel Win', x=cross_df_display['Support'], y=cross_df_display['Predict USA-Israel Win'], marker_color='#3b82f6'))
fig.add_trace(go.Bar(name='Predict Iran Win', x=cross_df_display['Support'], y=cross_df_display['Predict Iran Win'], marker_color='#10b981'))
fig.add_trace(go.Bar(name='Predict Neither Win', x=cross_df_display['Support'], y=cross_df_display['Predict Neither Win'], marker_color='#f59e0b'))
fig.update_layout(barmode='group', title="Predictions by Support Group", yaxis_title="Percentage (%)", height=400, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(cross_df_display.round(1), use_container_width=True, hide_index=True)

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#5b21b6 0%,#6d28d9 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · War Predictions & Responsibility</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
