import streamlit as st
from helper_functions.llm import generate_llm_response
from helper_functions.utility import check_password  

# Check if the password is correct.  
if not check_password():  
    st.stop()

st.header("Practise _flexitalk_")
st.write("Need to prepare for a difficult conversation with your staff about flexible work "
             "arrangements? Put yourself in their shoes and have a chat with our bot! Our bot will respond"
              " as the supervisor, which will help you think of ways in which you can manage the "
              "conversation and come to a fruitful landing.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Put yourself in the shoes of your staff, and speak to me about flexiwork!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = generate_llm_response(st.session_state.messages)
        st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
