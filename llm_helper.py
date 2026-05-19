import streamlit as st
from dotenv import load_dotenv 
from langchain_groq import ChatGroq
import os 

load_dotenv()

# Attempt to fetch the API key from environment variables (local) or Streamlit Secrets (cloud)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass

if not api_key:
    st.error("⚠️ Groq API Key not found! If you are on Streamlit Cloud, please add it to the App Settings > Secrets.")
    st.stop()

llm = ChatGroq(
    groq_api_key=api_key,
    model="llama-3.1-8b-instant",   # or llama-3.2-1b-preview
    temperature=0.2,
)

if __name__ == "__main__":
    res = llm.invoke("hii , how are you ?")
    print(res.content)