import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="War Expectations & Future Outlook | Iran Poll", page_icon="🔮", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#8b5cf6 0%,#7c3aed 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #8b5cf6;padding-bottom:0.5rem;}
.insight-box{background:#ede9fe;border-left:5px solid #8b5cf6;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#5b21b6;}
.insight-box strong{color:#6d28d9;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:#002147;padding:.4rem;border-radius:12px;}
.stTabs [data-baseweb="tab"]{height:46px;padding:0 22px;background:rgba(255,255,255,.1);border-radius:9px;color:#90b8e8 !important;font-weight:700;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#8b5cf6 0%,#7c3aed 100%) !important;color:white !important;font-weight:800 !important;}
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
    <div class="hero-title">🔮 War Expectations & Future Outlook</div>
    <div class="hero-sub">Regime change, war outcomes, duration, military support, and terrorism risks</div>
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
# Q9: REGIME CHANGE
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🏛️ Q9: Will USA-Israel Succeed in Regime Change?</div>', unsafe_allow_html=True)

st.markdown("""
**Question:** *Do you think that USA and Israel will succeed or fail in overthrowing the current government of Iran and replacing it by a government of their own choice?*

**Response Options:**
- 1 = Succeed in replacing
- 2 = Fail
- 9 = Don't know / No response
""")

total_wgt = df_filtered[df_filtered['Q9'].notna()]['WGT'].sum()
succeed_wgt = df_filtered[df_filtered['Q9'] == 'Succeed in replacing']['WGT'].sum()
fail_wgt = df_filtered[df_filtered['Q9'] == 'Fail']['WGT'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("✅ Will Succeed", f"{(succeed_wgt/total_wgt*100):.1f}%" if total_wgt > 0 else "N/A")
with col2:
    st.metric("❌ Will Fail", f"{(fail_wgt/total_wgt*100):.1f}%" if total_wgt > 0 else "N/A")

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(data=[go.Pie(
        labels=['Succeed', 'Fail'],
        values=[succeed_wgt, fail_wgt],
        marker=dict(colors=['#10b981', '#ef4444']),
        hole=0.4
    )])
    fig.update_layout(title="Global Expectation", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # By country
    regime_by_country = []
    for country in sorted(df_filtered['Country'].dropna().unique()):
        cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q9'].notna())]
        c_total = cdf['WGT'].sum()
        
        if c_total > 0:
            regime_by_country.append({
                'Country': country,
                'Succeed %': (cdf[cdf['Q9'] == 'Succeed in replacing']['WGT'].sum() / c_total * 100),
                'Fail %': (cdf[cdf['Q9'] == 'Fail']['WGT'].sum() / c_total * 100)
            })
    
    regime_df = pd.DataFrame(regime_by_country).sort_values('Succeed %', ascending=False)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Succeed', y=regime_df['Country'], x=regime_df['Succeed %'], orientation='h', marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Fail', y=regime_df['Country'], x=regime_df['Fail %'], orientation='h', marker_color='#ef4444'))
    fig.update_layout(barmode='stack', title="Regime Change Expectations by Country", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# Q10: WAR OUTCOMES
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Q10: War Outcome Expectations</div>', unsafe_allow_html=True)

st.markdown("**Question:** *What do you think the outcome of this war will be?*")

tab1, tab2, tab3 = st.tabs(["🇮🇷 Iran Stability", "🌍 Middle East Stability", "🇮🇱 Israel Safety"])

# Tab 1: Iran Stability
with tab1:
    st.markdown("#### Will Iran be stable or chaotic?")
    
    iran_stable = df_filtered[df_filtered['Q10_1'] == 'Iran will be a stable and peaceful country']['WGT'].sum()
    iran_chaos = df_filtered[df_filtered['Q10_1'] == 'Iran will be marked by chaos and internal strife']['WGT'].sum()
    total = df_filtered[df_filtered['Q10_1'].notna()]['WGT'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🕊️ Stable & Peaceful", f"{(iran_stable/total*100):.1f}%" if total > 0 else "N/A")
    with col2:
        st.metric("💥 Chaos & Strife", f"{(iran_chaos/total*100):.1f}%" if total > 0 else "N/A")
    
    # By country
    iran_by_country = []
    for country in sorted(df_filtered['Country'].dropna().unique()):
        cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q10_1'].notna())]
        c_total = cdf['WGT'].sum()
        
        if c_total > 0:
            iran_by_country.append({
                'Country': country,
                'Stable %': (cdf[cdf['Q10_1'] == 'Iran will be a stable and peaceful country']['WGT'].sum() / c_total * 100),
                'Chaos %': (cdf[cdf['Q10_1'] == 'Iran will be marked by chaos and internal strife']['WGT'].sum() / c_total * 100)
            })
    
    iran_df = pd.DataFrame(iran_by_country)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Stable', y=iran_df['Country'], x=iran_df['Stable %'], orientation='h', marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Chaos', y=iran_df['Country'], x=iran_df['Chaos %'], orientation='h', marker_color='#ef4444'))
    fig.update_layout(barmode='stack', title="Iran Future: Stability vs Chaos", height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Middle East Stability
with tab2:
    st.markdown("#### Will the Middle East be safe or unsafe?")
    
    me_safe = df_filtered[df_filtered['Q10_2'] == 'The Middle East will be a safe and stable region']['WGT'].sum()
    me_unsafe = df_filtered[df_filtered['Q10_2'] == 'The Middle East will be an unsafe and unstable region']['WGT'].sum()
    total = df_filtered[df_filtered['Q10_2'].notna()]['WGT'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Safe & Stable", f"{(me_safe/total*100):.1f}%" if total > 0 else "N/A")
    with col2:
        st.metric("⚠️ Unsafe & Unstable", f"{(me_unsafe/total*100):.1f}%" if total > 0 else "N/A")
    
    # By country
    me_by_country = []
    for country in sorted(df_filtered['Country'].dropna().unique()):
        cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q10_2'].notna())]
        c_total = cdf['WGT'].sum()
        
        if c_total > 0:
            me_by_country.append({
                'Country': country,
                'Safe %': (cdf[cdf['Q10_2'] == 'The Middle East will be a safe and stable region']['WGT'].sum() / c_total * 100),
                'Unsafe %': (cdf[cdf['Q10_2'] == 'The Middle East will be an unsafe and unstable region']['WGT'].sum() / c_total * 100)
            })
    
    me_df = pd.DataFrame(me_by_country)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Safe', y=me_df['Country'], x=me_df['Safe %'], orientation='h', marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Unsafe', y=me_df['Country'], x=me_df['Unsafe %'], orientation='h', marker_color='#ef4444'))
    fig.update_layout(barmode='stack', title="Middle East Future: Safety vs Instability", height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Israel Safety
with tab3:
    st.markdown("#### Will Israel be safe from attacks?")
    
    israel_safe = df_filtered[df_filtered['Q10_3'] == 'Israel will be safe from external attacks']['WGT'].sum()
    israel_attacks = df_filtered[df_filtered['Q10_3'] == 'Israel will continue to be affected by external attacks']['WGT'].sum()
    total = df_filtered[df_filtered['Q10_3'].notna()]['WGT'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🛡️ Safe from Attacks", f"{(israel_safe/total*100):.1f}%" if total > 0 else "N/A")
    with col2:
        st.metric("🎯 Continued Attacks", f"{(israel_attacks/total*100):.1f}%" if total > 0 else "N/A")
    
    # By country
    israel_by_country = []
    for country in sorted(df_filtered['Country'].dropna().unique()):
        cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q10_3'].notna())]
        c_total = cdf['WGT'].sum()
        
        if c_total > 0:
            israel_by_country.append({
                'Country': country,
                'Safe %': (cdf[cdf['Q10_3'] == 'Israel will be safe from external attacks']['WGT'].sum() / c_total * 100),
                'Attacks %': (cdf[cdf['Q10_3'] == 'Israel will continue to be affected by external attacks']['WGT'].sum() / c_total * 100)
            })
    
    israel_df = pd.DataFrame(israel_by_country)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Safe', y=israel_df['Country'], x=israel_df['Safe %'], orientation='h', marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Attacks', y=israel_df['Country'], x=israel_df['Attacks %'], orientation='h', marker_color='#ef4444'))
    fig.update_layout(barmode='stack', title="Israel's Future: Safety vs Continued Attacks", height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# Q11: WAR DURATION
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">⏱️ Q11: Expected War Duration</div>', unsafe_allow_html=True)

st.markdown("""
**Question:** *Do you expect the current war will be a long war for many months or will it end soon within weeks?*

**Options:**
- 1 = Long war over months
- 2 = End soon within weeks
""")

long_war = df_filtered[df_filtered['Q11'] == 'Long war over months']['WGT'].sum()
end_soon = df_filtered[df_filtered['Q11'] == 'End soon within weeks']['WGT'].sum()
total = df_filtered[df_filtered['Q11'].notna()]['WGT'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("📅 Long War (Months)", f"{(long_war/total*100):.1f}%" if total > 0 else "N/A")
with col2:
    st.metric("⚡ End Soon (Weeks)", f"{(end_soon/total*100):.1f}%" if total > 0 else "N/A")

# By country
duration_by_country = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q11'].notna())]
    c_total = cdf['WGT'].sum()
    
    if c_total > 0:
        duration_by_country.append({
            'Country': country,
            'Long War %': (cdf[cdf['Q11'] == 'Long war over months']['WGT'].sum() / c_total * 100),
            'End Soon %': (cdf[cdf['Q11'] == 'End soon within weeks']['WGT'].sum() / c_total * 100)
        })

duration_df = pd.DataFrame(duration_by_country)

fig = go.Figure()
fig.add_trace(go.Bar(name='Long War', y=duration_df['Country'], x=duration_df['Long War %'], orientation='h', marker_color='#ef4444'))
fig.add_trace(go.Bar(name='End Soon', y=duration_df['Country'], x=duration_df['End Soon %'], orientation='h', marker_color='#10b981'))
fig.update_layout(barmode='stack', title="War Duration Expectations by Country", height=500, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# Q12-Q13: MILITARY SUPPORT
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🎖️ Q12-Q13: Military Support for USA</div>', unsafe_allow_html=True)

# LIMITED DATA WARNING
st.markdown("""
<div style="background:#fef3c7;border-left:5px solid #f59e0b;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;">
<strong>⚠️ LIMITED DATA:</strong> Q12-Q14 were asked in <strong>only 3 countries</strong>: Germany, Portugal, and Spain. These results do NOT represent a global average - they reflect opinions in these three European nations only.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Q12: Should YOUR Country Support USA?")
    
    own_yes = df_filtered[df_filtered['Q12'] == 'Yes']['WGT'].sum()
    own_no = df_filtered[df_filtered['Q12'] == 'No']['WGT'].sum()
    own_total = df_filtered[df_filtered['Q12'].notna()]['WGT'].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=['Yes', 'No'],
        values=[own_yes, own_no],
        marker=dict(colors=['#3b82f6', '#ef4444']),
        hole=0.4
    )])
    fig.update_layout(title=f"Support: {(own_yes/own_total*100):.1f}% Yes", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Q13: Should EU Support USA?")
    
    eu_yes = df_filtered[df_filtered['Q13'] == 'Yes']['WGT'].sum()
    eu_no = df_filtered[df_filtered['Q13'] == 'No']['WGT'].sum()
    eu_total = df_filtered[df_filtered['Q13'].notna()]['WGT'].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=['Yes', 'No'],
        values=[eu_yes, eu_no],
        marker=dict(colors=['#3b82f6', '#ef4444']),
        hole=0.4
    )])
    fig.update_layout(title=f"Support: {(eu_yes/eu_total*100):.1f}% Yes", height=400)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# Q14: TERRORISM RISK
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">💣 Q14: Terrorism Risk</div>', unsafe_allow_html=True)

st.markdown("""
**Question:** *Do you think this war will increase the risk for terrorism attacks in your country?*

**Options:**
- 1 = Yes
- 2 = No
""")

# LIMITED DATA WARNING (same as Q12-Q13)
st.markdown("""
<div style="background:#fef3c7;border-left:5px solid #f59e0b;padding:1rem 1.2rem;border-radius:8px;margin:0.5rem 0 1rem 0;">
<strong>⚠️ LIMITED DATA:</strong> Only asked in Germany, Portugal, and Spain.
</div>
""", unsafe_allow_html=True)

terror_yes = df_filtered[df_filtered['Q14'] == 'Yes']['WGT'].sum()
terror_no = df_filtered[df_filtered['Q14'] == 'No']['WGT'].sum()
terror_total = df_filtered[df_filtered['Q14'].notna()]['WGT'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("⚠️ Yes, Increased Risk", f"{(terror_yes/terror_total*100):.1f}%")
with col2:
    st.metric("✅ No Increased Risk", f"{(terror_no/terror_total*100):.1f}%")

# By country
terror_by_country = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[(df_filtered['Country'] == country) & (df_filtered['Q14'].notna())]
    c_total = cdf['WGT'].sum()
    
    if c_total > 0:
        terror_by_country.append({
            'Country': country,
            'Yes %': (cdf[cdf['Q14'] == 'Yes']['WGT'].sum() / c_total * 100),
            'No %': (cdf[cdf['Q14'] == 'No']['WGT'].sum() / c_total * 100)
        })

terror_df = pd.DataFrame(terror_by_country).sort_values('Yes %', ascending=False)

fig = go.Figure(go.Bar(
    y=terror_df['Country'],
    x=terror_df['Yes %'],
    orientation='h',
    marker_color='#ef4444',
    text=[f"{v:.1f}%" for v in terror_df['Yes %']],
    textposition='outside'
))
fig.update_layout(title="% Expecting Increased Terrorism Risk", xaxis_title="Percentage (%)", height=500, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#5b21b6 0%,#6d28d9 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · War Expectations & Future Outlook</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
