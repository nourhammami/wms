import duckdb
import pandas as pd
import streamlit as st

st.title("🧠 AI Query Layer - Ask About Your Sales Data")

# Load CSV for querying
df = pd.read_csv("processed_sales.csv")
duckdb.sql("CREATE OR REPLACE TABLE sales AS SELECT * FROM df")

query = st.text_input("Ask a question (e.g., SELECT MSKU, COUNT(*) FROM sales GROUP BY MSKU)")

if query:
    try:
        result = duckdb.sql(query).df()
        st.dataframe(result)
        if 'MSKU' in result.columns:
            chart = alt.Chart(result).mark_bar().encode(
                x='MSKU:N',
                y=result.columns[1]
            )
            st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Query failed: {str(e)}")