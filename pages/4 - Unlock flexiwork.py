import streamlit as st
from helper_functions.llm2 import generate_rag_response, load_documents, get_embeddings, retrieve_documents
import glob
from helper_functions.utility import check_password  

# Check if the password is correct.  
if not check_password():  
    st.stop()

st.header("Unlock _flexiwork_")
st.write("Wondering how you can unlock flexiwork at your workplace? Have a chat with our"
         " bot, which is conversant Singapore's tripartite guidelines on flexible work arrangements, "
         "and the latest research on global trends and research on flexiwork! We seek your "
         "understanding that the bot may take a minute to come alive.")

# Initialise the RAG
# Load documents (adjust paths to your files)
retreival_param = 3 # number of user queries before retrieving documents again
file_paths = glob.glob("data/*.pdf")

# Initialise chat history
if "messages_2" not in st.session_state:
    st.session_state.messages_2 = [] # Initialise messages in chat history
if "query_count" not in st.session_state:
    st.session_state.query_count = 0  # Initialise query counter
if "context_docs" not in st.session_state:
    st.session_state.context_docs = []  # To store retrieved documents
if "documents" not in st.session_state:
    st.session_state.documents = load_documents(file_paths)
    # Generate embeddings for the documents
    st.session_state.document_embeddings = get_embeddings(st.session_state.documents)

# Function to retrieve documents based on the query
def update_context_docs(query):
    if st.session_state.query_count % retreival_param == 0:
        # Retrieve top documents based on the query
        st.session_state.context_docs = retrieve_documents(query, st.session_state.document_embeddings, st.session_state.documents)

# Display chat messages from history on app rerun
for message in st.session_state.messages_2:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me about the types of flexible work arrangements you can implement."):
    # update the context documents if applicable
    update_context_docs(prompt)

    st.session_state.query_count += 1
    # Add user message to chat history
    st.session_state.messages_2.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = generate_rag_response(st.session_state.messages_2, st.session_state.context_docs)
        st.write(response)
    
    st.session_state.messages_2.append({"role": "assistant", "content": response})
