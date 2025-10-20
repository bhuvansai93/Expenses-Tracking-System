import streamlit as st
import requests
import pandas as pd


API_URL = "http://localhost:8000"

def analytics_by_month_tab():
    response = requests.get(f"{API_URL}/analytics_by_month")
    data = response.json()

    dict = {
        "Month": [item['month_name'] for item in data],
        "Total Amount": [item["total_amount"] for item in data]
    }

    df = pd.DataFrame(dict)

    st.header("Expense Breakdown by Month")
    st.bar_chart(data=df.set_index("Month")["Total Amount"])

    st.table(df)


