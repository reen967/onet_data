import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# O*NET API key stored in the .env file (optional if you are no longer using API)
api_key = os.getenv("ONET_API_KEY")

# Check if the API key is loaded correctly (optional)
if not api_key:
    st.error("API Key is missing or not loaded.")
    print("Error: API Key not found in .env or environment.")
else:
    st.success("API Key loaded successfully.")
    print(f"Loaded API Key: {api_key}")

# Base URL for GitHub or Local CSV Files
data_files_url = "https://raw.githubusercontent.com/your-username/your-repo-name/main/"

# List of CSV files available on GitHub repo
data_files = [
    "abilities.csv",
    "abilities_descriptions.csv",
    "abilities_to_work_activities.csv",
    "abilities_to_work_context.csv",
    "alternate_titles.csv",
    "basic_interests_to_riasec.csv",
    "content_model_reference.csv",
    "frequency_of_task_categories.csv",
    "interests.csv",
    "interests_to_illustrative_activities.csv",
    "interests_to_illustrative_occupations.csv",
    "interests_to_riasec_keywords.csv",
    "knowledge.csv",
    "level_scale_anchors.csv",
    "occupation_data.csv",
    "related_occupations.csv",
    "scales_reference.csv",
    "skills.csv",
    "skills_to_work_activities.csv",
    "skills_to_work_context.csv",
    "task_statements.csv",
    "tasks_to_dwa.csv",
    "technology_skills.csv",
    "tools_used.csv",
    "unspsc_reference.csv",
    "work_activities.csv",
    "work_activities_to_iwa.csv",
    "work_activities_to_iwa_to_dwa.csv",
    "work_context_categories.csv"
]

# Function to load data from GitHub or local storage
def load_data(file_name):
    url = f"{data_files_url}{file_name}"
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Error loading {file_name}: {str(e)}")
        return None

# Streamlit app UI
st.sidebar.header("Search for an Occupation")
occupation_code = st.sidebar.text_input("Enter the O*NET-SOC Code", "17-2051.00")

if occupation_code:
    st.header(f"Data for {occupation_code}")

    # Load relevant occupation data (assuming you want to filter by occupation code)
    occupation_data = load_data("occupation_data.csv")
    if occupation_data is not None:
        filtered_data = occupation_data[occupation_data["O*NET-SOC Code"] == occupation_code]
        st.write(filtered_data)
    
    # Add further data extraction here if needed, such as related work activities, tasks, etc.
