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
    work_context = pd.read_csv("https://raw.githubusercontent.com/reen967/onet_data/main/work_context_categories.csv")
    
    return {
        "occupation_data": occupation_data,
        "abilities": abilities,
        "skills": skills,
        "task_statements": task_statements,
        "tools_used": tools_used,
        "work_activities": work_activities,
        "work_context": work_context
    }

# Filter data based on minimum Data Value for each table
def filter_data_by_value(data, min_values):
    abilities = data['abilities'][data['abilities']['Data Value'] >= min_values['abilities']]
    skills = data['skills'][data['skills']['Data Value'] >= min_values['skills']]
    tasks = data['task_statements'][data['task_statements']['Data Value'] >= min_values['tasks']]
    work_activities = data['work_activities'][data['work_activities']['Data Value'] >= min_values['work_activities']]
    tools_used = data['tools_used'][data['tools_used']['Data Value'] >= min_values['tools']]
    work_context = data['work_context'][data['work_context']['Data Value'] >= min_values['work_context']]

    return {
        "abilities": abilities,
        "skills": skills,
        "tasks": tasks,
        "work_activities": work_activities,
        "tools_used": tools_used,
        "work_context": work_context
    }

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

# Display filtered work context (which will help assess dangerous work or automation potential)
st.subheader("Work Context (Danger Assessment)")
st.write(filtered_data['work_context'])

# Insights on Automation:
st.subheader("Automation Insights")

# Assessing Automation based on the filtered data
def assess_automation(work_context_data):
    # Example: If work context involves dangerous work (e.g., exposure to hazardous conditions), automation might be more viable
    dangerous_work = work_context_data[work_context_data['Work Context Element Name'].str.contains('Hazardous', case=False)]
    
    if not dangerous_work.empty:
        st.write("**This occupation involves hazardous work.** Automating this job could significantly reduce risk to human workers.")
    else:
        st.write("**This occupation does not involve hazardous work**. Automation could be useful for efficiency but would require more precision, speed, etc.")

    return dangerous_work

# Apply the automation assessment function
dangerous_work = assess_automation(filtered_data['work_context'])

# Additional automation insights based on abilities, tools, and tasks
def analyze_automation_potential(abilities_data, tools_data):
    # Look at abilities required and tools used in context of automation potential
    speed_ability = abilities_data[abilities_data['Abilities Element Name'].str.contains('Speed', case=False)]
    precision_ability = abilities_data[abilities_data['Abilities Element Name'].str.contains('Precision', case=False)]
    
    if not speed_ability.empty:
        st.write("Automation might require **high speed** abilities.")
    if not precision_ability.empty:
        st.write("Automation might require **high precision** abilities.")
    
    if not tools_data.empty:
        st.write("**Tools used** in this occupation might also indicate automation suitability.")
        st.write(tools_data)

# Apply the automation analysis function
analyze_automation_potential(filtered_data['abilities'], filtered_data['tools_used'])

