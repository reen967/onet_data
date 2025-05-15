import streamlit as st
import pandas as pd

# Load CSV data
def load_data():
    # Load all CSV files into pandas DataFrames
    abilities = pd.read_csv('abilities.csv')
    abilities_descriptions = pd.read_csv('abilities_descriptions.csv')
    abilities_to_work_activities = pd.read_csv('abilities_to_work_activities.csv')
    abilities_to_work_context = pd.read_csv('abilities_to_work_context.csv')
    alternate_titles = pd.read_csv('alternate_titles.csv')
    basic_interests_to_riasec = pd.read_csv('basic_interests_to_riasec.csv')
    content_model_reference = pd.read_csv('content_model_reference.csv')
    frequency_of_task_categories = pd.read_csv('frequency_of_task_categories.csv')
    interests = pd.read_csv('interests.csv')
    interests_to_illustrative_activities = pd.read_csv('interests_to_illustrative_activities.csv')
    interests_to_illustrative_occupations = pd.read_csv('interests_to_illustrative_occupations.csv')
    interests_to_riasec_keywords = pd.read_csv('interests_to_riasec_keywords.csv')
    knowledge = pd.read_csv('knowledge.csv')
    level_scale_anchors = pd.read_csv('level_scale_anchors.csv')
    occupation_data = pd.read_csv('occupation_data.csv')
    related_occupations = pd.read_csv('related_occupations.csv')
    scales_reference = pd.read_csv('scales_reference.csv')
    skills = pd.read_csv('skills.csv')
    skills_to_work_activities = pd.read_csv('skills_to_work_activities.csv')
    skills_to_work_context = pd.read_csv('skills_to_work_context.csv')
    task_statements = pd.read_csv('task_statements.csv')
    tasks_to_dwa = pd.read_csv('tasks_to_dwa.csv')
    technology_skills = pd.read_csv('technology_skills.csv')
    tools_used = pd.read_csv('tools_used.csv')
    unspsc_reference = pd.read_csv('unspsc_reference.csv')
    work_activities = pd.read_csv('work_activities.csv')
    work_activities_to_iwa = pd.read_csv('work_activities_to_iwa.csv')
    work_activities_to_iwa_to_dwa = pd.read_csv('work_activities_to_iwa_to_dwa.csv')
    work_context_categories = pd.read_csv('work_context_categories.csv')

    return {
        'abilities': abilities,
        'abilities_descriptions': abilities_descriptions,
        'abilities_to_work_activities': abilities_to_work_activities,
        'abilities_to_work_context': abilities_to_work_context,
        'occupation_data': occupation_data,
        'skills': skills,
        'tasks': task_statements,
        'tools_used': tools_used,
        'work_activities': work_activities
    }

# Merge data based on occupation search
def get_occupation_data(occupation_code, data):
    # Start by merging occupation data with abilities, skills, etc.
    occupation = data['occupation_data'][data['occupation_data']['O*NET-SOC Code'] == occupation_code]

    if occupation.empty:
        st.error(f"No data found for occupation code: {occupation_code}")
        return
    
    abilities = pd.merge(occupation, data['abilities'], on='O*NET-SOC Code', how='inner')
    skills = pd.merge(occupation, data['skills'], on='O*NET-SOC Code', how='inner')
    tasks = pd.merge(occupation, data['tasks'], on='O*NET-SOC Code', how='inner')
    tools = pd.merge(occupation, data['tools_used'], on='O*NET-SOC Code', how='inner')
    work_activities = pd.merge(occupation, data['work_activities'], on='O*NET-SOC Code', how='inner')

    # Show occupation data
    st.subheader(f"Occupation: {occupation_code}")
    st.write(occupation)

    # Show abilities
    st.subheader("Abilities")
    st.write(abilities)

    # Show skills
    st.subheader("Skills")
    st.write(skills)

    # Show tasks
    st.subheader("Tasks")
    st.write(tasks)

    # Show tools
    st.subheader("Tools Used")
    st.write(tools)

    # Show work activities
    st.subheader("Work Activities")
    st.write(work_activities)

# Streamlit UI elements
def app():
    st.title("O*NET Occupation Data Viewer")

    # Load all data
    data = load_data()

    # Input occupation code
    occupation_code = st.text_input("Enter Occupation Code (e.g., 11-1011.00 for Chief Executives)", "")

    if occupation_code:
        get_occupation_data(occupation_code, data)

if __name__ == '__main__':
    app()
