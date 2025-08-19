import streamlit as st
import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect("artifacts.db")

st.set_page_config(page_title="Harvard Artifacts Explorer", layout="wide")
st.title("🏛 Harvard Artifacts Explorer")
st.write("Explore thousands of artifacts from Harvard Art Museums")

st.sidebar.header("🔍 Exploration Mode")
mode = st.sidebar.radio("Choose mode", ["Filters", "Charts"])

conn = get_connection()

if mode == "Filters":
    st.sidebar.subheader("Filters")
    search_title = st.sidebar.text_input("Search by Title (keyword)")
    culture_filter = st.sidebar.text_input("Filter by Culture (e.g., 'Greek')")
    century_filter = st.sidebar.text_input("Filter by Century (e.g., '11th century')")

    query = "SELECT id, title, culture, century, classification, department FROM artifact_metadata WHERE 1=1"
    if search_title:
        query += f" AND title LIKE '%{search_title}%'"
    if culture_filter:
        query += f" AND culture LIKE '%{culture_filter}%'"
    if century_filter:
        query += f" AND century LIKE '%{century_filter}%'"
    query += " LIMIT 50"

    df = pd.read_sql_query(query, conn)
    st.subheader("📊 Filtered Results")
    st.write(f"Showing {len(df)} records")
    st.dataframe(df)

elif mode == "Charts":
    st.sidebar.subheader("Chart Options")
    chart_type = st.sidebar.selectbox("Choose a chart", [
        "Top 10 Cultures",
        "Artifacts per Century",
        "Artifacts per Department"
    ])

    if chart_type == "Top 10 Cultures":
        df = pd.read_sql_query("SELECT culture, COUNT(*) as total FROM artifact_metadata WHERE culture IS NOT NULL GROUP BY culture ORDER BY total DESC LIMIT 10", conn)
        st.subheader("🌍 Top 10 Cultures")
        st.bar_chart(df.set_index("culture"))

    elif chart_type == "Artifacts per Century":
        df = pd.read_sql_query("SELECT century, COUNT(*) as total FROM artifact_metadata WHERE century IS NOT NULL GROUP BY century ORDER BY century", conn)
        st.subheader("📜 Artifacts per Century")
        st.line_chart(df.set_index("century"))

    elif chart_type == "Artifacts per Department":
        df = pd.read_sql_query("SELECT department, COUNT(*) as total FROM artifact_metadata WHERE department IS NOT NULL GROUP BY department ORDER BY total DESC LIMIT 10", conn)
        st.subheader("🏛 Top Departments by Artifact Count")
        st.bar_chart(df.set_index("department"))

conn.close()
