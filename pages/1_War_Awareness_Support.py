import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="War Awareness & Support | Iran Poll", page_icon="🎯", layout="wide")

# ══════════════════════════════════════════════════════════════════
# STYLING
# ══════════════════════════════════════════════════════════════════

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#002147 0%,#0057b8 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #0057b8;padding-bottom:0.5rem;}
.insight-box{background:#fef3c7;border-left:5px solid #f59e0b;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;}
.insight-box strong{color:#92400e;}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    df = pd.read_excel("Iran_Snap_Poll_2026_-_Merged_Data_Working_File__17_Countries_.xlsx")
    codebook = pd.read_csv("EOY_IRAN_CODE_BOOK_APR26.csv")
    
    # CountryID is already the country name in new data
    df["Country"] = df["CountryID"]
    # Armenia was screened via survey invitation (Q1 implicit Yes) - fill for correct analysis
    df.loc[df["CountryID"] == "Armenia", "Q1"] = "Yes"
    return df, codebook

df, codebook = load_data()

# ══════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-title">🎯 War Awareness & Support Analysis</div>
    <div class="hero-sub">Who knows about the conflict and which side do they support?</div>
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
# Q1: WAR AWARENESS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📻 Q1: War Awareness</div>', unsafe_allow_html=True)
st.markdown("*Have you heard about a war in the Middle East between the USA, Israel, and Iran these days?*")

# SCREENER WARNING
st.markdown("""
<div style="background:#fee2e2;border-left:5px solid #dc2626;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;">
<strong>⚠️ SCREENER QUESTION:</strong> Q1 was used to screen respondents. Only those who answered 'Yes' (heard about the war) continued with the survey. The 100% awareness rate reflects <strong>survey design</strong> - respondents who were unaware were excluded from the study entirely. This does NOT indicate universal awareness in these populations.
</div>
""", unsafe_allow_html=True)

# Overall awareness - only count respondents where Q1 was actually asked
df_q1 = df_filtered[df_filtered['Q1'].notna()]
total_wgt = df_q1['WGT'].sum()
aware_wgt = df_q1[df_q1['Q1'] == 'Yes']['WGT'].sum()
not_aware_wgt = df_q1[df_q1['Q1'] == 'No']['WGT'].sum()

aware_pct = (aware_wgt / total_wgt * 100) if total_wgt > 0 else 0
not_aware_pct = (not_aware_wgt / total_wgt * 100) if total_wgt > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("✅ Aware of War", f"{aware_pct:.1f}%", f"{int(aware_wgt):,} respondents")
with col2:
    st.metric("❌ Not Aware", f"{not_aware_pct:.1f}%", f"{int(not_aware_wgt):,} respondents")
with col3:
    st.metric("📊 Total Sample", f"{len(df_filtered):,}", f"{int(df_filtered['WGT'].sum()):,} weighted")

# Chart 1: Awareness by Country
st.markdown("#### 📊 War Awareness by Country")

awareness_by_country = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[df_filtered['Country'] == country]
    # Skip countries where Q1 was not asked (all NaN)
    if cdf['Q1'].isna().all():
        continue
    c_total = cdf['WGT'].sum()
    c_aware = cdf[cdf['Q1'] == 'Yes']['WGT'].sum()
    awareness_by_country.append({
        'Country': country,
        'Aware %': (c_aware / c_total * 100) if c_total > 0 else 0,
        'Sample': len(cdf)
    })

aware_df = pd.DataFrame(awareness_by_country).sort_values('Aware %', ascending=False)

fig = go.Figure()
fig.add_trace(go.Bar(
    y=aware_df['Country'],
    x=aware_df['Aware %'],
    orientation='h',
    text=[f"{v:.1f}%" for v in aware_df['Aware %']],
    textposition='outside',
    marker_color='#3b82f6',
    hovertemplate='<b>%{y}</b><br>%{x:.1f}%<br>Sample: %{customdata:,}<extra></extra>',
    customdata=aware_df['Sample']
))

fig.update_layout(
    title="Percentage Who Have Heard About the War",
    xaxis_title="Percentage (%)",
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# No insight box needed - all countries show 100% due to screener design

# ══════════════════════════════════════════════════════════════════
# Q2: SUPPORT DISTRIBUTION (Among Aware Respondents)
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🏳️ Q2: Which Side Do You Support?</div>', unsafe_allow_html=True)

# df_q2: all respondents who answered Q2 (Armenia Q1 filled as 'Yes' at load time)
df_q2 = df_filtered[df_filtered['Q2'].notna()].copy()

if len(df_q2) > 0:
    # Overall support
    aware_total = df_q2['WGT'].sum()
    usa_israel_wgt = df_q2[df_q2['Q2'] == 'USA-Israel coalition']['WGT'].sum()
    iran_wgt = df_q2[df_q2['Q2'] == 'Iran']['WGT'].sum()
    neither_wgt = df_q2[df_q2['Q2'] == 'Neither of them']['WGT'].sum()
    dk_wgt = df_q2[df_q2['Q2'] == "Don't know / No response"]['WGT'].sum()
    
    usa_israel_pct = (usa_israel_wgt / aware_total * 100) if aware_total > 0 else 0
    iran_pct = (iran_wgt / aware_total * 100) if aware_total > 0 else 0
    neither_pct = (neither_wgt / aware_total * 100) if aware_total > 0 else 0
    dk_pct = (dk_wgt / aware_total * 100) if aware_total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🇺🇸🇮🇱 USA-Israel", f"{usa_israel_pct:.1f}%")
    with col2:
        st.metric("🇮🇷 Iran", f"{iran_pct:.1f}%")
    with col3:
        st.metric("⚖️ Neither", f"{neither_pct:.1f}%")
    with col4:
        st.metric("❓ Don't Know", f"{dk_pct:.1f}%")
    
    # Chart 2: Overall Support Distribution (Donut)
    st.markdown("#### 🥧 Overall Support Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        support_data = pd.DataFrame({
            'Position': ['USA-Israel Coalition', 'Iran', 'Neither', "Don't Know"],
            'Percentage': [usa_israel_pct, iran_pct, neither_pct, dk_pct],
            'Weighted N': [usa_israel_wgt, iran_wgt, neither_wgt, dk_wgt]
        })
        
        fig = go.Figure(data=[go.Pie(
            labels=support_data['Position'],
            values=support_data['Weighted N'],
            hole=0.4,
            marker=dict(colors=['#3b82f6', '#10b981', '#f59e0b', '#94a3b8']),
            textinfo='label+percent',
            textfont=dict(size=13)
        )])
        
        fig.update_layout(
            title="Among Those Aware of War",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bar chart
        fig = go.Figure()
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#94a3b8']
        for i, row in support_data.iterrows():
            fig.add_trace(go.Bar(
                x=[row['Percentage']],
                y=[row['Position']],
                orientation='h',
                text=f"{row['Percentage']:.1f}%",
                textposition='outside',
                marker_color=colors[i],
                name=row['Position'],
                showlegend=False
            ))
        
        fig.update_layout(
            title="Support Percentages",
            xaxis_title="Percentage (%)",
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Chart 3: Support by Country (Stacked Bar)
    st.markdown("#### 🌍 Support Distribution by Country")
    
    support_by_country = []
    for country in sorted(df_q2['Country'].dropna().unique()):
        cdf = df_q2[df_q2['Country'] == country]
        c_total = cdf['WGT'].sum()
        
        support_by_country.append({
            'Country': country,
            'USA-Israel %': (cdf[cdf['Q2'] == 'USA-Israel coalition']['WGT'].sum() / c_total * 100) if c_total > 0 else 0,
            'Iran %': (cdf[cdf['Q2'] == 'Iran']['WGT'].sum() / c_total * 100) if c_total > 0 else 0,
            'Neither %': (cdf[cdf['Q2'] == 'Neither of them']['WGT'].sum() / c_total * 100) if c_total > 0 else 0,
            "Don't Know %": (cdf[cdf['Q2'] == "Don't know / No response"]['WGT'].sum() / c_total * 100) if c_total > 0 else 0
        })
    
    support_country_df = pd.DataFrame(support_by_country)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='USA-Israel',
        y=support_country_df['Country'],
        x=support_country_df['USA-Israel %'],
        orientation='h',
        marker_color='#3b82f6',
        text=[f"{v:.0f}%" if v > 5 else "" for v in support_country_df['USA-Israel %']],
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        name='Iran',
        y=support_country_df['Country'],
        x=support_country_df['Iran %'],
        orientation='h',
        marker_color='#10b981',
        text=[f"{v:.0f}%" if v > 5 else "" for v in support_country_df['Iran %']],
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        name='Neither',
        y=support_country_df['Country'],
        x=support_country_df['Neither %'],
        orientation='h',
        marker_color='#f59e0b',
        text=[f"{v:.0f}%" if v > 5 else "" for v in support_country_df['Neither %']],
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        name="Don't Know",
        y=support_country_df['Country'],
        x=support_country_df["Don't Know %"],
        orientation='h',
        marker_color='#94a3b8',
        text=[f"{v:.0f}%" if v > 5 else "" for v in support_country_df["Don't Know %"]],
        textposition='inside'
    ))
    
    fig.update_layout(
        barmode='stack',
        title="Support Breakdown by Country (Weighted %)",
        xaxis_title="Percentage (%)",
        height=600,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Chart 4: Heatmap - Support by Country
    st.markdown("#### 🔥 Support Heatmap")
    
    heatmap_data = support_country_df[['USA-Israel %', 'Iran %', 'Neither %', "Don't Know %"]].values
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=['USA-Israel', 'Iran', 'Neither', "Don't Know"],
        y=support_country_df['Country'],
        colorscale='RdYlGn',
        text=heatmap_data.round(1),
        texttemplate='%{text:.1f}%',
        textfont={"size": 11},
        colorbar=dict(title="Percentage")
    ))
    
    fig.update_layout(
        title="Support Patterns Across Countries",
        height=500,
        xaxis_title="Position",
        yaxis_title="Country"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Chart 5: Top Supporters Analysis
    st.markdown("#### 🏆 Top Supporters by Position")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🇺🇸🇮🇱 USA-Israel Coalition**")
        top_usa = support_country_df.nlargest(5, 'USA-Israel %')[['Country', 'USA-Israel %']]
        st.dataframe(top_usa, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("**🇮🇷 Iran**")
        top_iran = support_country_df.nlargest(5, 'Iran %')[['Country', 'Iran %']]
        st.dataframe(top_iran, hide_index=True, use_container_width=True)
    
    with col3:
        st.markdown("**⚖️ Neither Side**")
        top_neither = support_country_df.nlargest(5, 'Neither %')[['Country', 'Neither %']]
        st.dataframe(top_neither, hide_index=True, use_container_width=True)
    
    # DEMOGRAPHIC ANALYSIS
    st.markdown('<div class="section-header">👥 Support by Demographics</div>', unsafe_allow_html=True)
    
    # By Gender
    st.markdown("#### 👫 Support by Gender")
    
    gender_support = []
    for gender_label in ['Male', 'Female']:
        gdf = df_q2[df_q2['D1'] == gender_label]
        g_total = gdf['WGT'].sum()
        
        if g_total > 0:
            gender_support.append({
                'Gender': gender_label,
                'USA-Israel': (gdf[gdf['Q2'] == 'USA-Israel coalition']['WGT'].sum() / g_total * 100),
                'Iran': (gdf[gdf['Q2'] == 'Iran']['WGT'].sum() / g_total * 100),
                'Neither': (gdf[gdf['Q2'] == 'Neither of them']['WGT'].sum() / g_total * 100)
            })
    
    if gender_support:
        gender_df = pd.DataFrame(gender_support)
        
        fig = go.Figure()
        for col, color in [('USA-Israel', '#3b82f6'), ('Iran', '#10b981'), ('Neither', '#f59e0b')]:
            fig.add_trace(go.Bar(
                name=col,
                x=gender_df['Gender'],
                y=gender_df[col],
                text=[f"{v:.1f}%" for v in gender_df[col]],
                textposition='outside',
                marker_color=color
            ))
        
        fig.update_layout(
            barmode='group',
            title="Support by Gender",
            yaxis_title="Percentage (%)",
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # By Age Group
    st.markdown("#### 📅 Support by Age Group")
    
    age_labels = ['18 – 24', '25 – 34', '35 – 44', '45 – 54', '55 – 64', '65+']
    age_support = []
    
    for age_label in age_labels:
        adf = df_q2[df_q2['D2B'] == age_label]
        a_total = adf['WGT'].sum()
        
        if a_total > 100:  # Minimum sample
            age_support.append({
                'Age Group': age_label,
                'USA-Israel': (adf[adf['Q2'] == 'USA-Israel coalition']['WGT'].sum() / a_total * 100),
                'Iran': (adf[adf['Q2'] == 'Iran']['WGT'].sum() / a_total * 100),
                'Neither': (adf[adf['Q2'] == 'Neither of them']['WGT'].sum() / a_total * 100)
            })
    
    if age_support:
        age_df = pd.DataFrame(age_support)
        
        fig = go.Figure()
        for col, color in [('USA-Israel', '#3b82f6'), ('Iran', '#10b981'), ('Neither', '#f59e0b')]:
            fig.add_trace(go.Scatter(
                name=col,
                x=age_df['Age Group'],
                y=age_df[col],
                mode='lines+markers',
                marker=dict(size=10, color=color),
                line=dict(width=3, color=color)
            ))
        
        fig.update_layout(
            title="Support Trends Across Age Groups",
            yaxis_title="Percentage (%)",
            height=400,
            template="plotly_white",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No respondents are aware of the war in the selected countries.")

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#001833 0%,#002d6e 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · War Awareness & Support Analysis</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
