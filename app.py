import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="🏅 Olympics Dashboard",
    page_icon="🏅",
    layout="wide",
)

# -------------------------------------------------
# Custom CSS for Attractive UI
# -------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    h1, h2, h3 {
        color: #facc15;
    }
    .stMetric {
        background-color: #ffffff;
        # background-color: #1e293b;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Title Section
# -------------------------------------------------
st.title("🏅 Olympics Athlete Events Dashboard")
st.caption("Interactive Data Analysis using Streamlit, Plotly & Pandas")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("athlete_events.csv")
    return df


data = load_data()

# -------------------------------------------------
# Data Cleaning
# -------------------------------------------------
data = data.drop_duplicates()

data["Age"].fillna(round(data["Age"].mean(), 1), inplace=True)
data["Height"].fillna(round(data["Height"].mean(), 1), inplace=True)
data["Weight"].fillna(round(data["Weight"].mean(), 1), inplace=True)
data["Medal"].fillna("No medal", inplace=True)

if "NOC" in data.columns:
    data.drop("NOC", axis=1, inplace=True)

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("🔎 Filters")

years = sorted(data["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", ["All"] + years)

sports = sorted(data["Sport"].unique())
selected_sport = st.sidebar.selectbox("Select Sport", ["All"] + sports)

# Apply filters
filtered_data = data.copy()

if selected_year != "All":
    filtered_data = filtered_data[filtered_data["Year"] == selected_year]

if selected_sport != "All":
    filtered_data = filtered_data[filtered_data["Sport"] == selected_sport]

# -------------------------------------------------
# Key Metrics
# -------------------------------------------------
st.subheader("📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Athletes", len(filtered_data))

with col2:
    st.metric("Total Sports", filtered_data["Sport"].nunique())

with col3:
    medals = filtered_data[filtered_data["Medal"] != "No medal"]
    st.metric("Total Medals", len(medals))

with col4:
    st.metric("Countries Participated", filtered_data["Team"].nunique())

st.markdown("---")

# -------------------------------------------------
# Year-wise Trends
# -------------------------------------------------
st.subheader("📅 Year-wise Trends")

year_sports = (
    data.groupby("Year")["Sport"].nunique().reset_index(name="No_of_Sports")
)

fig1 = px.line(
    year_sports,
    x="Year",
    y="No_of_Sports",
    markers=True,
    title="Number of Sports Over Years",
)

st.plotly_chart(fig1, use_container_width=True)


year_medals = (
    data[data["Medal"] != "No medal"]
    .groupby("Year")["Medal"]
    .count()
    .reset_index(name="Medal_Count")
)

fig2 = px.area(
    year_medals,
    x="Year",
    y="Medal_Count",
    title="Total Medals Won Over Years",
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# Top Sports & Countries
# -------------------------------------------------
st.subheader("🏆 Top Performing Sports & Countries")

col1, col2 = st.columns(2)

with col1:
    top_sports = (
        filtered_data[filtered_data["Medal"] != "No medal"]
        .groupby("Sport")["Medal"]
        .count()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="Medals")
    )

    fig3 = px.bar(
        top_sports,
        x="Medals",
        y="Sport",
        orientation="h",
        title="Top 10 Sports by Medals",
        text="Medals",
    )

    st.plotly_chart(fig3, use_container_width=True)

with col2:
    top_countries = (
        filtered_data[filtered_data["Medal"] != "No medal"]
        .groupby("Team")["Medal"]
        .count()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="Medals")
    )

    fig4 = px.bar(
        top_countries,
        x="Medals",
        y="Team",
        orientation="h",
        title="Top 10 Countries by Medals",
        text="Medals",
    )

    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# Athlete Demographics
# -------------------------------------------------
st.subheader("👤 Athlete Demographics")

col1, col2 = st.columns(2)

with col1:
    fig5 = px.histogram(
        filtered_data,
        x="Age",
        nbins=30,
        title="Age Distribution",
    )

    st.plotly_chart(fig5, use_container_width=True)

with col2:
    gender_count = (
        filtered_data["Sex"].value_counts().reset_index(name="Count")
    )
    gender_count.columns = ["Gender", "Count"]

    fig6 = px.pie(
        gender_count,
        names="Gender",
        values="Count",
        title="Gender Participation",
    )

    st.plotly_chart(fig6, use_container_width=True)


fig7 = px.scatter(
    filtered_data,
    x="Height",
    y="Weight",
    color="Sex",
    title="Height vs Weight",
    opacity=0.6,
)

st.plotly_chart(fig7, use_container_width=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("✨ Designed with Streamlit • Olympics Data Analysis Project")
