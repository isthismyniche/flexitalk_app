import streamlit as st
from helper_functions.llm2 import generate_rag_response, load_documents, get_embeddings, retrieve_documents
import glob

# Initialise the RAG
# Load documents (adjust paths to your files)
retreival_param = 4 # number of user queries before retrieving documents again
file_paths = glob.glob("data/*.pdf")
documents = load_documents(file_paths)

# Generate embeddings for the documents
document_embeddings = get_embeddings(documents)

# Example query
query = "Explain the main concept in these documents."

# Retrieve top documents based on the query
context_docs = retrieve_documents(query, document_embeddings, documents)

# Initialise chat history
if "messages_2" not in st.session_state:
    st.session_state.messages_2 = [] # Initialise messages in chat history
if "query_count" not in st.session_state:
    st.session_state.query_count = 0  # Initialise query counter
if "context_docs" not in st.session_state:
    st.session_state.context_docs = []  # To store retrieved documents

# Function to retrieve documents based on the query
def update_context_docs(query):
    if st.session_state.query_count % retreival_param == 0:
        # Retrieve top documents based on the query
        st.session_state.context_docs = retrieve_documents(query, document_embeddings, documents)

# Display chat messages from history on app rerun
for message in st.session_state.messages_2:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.query_count += 1
    # Add user message to chat history
    st.session_state.messages_2.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # update the context documents if applicable
    update_context_docs(prompt)
    
    with st.chat_message("assistant"):
        response = generate_rag_response(st.session_state.messages_2, context_docs)
        st.write(response)
    
    st.session_state.messages_2.append({"role": "assistant", "content": response})
