import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("System error: GOOGLE_API_KEY cannot be found. Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

@st.cache_resource
def get_embeddings():
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        convert_system_message_to_human=True
    )

    embeddings = get_embeddings()

    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key='answer'
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def user_input(user_question):
    if not os.path.exists("faiss_index"):
        st.error("Please upload and process a PDF first.")
        return

    chain = get_conversational_chain()

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    response = chain({"question": user_question, "chat_history": st.session_state['chat_history']})
    st.session_state['chat_history'] = response['chat_history']

    st.write("🤖 **DocuMind:**", response["answer"])

def main():
    st.set_page_config(page_title="Chat with PDF", layout="wide")
    st.header("🤖 DocuMind-AI: Chat with your PDF")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing PDF..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("Success! Now ask questions.")
                    st.rerun()
            else:
                st.warning("Please select a PDF first.")


if __name__ == "__main__":
    main()