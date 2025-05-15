import os
import streamlit as st
import pandas as pd

# Function to load occupation codes from CSV file
@st.cache_data
def load_occupation_codes(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        # Ensure the column exists and extract unique occupation codes
        if 'O*NET-SOC Code' not in df.columns:
            st.error("The 'O*NET-SOC Code' column is missing in the CSV file.")
            return []
        
        occupation_codes = df['O*NET-SOC Code'].dropna().unique()
        return occupation_codes
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return []

# Function to load occupation data from CSV based on occupation code
@st.cache_data
def load_occupation_data(file_path, occupation_code):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        # Filter the dataframe by occupation code
        occupation_data = df[df['O*NET-SOC Code'] == occupation_code]
        
        if occupation_data.empty:
            return None
        
        # Extract relevant data from the occupation row
        occupation_info = {
            "title": occupation_data.iloc[0]["Title"],
            "description": occupation_data.iloc[0]["Description"],
            "sample_of_reported_job_titles": occupation_data.iloc[0]["Sample of Reported Job Titles"],
            # You can add more fields as required
        }
        return occupation_info
    except Exception as e:
        st.error(f"Error loading occupation data: {e}")
        return None

# Function to display occupation data
def display_occupation_data(occupation_data):
    if occupation_data:
        st.title(occupation_data["title"])
        st.write(f"**Description**: {occupation_data['description']}")
        st.write("**Sample Job Titles**:")
        st.write(f"- {occupation_data['sample_of_reported_job_titles']}")
    else:
        st.write("No data available for this occupation.")

# Streamlit app UI
st.sidebar.header("Search for an Occupation")
file_path = st.sidebar.text_input("Enter the CSV file path", "https://raw.githubusercontent.com/reen967/onet_data/refs/heads/main/occupation_data.csv")

if file_path:
    occupation_codes = load_occupation_codes(file_path)
    if occupation_codes:
        occupation_code = st.sidebar.selectbox("Select an Occupation Code", occupation_codes)
        if occupation_code:
            st.write(f"Fetching data for: {occupation_code}")
            occupation_data = load_occupation_data(file_path, occupation_code)
            display_occupation_data(occupation_data)
    else:
        st.write("No occupation codes found in the CSV.")
