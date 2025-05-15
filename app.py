import streamlit as st
import pandas as pd

# Load all CSV files into pandas DataFrames
@st.cache_data
def load_data():
    # Load all CSV files into pandas DataFrames
    occupation_data = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/occupation_data.csv")
    abilities = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/abilities.csv")
    skills = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/skills.csv")
    task_statements = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/task_statements.csv")
    tools_used = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/tools_used.csv")
    work_activities = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/work_activities.csv")
    work_context = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/work_context_categories.csv")
    scale_reference = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/scales_reference.csv")
    
    return {
        "occupation_data": occupation_data,
        "abilities": abilities,
        "skills": skills,
        "task_statements": task_statements,
        "tools_used": tools_used,
        "work_activities": work_activities,
        "work_context": work_context,
        "scale_reference": scale_reference
    }

# Merge data with scale reference for better context
def merge_with_scale_reference(data, scale_reference):
    # Merge the DataFrame with scale reference to clarify what the scale values mean
    data_with_scale = data.merge(scale_reference, how="left", left_on="Scale ID", right_on="Scale ID")
    return data_with_scale

# Streamlit app UI
st.sidebar.header("Filter Data by Categories and Scales")

# Add sliders for Data Value categories (Importance, Level, etc.) and set default minimum values
min_abilities_value = st.sidebar.slider("Minimum Data Value for Abilities", 0.0, 5.0, 0.0, 0.1)
min_skills_value = st.sidebar.slider("Minimum Data Value for Skills", 0.0, 5.0, 0.0, 0.1)
min_tasks_value = st.sidebar.slider("Minimum Data Value for Tasks", 0.0, 5.0, 0.0, 0.1)
min_work_activities_value = st.sidebar.slider("Minimum Data Value for Work Activities", 0.0, 5.0, 0.0, 0.1)
min_tools_value = st.sidebar.slider("Minimum Data Value for Tools", 0.0, 5.0, 0.0, 0.1)
min_work_context_value = st.sidebar.slider("Minimum Data Value for Work Context", 0.0, 5.0, 0.0, 0.1)

# Load all data
data = load_data()

# Apply the filtering based on sliders (Data Value filters)
min_values = {
    'abilities': min_abilities_value,
    'skills': min_skills_value,
    'tasks': min_tasks_value,
    'work_activities': min_work_activities_value,
    'tools': min_tools_value,
    'work_context': min_work_context_value
}

# Merge each dataset with the scale reference
abilities_with_scale = merge_with_scale_reference(data['abilities'], data['scale_reference'])
skills_with_scale = merge_with_scale_reference(data['skills'], data['scale_reference'])
tasks_with_scale = merge_with_scale_reference(data['task_statements'], data['scale_reference'])
work_activities_with_scale = merge_with_scale_reference(data['work_activities'], data['scale_reference'])
tools_with_scale = merge_with_scale_reference(data['tools_used'], data['scale_reference'])
work_context_with_scale = merge_with_scale_reference(data['work_context'], data['scale_reference'])

# Function to filter data based on Data Values and show detailed results
def filter_data_by_value(data, min_values):
    filtered_abilities = data['abilities'][data['abilities']['Data Value'] >= min_values['abilities']]
    filtered_skills = data['skills'][data['skills']['Data Value'] >= min_values['skills']]
    filtered_tasks = data['task_statements'][data['task_statements']['Data Value'] >= min_values['tasks']]
    filtered_work_activities = data['work_activities'][data['work_activities']['Data Value'] >= min_values['work_activities']]
    filtered_tools = data['tools_used'][data['tools_used']['Data Value'] >= min_values['tools']]
    filtered_work_context = data['work_context'][data['work_context']['Data Value'] >= min_values['work_context']]
    
    return {
        "abilities": filtered_abilities,
        "skills": filtered_skills,
        "tasks": filtered_tasks,
        "work_activities": filtered_work_activities,
        "tools_used": filtered_tools,
        "work_context": filtered_work_context
    }

# Apply the filter function with minimum values
filtered_data = filter_data_by_value(data, min_values)

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

# Display filtered work context (to assess if the occupation involves dangerous or automation-suitable work)
st.subheader("Work Context (Danger Assessment)")
st.write(filtered_data['work_context'])

# Show the scale references for each filtered entry
st.subheader("Scale References")
st.write("Scale names and their descriptions help understand what the Data Value represents.")

st.write(abilities_with_scale[['Abilities Element Name', 'Scale Name', 'Data Value']])
st.write(skills_with_scale[['Skills Element Name', 'Scale Name', 'Data Value']])
st.write(tasks_with_scale[['Task Title', 'Scale Name', 'Data Value']])
st.write(work_activities_with_scale[['Work Activities Element Name', 'Scale Name', 'Data Value']])
st.write(tools_with_scale[['Example', 'Scale Name', 'Data Value']])
st.write(work_context_with_scale[['Work Context Element Name', 'Scale Name', 'Data Value']])

