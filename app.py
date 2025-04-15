import streamlit as st
import pandas as pd
import plotly.express as px
import os

if not os.path.exists("weekly_nudges_llm.csv"):
    st.error("❌ File 'weekly_nudges_llm.csv' is missing in the app directory.")
    st.stop()

# Load your trend+nudge dataset
df = pd.read_csv("weekly_nudges_llm.csv", parse_dates=["week"])

# Melt for plotting
melted = df.melt(
    id_vars=["week", "TrendSummary", "LLM_Nudge"],
    value_vars=["RestingHeartRate", "HRV", "ExerciseTime", "Sleep", "Daylight", "HeadphoneAudio"],
    var_name="Metric", value_name="ZScore"
).dropna()

# Sidebar filters
metrics = st.multiselect("Select Metrics", melted["Metric"].unique(), default=melted["Metric"].unique())

# Filter data
filtered = melted[melted["Metric"].isin(metrics)]

# 📈 Line plot
fig = px.line(
    filtered, x="week", y="ZScore", color="Metric",
    hover_data=["TrendSummary", "LLM_Nudge"],
    title="Weekly Health Trends with Personalized Nudges"
)
st.plotly_chart(fig, use_container_width=True)

# 📋 Nudge Explorer
st.subheader("📬 Weekly Nudges")
selected_week = st.selectbox("Select Week", df["week"].dropna().dt.strftime("%Y-%m-%d"))
week_data = df[df["week"].dt.strftime("%Y-%m-%d") == selected_week]

for _, row in week_data.iterrows():
    if pd.notnull(row["LLM_Nudge"]):
        st.markdown(f"**Trend Summary**: {row['TrendSummary']}")
        st.info(row["LLM_Nudge"])

# 📊 Tableau Dashboards
st.subheader("📈 Tableau Storytelling Dashboards")

tabs = st.tabs(["❤️ Cardiovascular Health", "🛌 Sleep & Lifestyle", "📊 Anomaly Detection"])

with tabs[0]:
    st.markdown("### ❤️ Cardiovascular Health Dashboard")
    st.components.v1.iframe(
        "https://public.tableau.com/views/Cardinovascularhealthdashboard/Dashboard1?:language=en-US&publish=yes",
        height=850, width=1000
    )

with tabs[1]:
    st.markdown("### 🛌 Sleep, Activity & Lifestyle Dashboard")
    st.components.v1.iframe(
        "https://public.tableau.com/views/SleepActivityandLifestyleDashboard/Dashboard1?:embed=y&:display_count=yes&publish=yes",
        height=850, width=1000
    )

with tabs[2]:
    st.markdown("### 📊 Multi-Metric Anomaly Detection System")
    st.components.v1.iframe(
        "https://public.tableau.com/views/Multi-metricanomalydetectionsystem/Dashboard1?:embed=y&:display_count=yes&publish=yes",
        height=850, width=1000
    )
