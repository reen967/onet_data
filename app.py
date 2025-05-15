import streamlit as st
import pandas as pd

# Load all CSV files into pandas DataFrames
@st.cache
def load_data():
    # Load all CSV files into pandas DataFrames
    occupation_data = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/occupation_data.csv")
    abilities = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/abilities.csv")
    skills = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/skills.csv")
    task_statements = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/task_statements.csv")
    tools_used = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/tools_used.csv")
    work_activities = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/work_activities.csv")
    
    # Return as a dictionary
    return {
        "occupation_data": occupation_data,
        "abilities": abilities,
        "skills": skills,
        "task_statements": task_statements,
        "tools_used": tools_used,
        "work_activities": work_activities
    }

# Filter data based on minimum Data Value for each table
def get_filtered_data(data, min_values):
    # Apply Data Value filters for each table
    abilities = data['abilities'][data['abilities']['Data Value'] >= min_values['abilities']]
    skills = data['skills'][data['skills']['Data Value'] >= min_values['skills']]
    tasks = data['task_statements'][data['task_statements']['Data Value'] >= min_values['tasks']]
    work_activities = data['work_activities'][data['work_activities']['Data Value'] >= min_values['work_activities']]
    tools_used = data['tools_used'][data['tools_used']['Data Value'] >= min_values['tools']]
    
    return {
        "abilities": abilities,
        "skills": skills,
        "tasks": tasks,
        "work_activities": work_activities,
        "tools_used": tools_used
    }

# Streamlit app UI
st.sidebar.header("Filter Data by Categories and Scales")

# Add sliders for Data Value categories (Importance, Level, etc.) and set default minimum values
min_abilities_value = st.sidebar.slider("Minimum Data Value for Abilities", 0.0, 5.0, 0.0, 0.1)
min_skills_value = st.sidebar.slider("Minimum Data Value for Skills", 0.0, 5.0, 0.0, 0.1)
min_tasks_value = st.sidebar.slider("Minimum Data Value for Tasks", 0.0, 5.0, 0.0, 0.1)
min_work_activities_value = st.sidebar.slider("Minimum Data Value for Work Activities", 0.0, 5.0, 0.0, 0.1)
min_tools_value = st.sidebar.slider("Minimum Data Value for Tools", 0.0, 5.0, 0.0, 0.1)

# Load all data
data = load_data()

# Apply the filtering based on sliders (Data Value filters)
min_values = {
    'abilities': min_abilities_value,
    'skills': min_skills_value,
    'tasks': min_tasks_value,
    'work_activities': min_work_activities_value,
    'tools': min_tools_value
}
filtered_data = get_filtered_data(data, min_values)

# Display the filtered results
st.title("Filtered Occupation Data")
st.write("The results below show data for Abilities, Skills, Tasks, Tools, and Work Activities filtered based on the selected minimum Data Values.")

# Display filtered abilities
st.subheader("Abilities")
st.write(filtered_data['abilities'])

# Display filtered skills
st.subheader("Skills")
st.write(filtered_data['skills'])

# Display filtered tasks
st.subheader("Tasks")
st.write(filtered_data['tasks'])

# Display filtered work activities
st.subheader("Work Activities")
st.write(filtered_data['work_activities'])

# Display filtered tools used
st.subheader("Tools Used")
st.write(filtered_data['tools_used'])

