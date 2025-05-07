import streamlit as st
import pandas as pd
import altair as alt
import os
import sys
import requests
from query_parser import parse_user_query
# === Configuration ===
BASEROW_API_TOKEN = "1x6UPMjWrCvU5wb2fljfsN4JnME1d6TZ"
BASEROW_API_URL = "https://api.baserow.io/api/database/rows/table/529099/"  # Your Baserow API URL

# Add ../part1 to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../part1')))
from wms_mapper import SKUMapper
from export_baserow import export_baserow

# === Page Setup ===
st.set_page_config(page_title="WMS - Sales Data Processor", layout="wide")
st.title("📦 WMS - Sales Data Processor")

# === Test Baserow API ===
st.markdown("### 🧪 Test Baserow Database Connection")
if st.button("Test Connection to Baserow"):
    try:
        headers = {"Authorization": f"Token {BASEROW_API_TOKEN}"}
        response = requests.get(BASEROW_API_URL, headers=headers)
        if response.status_code == 200:
            st.success("✅ Successfully connected to Baserow!")
        else:
            st.error(f"❌ Connection failed. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# === Upload Files ===
st.markdown("### Step 1: Upload Required Files")
mapping_file = st.file_uploader("🗂️ Upload WMS Mapping File (`file1.xlsx`)", type="xlsx", key="mapping")
sales_file = st.file_uploader("🛒 Upload Sales Data File (`file2.xlsx`)", type="xlsx", key="sales")

if not mapping_file or not sales_file:
    st.info("👆 Please upload both files to proceed.")
    st.stop()

# === Processing ===
try:
    # Initialize the SKU Mapper and process the sales file
    mapper = SKUMapper(mapping_file)
    df = mapper.process_file(sales_file)

    st.success("✅ File processed successfully!")
    st.subheader("📊 Mapped Data Preview")
    st.dataframe(df)

    # === MSKU Sales Count Chart ===
    if "MSKU" in df.columns:
        st.subheader("📈 Sales Count per MSKU")
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('MSKU:N', sort='-y'),
            y='count():Q'
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

        # === Top 10 MSKUs Chart ===
        st.subheader("🏆 Top Selling MSKUs")
        top_mskus = df['MSKU'].value_counts().head(10).reset_index()
        top_mskus.columns = ['MSKU', 'Sales']
        chart = alt.Chart(top_mskus).mark_bar().encode(
            x='MSKU:N',
            y='Sales:Q'
        )
        st.altair_chart(chart, use_container_width=True)

    # === Time Series Chart ===
    if "Date" in df.columns:
        st.subheader("📈 Sales Over Time")
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        time_df = df.dropna(subset=["Date"]).groupby('Date').size().reset_index(name='Sales')
        chart = alt.Chart(time_df).mark_line().encode(
            x='Date:T',
            y='Sales:Q'
        )
        st.altair_chart(chart, use_container_width=True)

    # === Export to Baserow ===
    if st.button("📤 Export to Baserow"):
        try:
            s_skus, e_skus, s_sales, e_sales = export_baserow(df)
            st.success(
                f"✅ Export complete: {s_skus} SKU rows uploaded, {e_skus} SKU errors, "
                f"{s_sales} Sales rows uploaded, {e_sales} Sales errors."
            )
        except Exception as e:
            st.error(f"❌ Export failed: {e}")

    # === Download CSV ===
    st.subheader("📥 Download Processed Data")
    csv_file = "processed_sales.csv"
    df.to_csv(csv_file, index=False)
    with open(csv_file, "rb") as f:
        st.download_button("Download Processed CSV", f, file_name=csv_file)

except Exception as e:
    st.error(f"❌ An error occurred during processing: {e}")

# === Display Baserow Table Content ===
st.subheader("📄 Baserow Table Content")
def fetch_baserow_data():
    headers = {"Authorization": f"Token {BASEROW_API_TOKEN}"}
    try:
        response = requests.get(BASEROW_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            st.error(f"❌ Failed to fetch data: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ Fetch error: {e}")
        return []

# Fetch data from Baserow and show as a dataframe
baserow_data = fetch_baserow_data()
if baserow_data:
    st.dataframe(pd.DataFrame(baserow_data))

# Replace the CSV load with data from Baserow
data = pd.DataFrame(baserow_data)

# Title
st.title("AI over Data Layer Dashboard")

st.markdown("## 🤖 AI Query Over Data Layer")

user_query = st.text_input("Ask something like: 'Show sales for April', 'Add profit column', 'Plot sales by SKU'", "")

if user_query:
    from services.query_processor import process_query
    from utils.calculated_fields import add_calculated_fields
    from visualizations.charts import generate_chart

    try:
        # 1. Handle calculated fields
        df_updated = add_calculated_fields(df, user_query)

        # 2. Apply filter/query logic
        filtered_df = process_query(df_updated, user_query)

        st.success("✅ Query processed!")
        st.write("### 🔍 Filtered Data")
        st.dataframe(filtered_df)

        # 3. Generate charts if the query suggests it
        chart = generate_chart(filtered_df, user_query)
        if chart:
            st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Failed to process query: {e}")

# Group by order and count how many IDs are linked to each
order_counts = data.groupby('order')['id'].count().reset_index()
order_counts.rename(columns={'id': 'Item Count'}, inplace=True)

st.subheader("📦 Number of Items per Order")
chart = alt.Chart(order_counts).mark_bar().encode(
    x='order:N',
    y='Item Count:Q'
).properties(height=400)
st.altair_chart(chart, use_container_width=True)