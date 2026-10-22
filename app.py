
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Usage Dashboard", layout="wide")
df = pd.read_csv("clean_data.csv")

st.title("AI Usage and Impact on Students and Professionals")

# ---- Filters ----
st.sidebar.header("Filters")
user_types = sorted(df["User_Type"].unique())
sel_types = st.sidebar.multiselect("User type", user_types, default=user_types)
tools = sorted(df["AI_Tool"].unique())
sel_tools = st.sidebar.multiselect("AI tool", tools, default=tools)

f = df[df["User_Type"].isin(sel_types) & df["AI_Tool"].isin(sel_tools)]

# ---- Key numbers ----
c1, c2, c3 = st.columns(3)
c1.metric("Users", f"{len(f):,}")
if len(f):
    c2.metric("Avg productivity score", f"{f['Productivity_Score'].mean():.2f}")
    c3.metric("Avg time saved / week (hrs)", f"{f['Time_Saved_Hours_Per_Week'].mean():.1f}")
else:
    st.warning("No rows match these filters.")
    st.stop()

# ---- Charts ----
left, right = st.columns(2)

avg = f.groupby("AI_Tool", as_index=False)["Productivity_Score"].mean().sort_values("Productivity_Score")
left.plotly_chart(px.bar(avg, x="Productivity_Score", y="AI_Tool", orientation="h",
                         title="Average productivity score by AI tool"), use_container_width=True)

right.plotly_chart(px.box(f, x="User_Type", y="Productivity_Score", color="User_Type",
                          title="Productivity score by user type"), use_container_width=True)

st.plotly_chart(px.scatter(f, x="Time_Saved_Hours_Per_Week", y="Productivity_Score",
                           color="User_Type", trendline="ols",
                           title="Productivity vs time saved per week"), use_container_width=True)

# ---- Bonus: download ----
st.download_button("Download clean data", f.to_csv(index=False), "clean_data.csv", "text/csv")
