import streamlit as st
import pandas as pd

# Load data
@st.cache
def load_data():
    # Load the linked data file (adjust the path as needed)
    linked_data = pd.read_csv('linked_data.csv')
    
    # Load other CSV files if needed for further exploration
    abilities = pd.read_csv('abilities.csv')
    work_activities = pd.read_csv('work_activities.csv')
    skills = pd.read_csv('skills.csv')
    tasks = pd.read_csv('task_statements.csv')
    tools_used = pd.read_csv('tools_used.csv')
    
    return linked_data, abilities, work_activities, skills, tasks, tools_used

linked_data, abilities, work_activities, skills, tasks, tools_used = load_data()

# Sidebar for navigation
st.sidebar.title("Data Exploration App")
sidebar_selection = st.sidebar.radio("Select Data to Explore", ["Linked Data", "Abilities", "Work Activities", "Skills", "Tasks", "Tools Used"])

# Show Linked Data (default view)
if sidebar_selection == "Linked Data":
    st.title("Linked Data Overview")
    st.write("Explore the connections between occupations, abilities, tasks, and more.")
    st.write(linked_data)

# Show Abilities Data
elif sidebar_selection == "Abilities":
    st.title("Abilities Data")
    st.write("Explore abilities related to occupations.")
    st.write(abilities)

# Show Work Activities Data
elif sidebar_selection == "Work Activities":
    st.title("Work Activities Data")
    st.write("Explore work activities related to occupations.")
    st.write(work_activities)

# Show Skills Data
elif sidebar_selection == "Skills":
    st.title("Skills Data")
    st.write("Explore skills related to occupations.")
    st.write(skills)

# Show Tasks Data
elif sidebar_selection == "Tasks":
    st.title("Tasks Data")
    st.write("Explore tasks related to occupations.")
    st.write(tasks)

# Show Tools Used Data
elif sidebar_selection == "Tools Used":
    st.title("Tools Used Data")
    st.write("Explore tools used in various occupations.")
    st.write(tools_used)

# Display a specific link between elements
st.sidebar.title("Explore Relationships")
entity_1 = st.sidebar.selectbox("Select First Entity", ['Abilities', 'Work Activities', 'Skills', 'Tasks', 'Tools Used'])
entity_2 = st.sidebar.selectbox("Select Second Entity", ['Abilities', 'Work Activities', 'Skills', 'Tasks', 'Tools Used'])

if entity_1 and entity_2:
    st.title(f"Relationships between {entity_1} and {entity_2}")
    selected_links = linked_data[(linked_data['Entity_1'] == entity_1) & (linked_data['Entity_2'] == entity_2)]
    st.write(selected_links)

# Add some interactivity to explore more options
st.sidebar.title("Other Options")
if st.sidebar.button("Show Linked Data Summary"):
    st.write("Summary of Linked Data:")
    st.write(linked_data.describe())

