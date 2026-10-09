import streamlit as st

st.set_page_config(page_title="Methodology | Iran Poll", page_icon="📋", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#1e3a8a 0%,#3b82f6 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.6rem;font-weight:700;color:#002147;margin:2.5rem 0 1rem;border-bottom:3px solid #3b82f6;padding-bottom:0.5rem;}
.content-box{background:white;padding:1.5rem 2rem;border-radius:12px;margin:1rem 0;box-shadow:0 2px 8px rgba(0,0,0,0.08);}
.highlight-box{background:#dbeafe;border-left:5px solid #3b82f6;padding:1.2rem 1.5rem;border-radius:8px;margin:1.5rem 0;}
.info-card{background:#f8fafc;border:1px solid #e2e8f0;padding:1.2rem;border-radius:8px;margin:1rem 0;}
ul{line-height:1.8;}
li{margin:0.5rem 0;}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-title">📋 Survey Methodology</div>
    <div class="hero-sub">Comprehensive methodological framework and sampling design</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Study Overview</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-box">
<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;">
The study was conducted by the <strong>Gallup International Association</strong> with a total sample of approximately <strong>15,000 respondents across 17 countries</strong>. The survey covers a diverse set of countries across Europe, Asia, and Latin America, with an average sample of around 873 respondents per country.
</p>

<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-top:1rem;">
The findings are based on adults who reported being aware of the war. Data were collected using nationally representative approaches, employing a mix of <strong>online and telephone interviews</strong> depending on country context. In some countries, non-probability online panels were used; further details on these approaches are provided in the full methodology note.
</p>

<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-top:1rem;">
Data were weighted to reflect national population characteristics, and global results are computed as averages across countries.
</p>
</div>
""", unsafe_allow_html=True)

# Fieldwork period
st.markdown("""
<div class="highlight-box">
<strong>📅 Fieldwork Period:</strong> 10th March – 30th March 2026
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# GEOGRAPHIC COVERAGE
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🌍 Geographic Coverage</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-box">
<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-bottom:1.5rem;">
The survey covers a total of <strong>17 countries across multiple regions</strong>, with a strong representation from Europe alongside key countries in Asia and Latin America. Together, this mix of advanced and emerging economies provides a diverse cross-regional perspective, combining views from both Western and non-Western societies across different economic and geopolitical contexts.
</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
    <h4 style="color:#1e3a8a;margin:0 0 1rem 0;">🇪🇺 Europe (8 countries)</h4>
    <ul style="margin:0;padding-left:1.5rem;">
        <li>Croatia</li>
        <li>Germany</li>
        <li>Portugal</li>
        <li>Serbia</li>
        <li>Slovenia</li>
        <li>Spain</li>
        <li>Sweden</li>
        <li>Switzerland</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
    <h4 style="color:#1e3a8a;margin:0 0 1rem 0;">🌏 Asia (7 countries)</h4>
    <ul style="margin:0;padding-left:1.5rem;">
        <li>Armenia</li>
        <li>Georgia</li>
        <li>Japan</li>
        <li>Pakistan</li>
        <li>Philippines</li>
        <li>Republic of Korea</li>
        <li>Turkey</li>
    </ul>
    <p style="font-size:0.9rem;color:#64748b;margin-top:0.5rem;">
    Covering East, Southeast, South, and West Asia
    </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
    <h4 style="color:#1e3a8a;margin:0 0 1rem 0;">🌎 Latin America (2 countries)</h4>
    <ul style="margin:0;padding-left:1.5rem;">
        <li>Colombia</li>
        <li>Mexico</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SAMPLING DESIGN
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📐 Sampling Design & Methodology</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-box">
<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-bottom:1.5rem;">
Across the 17 countries covered in this study, <strong>nationally representative samples were achieved in 15 countries</strong>, while 2 countries had more limited or non-national coverage due to methodological constraints.
</p>

<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;">
Out of 17 countries, <strong>10 used probability-based sampling</strong>, <strong>5 used quota sampling</strong>, and <strong>2 relied on non-probability samples</strong>.
</p>
</div>
""", unsafe_allow_html=True)

# Sampling methods breakdown
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card" style="background:#dcfce7;border-left:4px solid #16a34a;">
    <h4 style="color:#15803d;margin:0 0 1rem 0;">✅ Random Probability</h4>
    <p style="font-weight:600;color:#15803d;margin-bottom:0.5rem;">10 Countries</p>
    <ul style="margin:0;padding-left:1.5rem;font-size:0.95rem;">
        <li>Armenia</li>
        <li>Croatia</li>
        <li>Georgia</li>
        <li>Germany</li>
        <li>Pakistan</li>
        <li>Serbia</li>
        <li>Slovenia</li>
        <li>Sweden</li>
        <li>Switzerland</li>
        <li>Turkey</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card" style="background:#fef3c7;border-left:4px solid #f59e0b;">
    <h4 style="color:#b45309;margin:0 0 1rem 0;">📊 Quota Sampling</h4>
    <p style="font-weight:600;color:#b45309;margin-bottom:0.5rem;">5 Countries</p>
    <ul style="margin:0;padding-left:1.5rem;font-size:0.95rem;">
        <li>Colombia</li>
        <li>Japan</li>
        <li>Portugal</li>
        <li>Republic of Korea</li>
        <li>Spain</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card" style="background:#fee2e2;border-left:4px solid #dc2626;">
    <h4 style="color:#991b1b;margin:0 0 1rem 0;">⚠️ Non-Probability</h4>
    <p style="font-weight:600;color:#991b1b;margin-bottom:0.5rem;">2 Countries</p>
    <ul style="margin:0;padding-left:1.5rem;font-size:0.95rem;">
        <li>Mexico</li>
        <li>Philippines</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Important note about margin of error
st.markdown("""
<div class="highlight-box" style="background:#fef3c7;border-left:5px solid #f59e0b;">
<strong>⚠️ Important Note on Margin of Error:</strong><br><br>
Given the use of non-probability sampling in some countries, a conventional margin of error is not reported, as it is not strictly applicable in such designs. Accordingly, the findings should be interpreted with appropriate caution and viewed as <strong>indicative of public sentiment rather than precise population estimates</strong>, particularly when making cross-country comparisons.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SAMPLE SIZES BY COUNTRY
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Sample Sizes by Country</div>', unsafe_allow_html=True)

# Create sample size data
sample_data = {
    'Country': [
        '🇦🇲 Armenia', '🇨🇴 Colombia', '🇭🇷 Croatia', '🇬🇪 Georgia', '🇩🇪 Germany',
        '🇯🇵 Japan', '🇲🇽 Mexico', '🇵🇰 Pakistan', '🇵🇭 Philippines', '🇵🇹 Portugal',
        '🇷🇸 Serbia', '🇸🇮 Slovenia', '🇪🇸 Spain', '🇸🇪 Sweden', '🇨🇭 Switzerland',
        '🇹🇷 Turkey', '🇰🇷 South Korea'
    ],
    'Sample Size': [
        1001, 866, 786, 943, 800,
        927, 830, 894, 800, 620,
        802, 785, 1023, 1051, 800,
        804, 1121
    ],
    'Method': [
        'Probability', 'Quota', 'Probability', 'Probability', 'Probability',
        'Quota', 'Non-Probability', 'Probability', 'Non-Probability', 'Quota',
        'Probability', 'Probability', 'Quota', 'Probability', 'Probability',
        'Probability', 'Quota'
    ]
}

import pandas as pd
sample_df = pd.DataFrame(sample_data)

# Display as styled table
st.dataframe(
    sample_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Country": st.column_config.TextColumn("Country", width="medium"),
        "Sample Size": st.column_config.NumberColumn("Sample Size", format="%d"),
        "Method": st.column_config.TextColumn("Sampling Method", width="medium")
    }
)

# Total
st.markdown("""
<div class="highlight-box">
<strong>📊 Total Sample:</strong> 14,853 respondents across 17 countries
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ABOUT GALLUP INTERNATIONAL
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🏛️ About Gallup International Association</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-box">
<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-bottom:1rem;">
<strong>Gallup International Association (GIA)</strong> is the world's leading global independent association in market research and public opinion polling.
</p>

<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-bottom:1rem;">
For more than <strong>75 years</strong>, Gallup International members have demonstrated their expertise in conducting multi-country surveys on a fully comparable basis, consistently delivering research of the highest methodological quality. Today, the Association brings together <strong>over 65 members</strong> who together with partners have the capacity to cover <strong>more than 130 countries</strong> of the world with opinion polling.
</p>

<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-bottom:1rem;">
Each member is a leading national research institute with deep local expertise in research methods, statistical systems, culture, and social context.
</p>

<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;margin-bottom:1rem;">
With a <strong>strict one-member-per-country policy</strong>, Gallup International ensures independence, credibility, and the highest professional standards. Member agencies collaborate closely on a daily basis, sharing knowledge, innovative research techniques, and tools, while jointly delivering robust, reliable, and culturally informed insights for international research projects.
</p>

<p style="font-size:1.05rem;line-height:1.8;color:#1e293b;">
Gallup International was founded in <strong>1947 by George Gallup</strong>, the pioneer of modern scientific public opinion research together with colleagues from 10 countries.
</p>
</div>
""", unsafe_allow_html=True)

# Key stats about GIA
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="text-align:center;padding:1.5rem;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
        <p style="font-size:2.5rem;font-weight:800;color:#1e3a8a;margin:0;">75+</p>
        <p style="font-size:0.9rem;color:#64748b;margin:0.5rem 0 0 0;">Years of Excellence</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align:center;padding:1.5rem;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
        <p style="font-size:2.5rem;font-weight:800;color:#1e3a8a;margin:0;">65+</p>
        <p style="font-size:0.9rem;color:#64748b;margin:0.5rem 0 0 0;">Member Organizations</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align:center;padding:1.5rem;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
        <p style="font-size:2.5rem;font-weight:800;color:#1e3a8a;margin:0;">130+</p>
        <p style="font-size:0.9rem;color:#64748b;margin:0.5rem 0 0 0;">Countries Coverage</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="text-align:center;padding:1.5rem;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
        <p style="font-size:2.5rem;font-weight:800;color:#1e3a8a;margin:0;">1947</p>
        <p style="font-size:0.9rem;color:#64748b;margin:0.5rem 0 0 0;">Year Founded</p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════

st.markdown('<div style="border-top:2px solid #e2e8f0;margin:3rem 0 1rem 0;"></div>', unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
with col_f1:
    st.image("GIA.png", width=180)
with col_f3:
    st.image("GDAP_LOGO.png", width=180)

st.markdown("""
<div style="text-align:center;padding:1.5rem;background:#f8fafc;border-radius:12px;margin-top:1rem;">
    <p style="opacity:0.7;margin:0;font-size:0.85rem;">Iran War Poll 2026 · Developed by <a href="https://galluppakistandigitalanalytics.com" target="_blank" style="color:#002147;text-decoration:none;font-weight:600;">Gallup Pakistan Digital Analytics</a> for Gallup International Association</p>
</div>
""", unsafe_allow_html=True)
