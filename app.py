import streamlit as st
from automation_estimator import task_automation_breakdown

st.title("Task-Level Automation Estimator")
soc = st.text_input("Enter SOC Code (e.g. 53-7062.00)")

if soc:
    df = task_automation_breakdown(soc)
    st.dataframe(df)
