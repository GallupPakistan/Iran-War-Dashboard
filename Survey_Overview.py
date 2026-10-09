import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Iran War Poll 2026 | Survey Overview", page_icon="🌍", layout="wide")

# ══════════════════════════════════════════════════════════════════
# STYLING
# ══════════════════════════════════════════════════════════════════

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}

.hero-banner{
    background:linear-gradient(135deg,#002147 0%,#0057b8 70%,#4a90d9 100%);
    padding:3rem 2rem;
    border-radius:16px;
    color:white;
    margin-bottom:2rem;
    box-shadow:0 8px 24px rgba(0,33,71,0.15);
}
.hero-title{font-size:2.8rem;font-weight:800;margin:0;line-height:1.2;}
.hero-subtitle{font-size:1.2rem;opacity:0.9;margin-top:0.5rem;}
.hero-meta{font-size:0.95rem;opacity:0.75;margin-top:1rem;}

.stat-card{
    background:white;
    padding:1.5rem;
    border-radius:12px;
    border-left:4px solid #0057b8;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
    transition:transform 0.2s;
}
.stat-card:hover{transform:translateY(-4px);box-shadow:0 4px 16px rgba(0,0,0,0.12);}
.stat-number{font-size:2.5rem;font-weight:800;color:#002147;margin:0;}
.stat-label{font-size:0.9rem;color:#64748b;margin-top:0.3rem;text-transform:uppercase;letter-spacing:0.5px;}

.nav-card{
    background:white;
    padding:1.8rem;
    border-radius:12px;
    box-shadow:0 2px 12px rgba(0,0,0,0.08);
    transition:all 0.3s;
    height:100%;
    cursor:pointer;
}
.nav-card:hover{
    transform:translateY(-6px);
    box-shadow:0 8px 24px rgba(0,0,0,0.15);
}
.nav-icon{font-size:2.5rem;margin-bottom:0.8rem;}
.nav-title{font-size:1.3rem;font-weight:700;color:#002147;margin-bottom:0.5rem;}
.nav-desc{font-size:0.9rem;color:#64748b;line-height:1.6;}
.nav-badge{
    display:inline-block;
    padding:0.3rem 0.8rem;
    border-radius:20px;
    font-size:0.75rem;
    font-weight:700;
    margin-top:0.8rem;
}

.section-title{
    font-size:1.5rem;
    font-weight:700;
    color:#002147;
    margin:2rem 0 1rem;
    padding-bottom:0.5rem;
    border-bottom:3px solid #0057b8;
}

.finding-card{
    background:linear-gradient(135deg,#fef3c7 0%,#fde68a 100%);
    padding:1.5rem;
    border-radius:12px;
    border-left:5px solid #f59e0b;
    margin:1rem 0;
}
.finding-title{font-size:1.1rem;font-weight:700;color:#92400e;margin-bottom:0.5rem;}
.finding-text{font-size:0.95rem;color:#78350f;line-height:1.6;}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner="⚡ Loading Iran War Poll data...")
def load_data():
    df = pd.read_excel("Iran_Snap_Poll_2026_-_Merged_Data_Working_File__17_Countries_.xlsx")
    codebook = pd.read_csv("EOY_IRAN_CODE_BOOK_APR26.csv")
    
    # Map countries
    # CountryID is already the country name in new data
    df["Country"] = df["CountryID"]
    # Armenia was screened via survey invitation (Q1 implicit Yes) - fill for correct analysis
    df.loc[df["CountryID"] == "Armenia", "Q1"] = "Yes"
    
    return df, codebook

df, codebook = load_data()

# ══════════════════════════════════════════════════════════════════
# GALLUP PAKISTAN HEADER
# ══════════════════════════════════════════════════════════════════

# Load and display logos
col_logo1, col_logo2, col_logo3 = st.columns([2, 1, 2])

with col_logo1:
    st.image("GIA.png", width=280)

with col_logo3:
    st.image("GDAP_LOGO.png", width=280)

st.markdown('<div style="border-bottom:3px solid #002147;margin:1rem 0 1.5rem 0;"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🌍 Iran War Poll 2026</div>
    <div class="hero-subtitle">Global Public Opinion on the Middle East Conflict</div>
    <div class="hero-meta">USA-Israel-Iran War · 17 countries · 14,853 Respondents</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# KEY STATISTICS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">📊 Survey at a Glance</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">17</div>
        <div class="stat-label">Countries Surveyed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color:#10b981;">
        <div class="stat-number">{len(df):,}</div>
        <div class="stat-label">Total Respondents</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color:#f59e0b;">
        <div class="stat-number">{int(df['WGT'].sum()):,}</div>
        <div class="stat-label">Weighted Sample</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    awareness = (df['Q1'] == 'Yes').sum() / df['Q1'].notna().sum() * 100
    st.markdown(f"""
    <div class="stat-card" style="border-left-color:#ef4444;">
        <div class="stat-number">{awareness:.0f}%</div>
        <div class="stat-label">War Awareness</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# KEY FINDINGS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">🔍 Top Findings</div>', unsafe_allow_html=True)

# Calculate key metrics
# Use respondents who answered Q2 (includes Armenia which skipped Q1 screener)
df_q2 = df[df['Q2'].notna()].copy()
df_q3 = df[df['Q3_1'].notna()].copy()

# Support distribution (among all who answered Q2)
if len(df_q2) > 0:
    total_wgt = df_q2['WGT'].sum()
    usa_israel_pct = (df_q2[df_q2['Q2'] == 'USA-Israel coalition']['WGT'].sum() / total_wgt * 100)
    iran_pct = (df_q2[df_q2['Q2'] == 'Iran']['WGT'].sum() / total_wgt * 100)
    neither_pct = (df_q2[df_q2['Q2'] == 'Neither of them']['WGT'].sum() / total_wgt * 100)
    
    # Expected harm (Q3 asked to those who answered Q3)
    strong_harm = (df_q3[df_q3['Q3_1'] == 'Strong harm expected']['WGT'].sum() / df_q3['WGT'].sum() * 100) if len(df_q3) > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="finding-card">
            <div class="finding-title">🎯 War Support Split</div>
            <div class="finding-text">
                Among those aware of the war:<br>
                • <strong>{usa_israel_pct:.1f}%</strong> support USA-Israel coalition<br>
                • <strong>{iran_pct:.1f}%</strong> support Iran<br>
                • <strong>{neither_pct:.1f}%</strong> support neither side
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="finding-card" style="background:linear-gradient(135deg,#fecaca 0%,#fca5a5 100%);border-left-color:#ef4444;">
            <div class="finding-title" style="color:#7f1d1d;">💥 Expected Personal Impact</div>
            <div class="finding-text" style="color:#991b1b;">
                <strong>{strong_harm:.1f}%</strong> expect strong physical harm if war continues<br>
                High concern levels across multiple countries
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# COUNTRIES SURVEYED MAP
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">🗺️ Geographic Coverage</div>', unsafe_allow_html=True)

# Country list with sample sizes
country_stats = df.groupby('Country').agg({
    'RespID': 'count',
    'WGT': 'sum'
}).reset_index()
country_stats.columns = ['Country', 'Sample Size', 'Weighted N']
country_stats = country_stats.sort_values('Sample Size', ascending=False)

col1, col2 = st.columns([2, 1])

with col1:
    # World map showing surveyed countries
    country_codes = {
        'Colombia': 'COL', 'Croatia': 'HRV', 'Germany': 'DEU', 'Japan': 'JPN',
        'Mexico': 'MEX', 'Pakistan': 'PAK', 'Philippines': 'PHL', 'Portugal': 'PRT',
        'Serbia': 'SRB', 'Slovenia': 'SVN', 'Spain': 'ESP', 'Sweden': 'SWE',
        'Switzerland': 'CHE', 'Turkey': 'TUR', 'South Korea': 'KOR'
    }
    
    country_stats['ISO'] = country_stats['Country'].map(country_codes)
    
    fig = go.Figure(data=go.Choropleth(
        locations=country_stats['ISO'],
        z=country_stats['Sample Size'],
        text=country_stats['Country'],
        colorscale='Blues',
        marker_line_color='white',
        marker_line_width=0.5,
        colorbar_title="Sample<br>Size"
    ))
    
    fig.update_layout(
        title="Countries Surveyed",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.dataframe(
        country_stats,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Country": st.column_config.TextColumn("Country", width="medium"),
            "Sample Size": st.column_config.NumberColumn("Sample", format="%d"),
            "Weighted N": st.column_config.NumberColumn("Weighted", format="%.0f")
        }
    )

# ══════════════════════════════════════════════════════════════════
# NAVIGATION CARDS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">📑 Explore Analysis Pages</div>', unsafe_allow_html=True)
st.info("👇 Click any card below to dive into detailed analysis")

# Row 1
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #3b82f6;">
        <div class="nav-icon">🎯</div>
        <div class="nav-title">War Awareness & Support</div>
        <div class="nav-desc">Who supports whom? Detailed breakdown of public opinion on the USA-Israel-Iran conflict.</div>
        <span class="nav-badge" style="background:#dbeafe;color:#1e40af;">15+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_War_Awareness_Support.py", label="🎯 Go to Analysis →", use_container_width=True)

with col2:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #ef4444;">
        <div class="nav-icon">💥</div>
        <div class="nav-title">Expected Personal Harm</div>
        <div class="nav-desc">Physical, financial, and emotional impact expectations across all countries.</div>
        <span class="nav-badge" style="background:#fee2e2;color:#991b1b;">20+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Expected_Harm.py", label="💥 Go to Analysis →", use_container_width=True)

with col3:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #10b981;">
        <div class="nav-icon">🌐</div>
        <div class="nav-title">Global Actors' Policies</div>
        <div class="nav-desc">Satisfaction with UN, EU, Russia, China, and other global powers' responses.</div>
        <span class="nav-badge" style="background:#d1fae5;color:#065f46;">25+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/6_Global_Actors.py", label="🌐 Go to Analysis →", use_container_width=True)

# Row 2
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #7c3aed;">
        <div class="nav-icon">⚔️</div>
        <div class="nav-title">War Predictions & Responsibility</div>
        <div class="nav-desc">Who will win? Who started it? Global perspectives on the conflict.</div>
        <span class="nav-badge" style="background:#ede9fe;color:#5b21b6;">15+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Predictions_Responsibility.py", label="⚔️ Go to Analysis →", use_container_width=True)

with col2:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #0891b2;">
        <div class="nav-icon">🎭</div>
        <div class="nav-title">Khamenei Assessment</div>
        <div class="nav-desc">Public opinion on the assassination of Iran's Supreme Leader.</div>
        <span class="nav-badge" style="background:#cffafe;color:#164e63;">10+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Khamenei_Assessment.py", label="🎭 Go to Analysis →", use_container_width=True)

with col3:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #db2777;">
        <div class="nav-icon">🏛️</div>
        <div class="nav-title">Government Policy Satisfaction</div>
        <div class="nav-desc">Trust and satisfaction with own government's war response.</div>
        <span class="nav-badge" style="background:#fce7f3;color:#831843;">12+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/5_Government_Satisfaction.py", label="🏛️ Go to Analysis →", use_container_width=True)

# Row 3
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #8b5cf6;">
        <div class="nav-icon">🔮</div>
        <div class="nav-title">War Expectations & Future Outlook</div>
        <div class="nav-desc">Regime change, outcomes, duration, military support, and terrorism risks.</div>
        <span class="nav-badge" style="background:#ede9fe;color:#5b21b6;">18+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/7_War_Expectations.py", label="🔮 Go to Analysis →", use_container_width=True)

with col2:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #6366f1;">
        <div class="nav-icon">👥</div>
        <div class="nav-title">Demographics Deep Dive</div>
        <div class="nav-desc">Complete demographic analysis by gender, age, income, education, religion.</div>
        <span class="nav-badge" style="background:#e0e7ff;color:#3730a3;">30+ Charts</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/9_Demographics.py", label="👥 Go to Analysis →", use_container_width=True)

with col3:
    st.markdown("""
    <div class="nav-card" style="border-left:4px solid #0ea5e9;">
        <div class="nav-icon">🔍</div>
        <div class="nav-title">Country Comparison Tool</div>
        <div class="nav-desc">Interactive side-by-side comparison across all survey dimensions.</div>
        <span class="nav-badge" style="background:#e0f2fe;color:#075985;">Interactive</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/8_Country_Comparison.py", label="🔍 Go to Analysis →", use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# METHODOLOGY
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">📋 Survey Methodology</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Sampling Approach:**
    - Multi-stage stratified probability sampling
    - Nationally representative samples per country
    - Post-stratification weighting applied
    - Margin of error: ±3-5% at 95% confidence level
    """)

with col2:
    st.markdown("""
    **Data Collection:**
    - Methods: Online, telephone, face-to-face
    - Quality control procedures implemented
    - Weighted analysis throughout dashboard
    """)

# ══════════════════════════════════════════════════════════════════
# DISCLAIMER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div style="background:#fef3c7;border-left:5px solid #f59e0b;padding:1.2rem;border-radius:8px;margin:2rem 0;">
<strong>⚠️ Disclaimer:</strong> Gallup International Association or its members are not related to Gallup Inc., headquartered in Washington D.C. which is no longer a member of Gallup International Association. Gallup International Association does not accept responsibility for opinion polling other than its own. We require that our surveys be credited fully as <strong>Gallup International</strong> (not Gallup).
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════

# Footer logos
col_f1, col_f2, col_f3 = st.columns([1, 1, 1])

with col_f1:
    st.image("GIA.png", width=200)

with col_f3:
    st.image("GDAP_LOGO.png", width=200)

st.markdown("""
<div style="text-align:center;padding:2rem;background:linear-gradient(135deg,#001833 0%,#002d6e 100%);border-radius:16px;color:white;margin-top:1.5rem;">
    <p style="opacity:0.85;margin:0;font-size:1rem;">Iran War Poll 2026 · 17 countries · 14,853 Respondents</p>
    <p style="opacity:0.7;margin:1rem 0 0;font-size:0.9rem;">Developed by <a href="https://galluppakistandigitalanalytics.com" target="_blank" style="color:#F9E795;text-decoration:none;font-weight:600;">Gallup Pakistan Digital Analytics</a> for Gallup International Association</p>
</div>
""", unsafe_allow_html=True)
