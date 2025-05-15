import streamlit as st
import pandas as pd

# Load the CSV file with O*NET data
@st.cache_data
def load_occupation_data(file_path, occupation_code):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Ensure the column exists and filter based on the occupation code
        if 'O*NET-SOC Code' not in df.columns:
            st.error("The 'O*NET-SOC Code' column is missing in the CSV file.")
            return None
        
        # Filter the data for the specific occupation code
        occupation_data = df[df['O*NET-SOC Code'] == occupation_code]
        
        # Return the occupation data if found
        if not occupation_data.empty:
            return occupation_data
        else:
            st.error(f"No data found for occupation code {occupation_code}")
            return None
        
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

# Streamlit app UI
st.sidebar.header("Search for an Occupation")
occupation_code = st.sidebar.text_input("Enter the O*NET-SOC Code", "11-1011.00")  # Default code for testing

# CSV file path (use the raw URL from GitHub)
file_path = "https://raw.githubusercontent.com/reen967/onet_data/main/occupation_data.csv"

if occupation_code:
    # Load and display the occupation data based on the occupation code
    occupation_data = load_occupation_data(file_path, occupation_code)
    
    if occupation_data is not None:
        # Display the occupation data if found
        st.title(occupation_data.iloc[0]["Title"])  # Display the Title of the occupation
        st.write(f"**Description**: {occupation_data.iloc[0]['Description']}")  # Display the Description
    else:
        st.write("No data available.")
