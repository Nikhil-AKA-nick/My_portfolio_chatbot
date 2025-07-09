import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Initialization ---
# Load embedding model
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load existing vector DB from disk
# This will use the new, corrected Chroma loader
vectordb = Chroma(
    persist_directory="chroma_db", 
    embedding_function=embed_model
)

# Initialize the Groq Chat Model
# This is the new, recommended way to use Groq with LangChain
llm = ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"],
    model="llama3-8b-8192",
    temperature=0.7
)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template(
    """You are the AI assistant for Nikhil's portfolio. Speak as a professional version of Nikhil and only use the information in the context.

Instructions:
1. Answer only using the "Context". Do not make up anything.
2. If information is missing, say: "I don't have that detail, but I can tell you about my skills, experience, or projects."
3. Keep replies short, clear, and conversational (1–3 sentences).
4. Respond as if you're Nikhil, in first-person.

Context:
{context}

Question:
{question}
"""
)

# --- Main Response Function ---
def get_response(query):
    """
    Finds relevant documents and generates a response using the LLM chain.
    """
    try:
        # Retrieve relevant documents from the vector database
        docs = vectordb.similarity_search(query, k=3)
        if not docs:
            return "I don't have specific information on that topic, but I can tell you about my skills, experience, or projects."
        
        context_text = "\n".join(d.page_content for d in docs)

        # Create the chain of operations: prompt -> model -> output parser
        chain = prompt_template | llm | StrOutputParser()
        
        # Invoke the chain with the context and question
        response = chain.invoke({
            "context": context_text,
            "question": query
        })
        
        return response

    except Exception as e:
        print(f"An error occurred: {e}") # This will log to the Streamlit console
        return "Sorry, I encountered an issue while fetching a response. Please try again."
