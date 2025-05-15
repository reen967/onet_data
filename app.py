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

# Function to load occupation codes from CSV
@st.cache_data
def load_occupation_codes():
    try:
        # Correct URL to the raw CSV file in GitHub
        url = "https://raw.githubusercontent.com/reen967/onet_data/main/occupation_data.csv"  # Correct URL
        df = pd.read_csv(url)
        
        # Debugging: Check the first few rows of the data
        print(f"Loaded occupation data: {df.head()}")
        
        # Ensure "O*NET-SOC Code" is the correct column name
        if "O*NET-SOC Code" not in df.columns:
            st.error("O*NET-SOC Code column not found in the CSV.")
            return []
        
        # Return unique O*NET-SOC Codes
        occupation_codes = df['O*NET-SOC Code'].dropna().unique()
        if len(occupation_codes) == 0:
            st.error("No occupation codes found in the CSV.")
            return []
        
        return occupation_codes
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return []

# Load occupation codes
occupation_codes = load_occupation_codes()

# Check if occupation codes are loaded properly
if not occupation_codes:
    st.error("No occupation codes found.")
else:
    # Proceed with your app logic
    st.write(f"Found {len(occupation_codes)} occupation codes.")
    st.write("Example codes:", occupation_codes[:5])  # Display first 5 codes as a sample

    # Your Streamlit app logic to handle occupation code input and display data
    # (Example: display a dropdown with occupation codes)
    occupation_code = st.selectbox("Select an occupation code", occupation_codes)
    
    if occupation_code:
        # Your existing code to fetch and display occupation data based on the selected occupation code
        pass
