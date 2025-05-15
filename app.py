import os
import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# O*NET API key stored in the .env file
api_key = os.getenv("ONET_API_KEY")

# Debugging: Check if API key is loaded correctly
if not api_key:
    st.error("API Key is missing or not loaded.")
    print("Error: API Key not found in .env or environment.")
else:
    st.success("API Key loaded successfully.")
    print(f"Loaded API Key: {api_key}")

# Base URL for the O*NET API
base_url = "https://services.onetcenter.org/ws/online/occupations/"

# Function to fetch occupation data using the O*NET API
def fetch_occupation_data(occupation_code):
    url = f"{base_url}{occupation_code}/overview"
    headers = {
        "Authorization": f"Basic {api_key}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

# Function to display occupation data
def display_occupation_data(occupation_data):
    if occupation_data:
        st.title(occupation_data["title"])
        st.write(f"**Description**: {occupation_data['description']}")
        st.write("**Sample Job Titles**:")
        for job in occupation_data.get("sample_of_reported_job_titles", {}).get("title", []):
            st.write(f"- {job}")
        
        st.write("**Related Occupations**:")
        for related in occupation_data.get("also_see", {}).get("occupation", []):
            st.write(f"- {related['title']} (Code: {related['code']})")
    else:
        st.write("No data available.")

# Function to load occupation codes from CSV
@st.cache_data
def load_occupation_codes():
    try:
        # Ensure you use the correct URL to the raw CSV file from GitHub
        url = "https://raw.githubusercontent.com/reen967/onet_data/main/occupation_data.csv"
        df = pd.read_csv(url)
        
        # Debugging: Check what the data looks like
        print(f"Loaded occupation data: {df.head()}")
        
        # Ensure "O*NET-SOC Code" is the correct column name
        if "O*NET-SOC Code" not in df.columns:
            st.error("O*NET-SOC Code column not found in the CSV.")
            return []
        
        return df['O*NET-SOC Code'].dropna().unique()  # Extract unique O*NET-SOC Codes
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return []

# Streamlit app UI
st.sidebar.header("Search for an Occupation")
occupation_codes = load_occupation_codes()

# Debugging: Check if occupation_codes is being loaded correctly
if not occupation_codes:
    st.error("No occupation codes found.")
    print("Error: No occupation codes found.")
else:
    print(f"Loaded occupation codes: {occupation_codes}")

occupation_code = st.sidebar.selectbox("Select an Occupation Code", occupation_codes)

if occupation_code:
    occupation_data = fetch_occupation_data(occupation_code)
    display_occupation_data(occupation_data)
