from dotenv import load_dotenv 
from langchain_groq import ChatGroq
import os 

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",   # or llama-3.2-1b-preview
    temperature=0.2,
)

if __name__ == "__main__":
    res = llm.invoke("hii , how are you ?")
    print(res.content)