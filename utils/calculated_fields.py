def add_calculated_fields(df):
    if 'Sales' in df.columns and 'Cost' in df.columns:
        df['Profit'] = df['Sales'] - df['Cost']
    return df