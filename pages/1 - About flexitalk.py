from helper_functions.utility import check_password  
import streamlit as st

# Check if the password is correct.  
if not check_password():  
    st.stop()