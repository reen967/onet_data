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

# Load occupation data and linked data with filtering
def get_linked_data(occupation_code, data, min_values):
    occupation = data['occupation_data'][data['occupation_data']['O*NET-SOC Code'] == occupation_code]
    
    if occupation.empty:
        st.error(f"No data found for occupation code: {occupation_code}")
        return None
    
    # Linking data with O*NET-SOC Code
    abilities = pd.merge(occupation, data['abilities'], on='O*NET-SOC Code', how='inner')
    skills = pd.merge(occupation, data['skills'], on='O*NET-SOC Code', how='inner')
    tasks = pd.merge(occupation, data['task_statements'], on='O*NET-SOC Code', how='inner')
    tools = pd.merge(occupation, data['tools_used'], on='O*NET-SOC Code', how='inner')
    work_activities = pd.merge(occupation, data['work_activities'], on='O*NET-SOC Code', how='inner')

    # Apply Data Value filters for each table
    if min_values['abilities'] > 0:
        abilities = abilities[abilities['Data Value'] >= min_values['abilities']]
    if min_values['skills'] > 0:
        skills = skills[skills['Data Value'] >= min_values['skills']]
    if min_values['tasks'] > 0:
        tasks = tasks[tasks['Data Value'] >= min_values['tasks']]
    if min_values['work_activities'] > 0:
        work_activities = work_activities[work_activities['Data Value'] >= min_values['work_activities']]
    if min_values['tools'] > 0:
        tools = tools[tools['Data Value'] >= min_values['tools']]

    return {
        "occupation": occupation,
        "abilities": abilities,
        "skills": skills,
        "tasks": tasks,
        "tools": tools,
        "work_activities": work_activities
    }

# Streamlit app UI
st.sidebar.header("Search for an Occupation")
occupation_code = st.sidebar.text_input("Enter the O*NET-SOC Code", "11-1011.00")  # Default code for testing

# Add minimum Data Value filters for each table in the sidebar
min_abilities = st.sidebar.slider("Minimum Data Value for Abilities", 0.0, 5.0, 0.0, 0.1)
min_skills = st.sidebar.slider("Minimum Data Value for Skills", 0.0, 5.0, 0.0, 0.1)
min_tasks = st.sidebar.slider("Minimum Data Value for Tasks", 0.0, 5.0, 0.0, 0.1)
min_work_activities = st.sidebar.slider("Minimum Data Value for Work Activities", 0.0, 5.0, 0.0, 0.1)
min_tools = st.sidebar.slider("Minimum Data Value for Tools", 0.0, 5.0, 0.0, 0.1)

# Load all data
data = load_data()

if occupation_code:
    # Get the linked data for the selected occupation code with the selected filters
    min_values = {
        'abilities': min_abilities,
        'skills': min_skills,
        'tasks': min_tasks,
        'work_activities': min_work_activities,
        'tools': min_tools
    }
    linked_data = get_linked_data(occupation_code, data, min_values)
    
    if linked_data:
        # Display occupation data
        st.title(linked_data['occupation'].iloc[0]["Title"])  # Display the Title of the occupation
        st.write(f"**Description**: {linked_data['occupation'].iloc[0]['Description']}")  # Display the Description
        
        # Display abilities related to the occupation
        st.subheader("Abilities")
        st.write(linked_data['abilities'])
        
        # Display skills related to the occupation
        st.subheader("Skills")
        st.write(linked_data['skills'])
        
        # Display tasks related to the occupation
        st.subheader("Tasks")
        st.write(linked_data['tasks'])
        
        # Display tools used related to the occupation
        st.subheader("Tools Used")
        st.write(linked_data['tools'])
        
        # Display work activities related to the occupation
        st.subheader("Work Activities")
        st.write(linked_data['work_activities'])
    
    else:
        st.write("No linked data available for this occupation.")

