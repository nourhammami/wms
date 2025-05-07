from datetime import datetime, timedelta

def parse_user_query(query):
    query = query.lower()
    today = datetime.today()
    filters = {}

    if "last 30 days" in query:
        filters['date_range'] = (today - timedelta(days=30), today)
    elif "this month" in query:
        filters['date_range'] = (today.replace(day=1), today)
    elif "last 7 days" in query:
        filters['date_range'] = (today - timedelta(days=7), today)

    return filters