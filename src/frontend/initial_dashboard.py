import streamlit as st
import requests
import pandas as pd 
import plotly.express as px 


API_URL = ####

st.set_page_config(page_title="Global Education Dashboard", layout="wide")
st.title("🌍 Global Education Analysis")
st.subheader("Initial Dashboard")

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
   
    #sidebar filters
    st.sidebar.header("Filters")
    all_countries = df['Countries and Areas'].unique()
    selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries)

    if selected_countriescountries:
        df = df[df['Countries and Areas'].isin(selected_countriescountries)]

    #displaying data table   
    st.subheader("Dataset Overview")
    st.dataframe(df, use_container_width=True)

    #interactive chart
    st.subheader("Literacy Rates by Country")
    #using 'Youth_15_24_Literacy_Rate_Male' from the dataset
    fig = px.bar(df, 
                x='Countries and Areas', 
                y='Youth_15_24_Literacy_Rate_Male', 
                title="Male Youth Literacy Rate",
                color='Youth_15_24_Literacy_Rate_Male')
    st.plotly_chart(fig, use_container_width=True)

except requests.RequestException as e:
    st.error("Failed to connect to the server/API.")



