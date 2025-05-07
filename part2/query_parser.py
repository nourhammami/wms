# query_parser.py
import pandas as pd

def parse_user_query(query):
    filters = {}
    if 'last 30 days' in query:
        end_date = pd.to_datetime('today')
        start_date = end_date - pd.Timedelta(days=30)
        filters['date_range'] = (start_date, end_date)
    # More query parsing logic as needed
    return filters
