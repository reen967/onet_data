import streamlit as st
from estimate_automation import estimate_automation  # adjust if named differently

st.title("Role Automation Estimator")

soc = st.text_input("Enter a SOC Code (e.g. 53-7062.00)")

if soc:
    try:
        result = estimate_automation(soc)
        st.subheader("Automation Estimate")
        st.dataframe(result)
    except Exception as e:
        st.error(f"Error processing SOC: {e}")
