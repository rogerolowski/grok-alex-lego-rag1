import os
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import sqlite3
import streamlit as st

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize SQLite database
conn = sqlite3.connect("lego_data.db")
cursor = conn.cursor()
print("Connected to SQLite database")

# Load data into ChromaDB (using preloaded data)
print("Loading data into ChromaDB...")
texts = [row[3] for row in cursor.execute("SELECT details FROM lego_data").fetchall()]
if not texts:
    st.error("No data found in database. Run preload_db.py first.")
else:
    print(f"Loaded {len(texts)} records from database")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Chroma.from_texts(texts, embeddings, persist_directory="./chroma_db")
vectorstore.persist()
print("ChromaDB loaded and persisted")

# Initialize LLM and RetrievalQA
print("Initializing LLM and RetrievalQA...")
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
print("RetrievalQA initialized")

# Streamlit UI
st.title("LEGO RAG Search (Rebrickable, Brickset, BrickOwl)")
query = st.text_input("Ask about LEGO sets:")
if query:
    print(f"Processing query: {query}")
    response = qa_chain.run(query)
    print(f"Response: {response}")
    st.write(response)

# Cleanup
conn.close()
print("Database connection closed")