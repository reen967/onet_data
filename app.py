import streamlit as st
import pandas as pd

# Load CSV files
@st.cache_data
def load_data():
    occupation_data = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/occupation_data.csv")
    abilities = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/abilities.csv")
    skills = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/skills.csv")
    task_statements = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/task_statements.csv")
    work_activities = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/work_activities.csv")
    work_context = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/work_context_categories.csv")
    scale_reference = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/scales_reference.csv")
    
    return occupation_data, abilities, skills, task_statements, work_activities, work_context, scale_reference

# Merge with Scale Reference to provide clarity
def merge_with_scale_reference(data, scale_reference):
    data_with_scale = data.merge(scale_reference, how="left", left_on="Scale ID", right_on="Scale ID")
    return data_with_scale

# Filtering function based on Data Value and Scale
def filter_data(data, min_value):
    return data[data['Data Value'] >= min_value]

# Streamlit UI for filtering data values
st.sidebar.header("Filter Data")
min_value = st.sidebar.slider("Minimum Data Value", 0.0, 5.0, 0.0, 0.1)

# Load data
occupation_data, abilities, skills, task_statements, work_activities, work_context, scale_reference = load_data()

# Merge data with scale reference
abilities_with_scale = merge_with_scale_reference(abilities, scale_reference)
skills_with_scale = merge_with_scale_reference(skills, scale_reference)
task_with_scale = merge_with_scale_reference(task_statements, scale_reference)
work_activities_with_scale = merge_with_scale_reference(work_activities, scale_reference)
work_context_with_scale = merge_with_scale_reference(work_context, scale_reference)

# Filter data by minimum Data Value
filtered_abilities = filter_data(abilities_with_scale, min_value)
filtered_skills = filter_data(skills_with_scale, min_value)
filtered_tasks = filter_data(task_with_scale, min_value)
filtered_work_activities = filter_data(work_activities_with_scale, min_value)
filtered_work_context = filter_data(work_context_with_scale, min_value)

# Display the filtered results
st.title("Filtered Occupation Data Based on Automation Criteria")
st.write("Showing occupations where the data value meets or exceeds the minimum filter threshold.")

# Display filtered abilities
st.subheader("Abilities")
st.write(filtered_abilities[['Abilities Element Name', 'Scale Name', 'Data Value']])

# Display filtered skills
st.subheader("Skills")
st.write(filtered_skills[['Skills Element Name', 'Scale Name', 'Data Value']])

# Display filtered tasks
st.subheader("Tasks")
st.write(filtered_tasks[['Task Title', 'Scale Name', 'Data Value']])

# Display filtered work activities
st.subheader("Work Activities")
st.write(filtered_work_activities[['Work Activities Element Name', 'Scale Name', 'Data Value']])

# Display filtered work context
st.subheader("Work Context")
st.write(filtered_work_context[['Work Context Element Name', 'Scale Name', 'Data Value']])

# Display scale reference details for context
st.subheader("Scale Reference Definitions")
st.write(scale_reference[['Scale Name', 'Minimum', 'Maximum']])
