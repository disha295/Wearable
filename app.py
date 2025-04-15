import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.components.v1.html(
        """
        <iframe src="<div class='tableauPlaceholder' id='viz1744658623037' style='position: relative'><noscript><a href='#'><img alt='Cardiovascular Health Dashboard ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Cardinovascularhealthdashboard&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Cardinovascularhealthdashboard&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Cardinovascularhealthdashboard&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1744658623037');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='2127px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
                width="100%" height="827" frameborder="0" allowfullscreen></iframe>
        """, height=850
    )

with tabs[1]:
    st.markdown("### 🛌 Sleep, Activity & Lifestyle Dashboard")
    st.components.v1.html(
        """
        <iframe src="https://public.tableau.com/views/SleepActivityandLifestyleDashboard/Dashboard1?:embed=y&:display_count=yes&publish=yes"
                width="100%" height="827" frameborder="0" allowfullscreen></iframe>
        """, height=850
    )

with tabs[2]:
    st.markdown("### 📊 Multi-Metric Anomaly Detection System")
    st.components.v1.html(
        """
        <iframe src="https://public.tableau.com/views/Multi-metricanomalydetectionsystem/Dashboard1?:embed=y&:display_count=yes&publish=yes"
                width="100%" height="827" frameborder="0" allowfullscreen></iframe>
        """, height=850
    )
