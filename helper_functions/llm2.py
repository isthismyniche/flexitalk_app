import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os
import streamlit as st
import glob
from openai import OpenAI
import tiktoken
import PyPDF2

# Retrieve and load Open AI key
if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv("OPEN_API_KEY")
else:
   OPENAI_KEY = st.secrets["OPEN_API_KEY"]
   
client = OpenAI(api_key = OPENAI_KEY)

# Load and preprocess the documents
def load_documents(file_paths, max_tokens=500):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    documents = []
    
    for file_path in file_paths:
        print(f"Processing: {file_path}")
        
        # Check if the file is a PDF or a text file based on its extension
        if file_path.lower().endswith('.pdf'):
            try:
                # Read PDF file
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text() or ''  # Handle cases where extract_text() might return None
            except Exception as e:
                print(f"Failed to read PDF {file_path}: {e}")
                continue  # Skip this file and continue with others
        else:
            # First, attempt to read using UTF-8
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except UnicodeDecodeError:
                print(f"Encoding issue detected in {file_path}, attempting fallback encoding.")
                try:
                    # Attempt to read with latin-1 as a fallback
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text = f.read()
                except UnicodeDecodeError:
                    print(f"Both UTF-8 and latin-1 decoding failed for {file_path}. Ignoring errors.")
                    # As a last resort, read while ignoring problematic characters
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
        print("Completed")
        # Tokenize and split into chunks
        tokens = tokenizer.encode(text)
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i + max_tokens]
            chunk = tokenizer.decode(chunk_tokens)
            documents.append(chunk)
        
    return documents

# Embed text using OpenAI
def get_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [np.array(embedding.embedding) for embedding in response.data]

# Retrieve top documents based on similarity to the query
def retrieve_documents(query, document_embeddings, documents, top_k=3):
    query_embedding = get_embeddings([query])[0]
    similarities = cosine_similarity([query_embedding], document_embeddings).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [documents[i] for i in top_indices]

# Generate response with the relevant documents
def generate_rag_response(messages, context_docs, model="gpt-4o-mini"):
    
    for i, doc in enumerate(context_docs, 1):
        messages.append({"role": "system", "content": f"Document {i}: {doc}"})

    system_instructions = {"role" : "system", "content" : """
                            Act as a top-tier management consultant with a specialisation in 
                           flexible work arrangements. The content from the retrieved documents
                           is valuable information that you should examine carefully before replying,
                           but your reply need not be fully wedded to it.

                           Think carefully about what the user is asking, before responding.

                           Your response must be concise and insightful, and contain any relevant 
                           information from the retrieved documents. If there is no relevant 
                           information in the retrieved documents, then assess whether the user
                           is asking for hard facts or an opinion. If hard facts (e.g. statistics),
                           then explain that you do not have the information requested and guide the 
                           user towards other means of obtaining the information. If an opinion,
                           provide your best opinion.

                           Your tone should be approachable and friendly, yet crisp in providing
                           sharp responses that are backed by data and sources. Mention your sources
                           where it helps to establish credibililty. If you are mentioning your source,
                           state the title of the document drawing from the document name.
                           """}

    messages.insert(0, system_instructions)

    response = client.chat.completions.create(
        temperature=0.4,
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    # Load documents (adjust paths to your files)
    file_paths = glob.glob("data/*.pdf")
    documents = load_documents(file_paths)

    # Generate embeddings for the documents
    document_embeddings = get_embeddings(documents)

    # Example query
    query = "Explain the main concept in these documents."

    # Retrieve top documents based on the query
    context_docs = retrieve_documents(query, document_embeddings, documents)

    # Generate response with context
    messages = [
        {"role": "system", "content": "Use the following documents to answer the user's question."},
        {"role": "user", "content": query},
    ]
    response = generate_rag_response(messages, context_docs)
    print("Chatbot response:", response)
