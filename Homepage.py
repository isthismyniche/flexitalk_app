import os
import streamlit as st  
from helper_functions.utility import check_password  

# Check if the password is correct.  
if not check_password():  
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="flexitalk homepage"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("_flexitalk_")

st.markdown(
    """
    <style>
    .custom-text {
        font-family: 'Cursive', sans-serif;
        color: #A9A9A9;  
        font-size: 24px;  
    }
    </style>
    <p class="custom-text">Practise having difficult conversations with your
    boss or report! And learn more about how flexible work arrangements could
    work for you and your organisation.</p>
    """, unsafe_allow_html=True
)

# Create an expander for the important notice
with st.expander("IMPORTANT NOTICE", expanded=True):
    st.markdown("""
    This web application is a prototype developed for educational purposes only. The information provided here is 
    NOT intended for real-world usage and should not be relied upon for making any decisions, especially those 
    related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full 
    responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)