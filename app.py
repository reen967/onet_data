import streamlit as st
import pandas as pd

# Load the linked data Python file (linked_data.py) to merge all tables
# Assuming linked_data.py is in the same directory as your app.py

from linked_data import *

# Streamlit App

def app():
    st.title('O*NET Data Analysis and Visualizations')

    # Show a summary of the merged datasets
    st.subheader('Occupation with Abilities')
    st.write(occupation_with_abilities.head())

    st.subheader('Occupation with Skills')
    st.write(occupation_with_skills.head())

    st.subheader('Task with DWA')
    st.write(task_with_dwa.head())

    st.subheader('Work Context with Activities')
    st.write(work_context_with_activities.head())

    # You can display more datasets or perform further analyses here
    # Add visualizations, stats, or additional filters as needed
    # For example:
    st.subheader('Occupation and Skills Visualization')
    occupation_skill_counts = occupation_with_skills.groupby('Title').size()
    st.bar_chart(occupation_skill_counts)

# Run the app
if __name__ == '__main__':
    app()


