# export_baserow.py
import requests

# Constants
BASEROW_API_TOKEN = "1x6UPMjWrCvU5wb2fljfsN4JnME1d6TZ"
BASEROW_TABLE_ID_SKU = "529099"  # SKU Table ID
BASEROW_TABLE_ID_SALES = "529100"  # Sales Data Table ID
BASEROW_API_URL_SKU = f"https://api.baserow.io/api/database/rows/table/{BASEROW_TABLE_ID_SKU}/"
BASEROW_API_URL_SALES = f"https://api.baserow.io/api/database/rows/table/{BASEROW_TABLE_ID_SALES}/"
HEADERS = {
    "Authorization": f"Token {BASEROW_API_TOKEN}",
    "Content-Type": "application/json"
}

def export_baserow(df):
    success_count_skus = 0
    error_count_skus = 0
    success_count_sales = 0
    error_count_sales = 0

    # Iterate over the rows of the DataFrame and export to both tables
    for _, row in df.iterrows():
        # Export SKU data
        sku_data = {
            "field_1": row.get("MSKU", ""),
            "field_2": row.get("SKU", ""),
            "field_3": row.get("Quantity", 0),
            "field_4": row.get("Marketplace", "")
        }
        response_sku = requests.post(BASEROW_API_URL_SKU, headers=HEADERS, json=sku_data)

        if response_sku.status_code == 200:
            success_count_skus += 1
        else:
            error_count_skus += 1
            print(f"Error posting SKU row: {response_sku.text}")

        # Export Sales data
        sales_data = {
            "field_1": row.get("Order ID", ""),
            "field_2": row.get("Quantity", 0),
            "field_3": row.get("Sale Date", ""),
            "field_4": row.get("Price", 0.0),
            "field_5": row.get("Product SKU", "")
        }
        response_sales = requests.post(BASEROW_API_URL_SALES, headers=HEADERS, json=sales_data)

        if response_sales.status_code == 200:
            success_count_sales += 1
        else:
            error_count_sales += 1
            print(f"Error posting Sales row: {response_sales.text}")

    return success_count_skus, error_count_skus, success_count_sales, error_count_sales
