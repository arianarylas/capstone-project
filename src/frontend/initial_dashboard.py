import streamlit as st
import requests
import pandas as pd 
import plotly.express as px 
import os

st.set_page_config(page_title="Global Education Dashboard", layout="wide")
st.title("Global Education Analysis")

#creates the dataset switcher w/ sidebar
st.sidebar.header("Data Settings")
dataset_options = {
    "Gender Gap (Enrollment)": "gender-gap",
    "Formal Education Levels": "formal-education",
    "Learning Adjusted Years": "learning-adjusted",
    "Out of School Statistics": "out-of-school"
}

selected_label = st.sidebar.selectbox("Choose a Dataset", options=list(dataset_options.keys()))
endpoint = dataset_options[selected_label]


BASE_URL = "https://education-api-329670330214.us-central1.run.app"
API_URL = f"{BASE_URL}/{endpoint}"

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    st.write(df.columns.tolist())
   
    #sidebar filters
    st.sidebar.header("Filters")
# Replace your current all_countries line with this 'Safety Net'
    if not df.empty and 'entity' in df.columns:
        all_countries = df['entity'].unique()
    else:
        st.warning("The Cloud Database is still waking up. Please wait 60 seconds and refresh.")
        st.stop() # This prevents the 'entity' error from happening
    if selected_countries:
        df = df[df['entity'].isin(selected_countries)]

    selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries)

    if selected_countries:
        df = df[df['entity'].isin(selected_countries)]

    #display data
    st.subheader(f"Dataset Overview: {selected_label}")
    st.dataframe(df, use_container_width=True)

    st.subheader("Visual Analysis")
    
    # We need to pick a Y-axis based on which dataset is selected
    #picking a Y-axis based on selected dataset
    if endpoint == "gender-gap":
        y_axis = "tertiary_female_enrollment"
        chart_title = "Female Tertiary Enrollment"
    elif endpoint == "formal-education":
        y_axis = "no_formal_education"
        chart_title = "Population with No Formal Education"
    elif endpoint == "learning-adjusted":
        y_axis = "learning_adjusted_years"
        chart_title = "Learning Adjusted Years of Schooling"
    else: # out-of-school
        y_axis = "out_of_school_females"
        chart_title = "Females Out of School"

    fig = px.bar(df, 
                x='entity', 
                y=y_axis, 
                title=chart_title,
                color=y_axis,
                labels={'entity': 'Country', y_axis: 'Value'})
    
    st.plotly_chart(fig, use_container_width=True)

except requests.RequestException:
    st.error(f"Failed to connect to the backend at {API_URL}. Is the server running?")