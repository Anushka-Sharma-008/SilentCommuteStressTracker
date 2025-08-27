import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Silent Commute Stress Tracker", layout="wide")
st.title("Commute Stress Tracker")

@st.cache_data
def load_data():
    df = pd.read_csv("data/with_stress.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")
city = st.sidebar.selectbox("City", sorted(df['city'].unique()))
routes = sorted(df[df['city']==city]['route'].unique())
route = st.sidebar.selectbox("Route", routes)
start_date = st.sidebar.date_input("Start date", df['date'].min().date())
end_date = st.sidebar.date_input("End date", df['date'].max().date())

mask = (df['city']==city) & (df['route']==route) & (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
subset = df[mask].sort_values('date')

# KPI
if not subset.empty:
    today = subset.iloc[-1]
    st.metric(label="Latest Stress Index (0-100)", value=f"{today['stress_pct']}")
else:
    st.write("No data for this selection.")

# Line chart
if not subset.empty:
    fig = px.line(subset, x='date', y='stress_pct', title=f"Stress trend — {city} {route}", labels={'stress_pct':'Stress (0-100)'})
    st.plotly_chart(fig, use_container_width=True)

# Comparison across routes (bar)
avg_by_route = df[(df['city']==city) & (df['date'].dt.date.between(start_date, end_date))].groupby('route')['stress_pct'].mean().reset_index()
st.subheader(f"Average stress across routes in {city}")
fig2 = px.bar(avg_by_route, x='route', y='stress_pct', labels={'stress_pct':'Avg Stress (0-100)'})
st.plotly_chart(fig2, use_container_width=True)

# Insights (auto text)
if not subset.empty:
    mean_recent = subset['stress_pct'].mean()
    mean_prev = df[(df['city']==city) & (df['route']==route) & (df['date'] < subset['date'].min())]['stress_pct'].mean()
    if pd.notna(mean_prev):
        diff = mean_recent - mean_prev
        st.write(f"Insight: The selected period's mean stress is {mean_recent:.1f}. That's {diff:+.1f} points compared with the earlier period.")
    else:
        st.write("No earlier data for comparison.")