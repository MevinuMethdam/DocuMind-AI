import streamlit as st
from dotenv import load_dotenv
import os

# 1. Environment variables load කරගනිමු (.env ෆයිල් එකෙන් Key එක ගන්න)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Page Configuration (App එකේ නම සහ පෙනුම)
st.set_page_config(page_title="DocuMind-AI", layout="wide")

# 3. Header එක
st.header("🤖 DocuMind-AI: Chat with your PDF")

# 4. Sidebar (වම් පැත්තේ මෙනුව - PDF Upload කරන්න)
with st.sidebar:
    st.title("PDF Menu")
    pdf_docs = st.file_uploader("Upload your PDF files here", accept_multiple_files=True)

    # Process Button එක
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            # මෙතනට පස්සේ අපි PDF කියවන logic එක ලියනවා
            if api_key:
                st.success("API Key වැඩ කරනවා! දැන් PDF කියවන්න පුළුවන්.")
            else:
                st.error("API Key එක සොයාගත නොහැක. කරුණාකර .env ෆයිල් එක පරීක්ෂා කරන්න.")

# 5. User Input (ප්‍රශ්න අහන තැන)
user_question = st.text_input("Ask a Question from the PDF Files")

if user_question:
    st.write("User Question:", user_question)