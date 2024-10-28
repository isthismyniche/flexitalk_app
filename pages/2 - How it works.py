from helper_functions.utility import check_password  
import streamlit as st

# Check if the password is correct.  
if not check_password():  
    st.stop()

st.header("How it works")

st.write("Take a peek under the hood to see how this web app works!")

st.divider()

st.image("images/Practiseflexitalk.jpg", caption="How Practise flexitalk works", use_column_width=True)

st.divider()

st.image("images/Unlockflexiwork.jpg", caption="How Unlock flexiwork works", use_column_width=True)

