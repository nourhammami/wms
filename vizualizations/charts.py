import altair as alt

def plot_sales_growth_chart(df):
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='Date:T',
        y='Sales:Q',
        tooltip=['Date:T', 'Sales:Q']
    ).properties(title="Sales Over Time")
    return chart
