import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="DocuMind-AI", layout="wide")

st.header("🤖 DocuMind-AI: Chat with your PDF")

with st.sidebar:
    st.title("PDF Menu")
    pdf_docs = st.file_uploader("Upload your PDF files here", accept_multiple_files=True)

    # Process Button
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            if api_key:
                st.success("API Key is work.")
            else:
                st.error("API Key is can't found. Please check .env file. ")

user_question = st.text_input("Ask a Question from the PDF Files")

if user_question:
    st.write("User Question:", user_question)