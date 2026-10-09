import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="Demographics | Iran Poll", page_icon="👥", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu,footer,header{visibility:hidden;}
.main{background:#f0f4f8;}
.hero{background:linear-gradient(135deg,#6366f1 0%,#4f46e5 70%);padding:2rem;border-radius:14px;color:white;margin-bottom:1.5rem;}
.hero-title{font-size:2.2rem;font-weight:800;margin:0;}
.hero-sub{font-size:1rem;opacity:0.88;margin-top:0.4rem;}
.section-header{font-size:1.4rem;font-weight:700;color:#002147;margin:2rem 0 1rem;border-bottom:3px solid #6366f1;padding-bottom:0.5rem;}
.insight-box{background:#e0e7ff;border-left:5px solid #6366f1;padding:1rem 1.2rem;border-radius:8px;margin:1rem 0;color:#3730a3;}
.insight-box strong{color:#4338ca;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:#002147;padding:.4rem;border-radius:12px;}
.stTabs [data-baseweb="tab"]{height:46px;padding:0 22px;background:rgba(255,255,255,.1);border-radius:9px;color:#90b8e8 !important;font-weight:700;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#6366f1 0%,#4f46e5 100%) !important;color:white !important;font-weight:800 !important;}
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
    <div class="hero-title">👥 Demographics Deep Dive</div>
    <div class="hero-sub">Complete demographic profile of survey respondents</div>
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
# OVERVIEW
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Demographic Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Gender
male_pct = (df_filtered[df_filtered['D1'] == 'Male']['WGT'].sum() / df_filtered['WGT'].sum() * 100)
female_pct = (df_filtered[df_filtered['D1'] == 'Female']['WGT'].sum() / df_filtered['WGT'].sum() * 100)

with col1:
    st.metric("👨 Male", f"{male_pct:.1f}%")
    
with col2:
    st.metric("👩 Female", f"{female_pct:.1f}%")

# Average age (approximate from age groups)
age_groups = df_filtered[df_filtered['D2B'].notna()]['D2B'].value_counts()

with col3:
    st.metric("📊 Age Groups", f"{len(age_groups)} categories")

# Education
edu_data = df_filtered[df_filtered['D4'].notna()]
with col4:
    st.metric("🎓 Education Data", f"{len(edu_data):,} responses")

# ══════════════════════════════════════════════════════════════════
# GENDER DISTRIBUTION BY COUNTRY (NEW FULL-WIDTH CHART)
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">👫 Gender Distribution by Country</div>', unsafe_allow_html=True)

gender_by_country = []
for country in sorted(df_filtered['Country'].dropna().unique()):
    cdf = df_filtered[df_filtered['Country'] == country]
    total = cdf['WGT'].sum()
    male = cdf[cdf['D1'] == 'Male']['WGT'].sum()
    female = cdf[cdf['D1'] == 'Female']['WGT'].sum()
    
    gender_by_country.append({
        'Country': country,
        'Male %': (male / total * 100) if total > 0 else 0,
        'Female %': (female / total * 100) if total > 0 else 0
    })

gender_country_df = pd.DataFrame(gender_by_country)

fig = go.Figure()
fig.add_trace(go.Bar(
    name='Male',
    y=gender_country_df['Country'],
    x=gender_country_df['Male %'],
    orientation='h',
    marker_color='#6366f1',
    text=[f"{v:.1f}%" for v in gender_country_df['Male %']],
    textposition='inside',
    textfont=dict(color='white', size=11)
))
fig.add_trace(go.Bar(
    name='Female',
    y=gender_country_df['Country'],
    x=gender_country_df['Female %'],
    orientation='h',
    marker_color='#ec4899',
    text=[f"{v:.1f}%" for v in gender_country_df['Female %']],
    textposition='inside',
    textfont=dict(color='white', size=11)
))

fig.update_layout(
    barmode='stack',
    title="Gender Distribution by Country",
    xaxis_title="Percentage (%)",
    yaxis_title="",
    height=600,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# DETAILED DEMOGRAPHIC TABS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Detailed Demographic Breakdown</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# DETAILED TABS
# ══════════════════════════════════════════════════════════════════

tabs = st.tabs(["👫 Gender", "📅 Age", "💰 Income", "🎓 Education", "💼 Employment", "⛪ Religion"])

# TAB 1: GENDER
with tabs[0]:
    st.markdown("### Gender Distribution")
    
    # Overall
    gender_data = []
    for gender_label in ['Male', 'Female']:
        count = df_filtered[df_filtered['D1'] == gender_label]['WGT'].sum()
        pct = (count / df_filtered['WGT'].sum() * 100)
        gender_data.append({'Gender': gender_label, 'Percentage': pct, 'Count': count})
    
    gender_df = pd.DataFrame(gender_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=gender_df['Gender'],
            values=gender_df['Count'],
            marker=dict(colors=['#6366f1', '#ec4899', '#8b5cf6']),
            hole=0.4
        )])
        fig.update_layout(title="Overall Gender Distribution", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # By country
        country_gender = []
        for country in sorted(df_filtered['Country'].dropna().unique()):
            cdf = df_filtered[df_filtered['Country'] == country]
            total = cdf['WGT'].sum()
            male = cdf[cdf['D1'] == 'Male']['WGT'].sum()
            country_gender.append({
                'Country': country,
                'Male %': (male / total * 100) if total > 0 else 0,
                'Female %': ((total - male) / total * 100) if total > 0 else 0
            })
        
        cg_df = pd.DataFrame(country_gender)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Male', y=cg_df['Country'], x=cg_df['Male %'], orientation='h', marker_color='#6366f1'))
        fig.add_trace(go.Bar(name='Female', y=cg_df['Country'], x=cg_df['Female %'], orientation='h', marker_color='#ec4899'))
        fig.update_layout(barmode='stack', title="Gender Distribution by Country", height=400, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: AGE
with tabs[1]:
    st.markdown("### Age Distribution")
    
    age_labels_ordered = ['18 – 24', '25 – 34', '35 – 44', '45 – 54', '55 – 64', '65+']
    
    age_data = []
    for age_val in age_labels_ordered:
        count = df_filtered[df_filtered['D2B'] == age_val]['WGT'].sum()
        pct = (count / df_filtered['WGT'].sum() * 100)
        age_data.append({'Age Group': age_val, 'Percentage': pct})
    
    age_df = pd.DataFrame(age_data)
    
    fig = go.Figure(go.Bar(
        x=age_df['Age Group'],
        y=age_df['Percentage'],
        marker_color='#6366f1',
        text=[f"{v:.1f}%" for v in age_df['Percentage']],
        textposition='outside'
    ))
    fig.update_layout(title="Age Group Distribution", yaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: INCOME
with tabs[2]:
    st.markdown("### Income Distribution")
    
    income_labels = {
        'Low  (Bottom quintile/20%)': 'Low (Bottom 20%)',
        'Medium low (Second quintile/20%)': 'Medium Low (2nd 20%)',
        'Medium (Third quintile/20%)': 'Medium (3rd 20%)',
        'Medium high (Fourth quintile/20%)': 'Medium High (4th 20%)',
        'High (Top quintile/20%)': 'High (Top 20%)'
    }
    income_valid = list(income_labels.keys())
    
    income_data = []
    for d3_val, display_label in income_labels.items():
        count = df_filtered[df_filtered['D3'] == d3_val]['WGT'].sum()
        total = df_filtered[df_filtered['D3'].isin(income_valid)]['WGT'].sum()
        pct = (count / total * 100) if total > 0 else 0
        income_data.append({'Income Level': display_label, 'Percentage': pct})
    
    income_df = pd.DataFrame(income_data)
    
    fig = go.Figure(go.Bar(
        x=income_df['Income Level'],
        y=income_df['Percentage'],
        marker=dict(
            color=income_df['Percentage'],
            colorscale='Greens',
            showscale=True
        ),
        text=[f"{v:.1f}%" for v in income_df['Percentage']],
        textposition='outside'
    ))
    fig.update_layout(title="Income Quintile Distribution", yaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: EDUCATION
with tabs[3]:
    st.markdown("### Education Level Distribution")
    
    edu_labels = {
        'No education/only basic education': 'No/Basic Education',
        'Completed primary': 'Completed Primary',
        'Completed secondary school': 'Completed Secondary',
        'Completed High level education (University)': 'University Degree',
        'Completed Higher level of education (Masters, PHD, etc.)': 'Masters/PhD',
        'Vocational Education': 'Vocational Education'
    }
    edu_valid = list(edu_labels.keys())
    
    edu_data = []
    for d4_val, display_label in edu_labels.items():
        count = df_filtered[df_filtered['D4'] == d4_val]['WGT'].sum()
        total = df_filtered[df_filtered['D4'].isin(edu_valid)]['WGT'].sum()
        pct = (count / total * 100) if total > 0 else 0
        edu_data.append({'Education': display_label, 'Percentage': pct})
    
    edu_df = pd.DataFrame(edu_data)
    
    fig = go.Figure(go.Bar(
        y=edu_df['Education'],
        x=edu_df['Percentage'],
        orientation='h',
        marker_color='#6366f1',
        text=[f"{v:.1f}%" for v in edu_df['Percentage']],
        textposition='outside'
    ))
    fig.update_layout(title="Education Level Distribution", xaxis_title="Percentage (%)", height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# TAB 5: EMPLOYMENT
with tabs[4]:
    st.markdown("### Employment Status")
    
    emp_labels = {
        'Working full (include self-employed)': 'Working Full-Time',
        'Working Part-time': 'Working Part-Time',
        'Unemployed': 'Unemployed',
        'Student': 'Student',
        'Housewife': 'Housewife',
        'Retired/Disabled': 'Retired/Disabled',
        'Refused/DNK/DNA': 'Others'
    }
    emp_valid = [k for k in emp_labels.keys() if k != 'Refused/DNK/DNA']
    
    emp_data = []
    for d5_val, display_label in emp_labels.items():
        if d5_val == 'Refused/DNK/DNA':
            continue
        count = df_filtered[df_filtered['D5'] == d5_val]['WGT'].sum()
        total = df_filtered[df_filtered['D5'].isin(emp_valid)]['WGT'].sum()
        pct = (count / total * 100) if total > 0 else 0
        emp_data.append({'Employment': display_label, 'Percentage': pct})
    
    emp_df = pd.DataFrame(emp_data)
    
    fig = go.Figure(data=[go.Pie(
        labels=emp_df['Employment'],
        values=emp_df['Percentage'],
        hole=0.4
    )])
    fig.update_layout(title="Employment Status Distribution", height=500)
    st.plotly_chart(fig, use_container_width=True)

# TAB 6: RELIGION
with tabs[5]:
    st.markdown("### Religious Affiliation")
    
    religion_labels = {
        'Roman Catholic': 'Roman Catholic',
        'Russian or Eastern Orthodox': 'Orthodox',
        'Protestant': 'Protestant',
        'Other Christian': 'Other Christian',
        'Hindu': 'Hindu',
        'Muslim': 'Muslim',
        'Jewish': 'Jewish',
        'Buddhist': 'Buddhist',
        'Other': 'Other',
        'Atheist/agnostic': 'Atheist/Agnostic'
    }
    
    rel_data = []
    for d6_val, display_label in religion_labels.items():
        count = df_filtered[df_filtered['D6'] == d6_val]['WGT'].sum()
        total = df_filtered[df_filtered['D6'].isin(list(religion_labels.keys()))]['WGT'].sum()
        pct = (count / total * 100) if total > 0 else 0
        if pct > 0.5:  # Only show if >0.5%
            rel_data.append({'Religion': display_label, 'Percentage': pct})
    
    rel_df = pd.DataFrame(rel_data).sort_values('Percentage', ascending=False)
    
    fig = go.Figure(go.Bar(
        y=rel_df['Religion'],
        x=rel_df['Percentage'],
        orientation='h',
        marker_color='#6366f1',
        text=[f"{v:.1f}%" for v in rel_df['Percentage']],
        textposition='outside'
    ))
    fig.update_layout(title="Religious Affiliation Distribution", xaxis_title="Percentage (%)", height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# CROSSTABS
# ══════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔗 Demographic Cross-Tabulations</div>', unsafe_allow_html=True)

st.markdown("#### Gender × Age Distribution")

# Calculate total for percentages
total_wgt = df_filtered['WGT'].sum()

cross_data = []
age_labels_list = ['18 – 24', '25 – 34', '35 – 44', '45 – 54', '55 – 64', '65+']
for gender in ['Male', 'Female']:
    for age in age_labels_list:
        count = df_filtered[(df_filtered['D1'] == gender) & (df_filtered['D2B'] == age)]['WGT'].sum()
        pct = (count / total_wgt * 100) if total_wgt > 0 else 0
        cross_data.append({
            'Gender': gender,
            'Age': age,
            'Percentage': pct
        })

cross_df = pd.DataFrame(cross_data)
cross_pivot = cross_df.pivot(index='Age', columns='Gender', values='Percentage')

fig = go.Figure(data=go.Heatmap(
    z=cross_pivot.values,
    x=cross_pivot.columns,
    y=cross_pivot.index,
    colorscale='Blues',
    text=cross_pivot.values,
    texttemplate='%{text:.1f}%',
    colorbar=dict(title="Percentage (%)")
))
fig.update_layout(title="Gender × Age Heatmap", height=400)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,#3730a3 0%,#4338ca 100%);border-radius:16px;color:white;margin-top:3rem;">
    <p style="font-size:1.25rem;font-weight:800;margin:0;">GALLUP PAKISTAN</p>
    <p style="opacity:0.85;margin:0.6rem 0 0;">Iran War Poll 2026 · Demographics Deep Dive</p>
    <p style="opacity:0.6;margin:0.5rem 0 0;font-size:0.82rem;">© 2026 Gallup Pakistan</p>
</div>
""", unsafe_allow_html=True)
