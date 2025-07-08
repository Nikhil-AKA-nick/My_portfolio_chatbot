import os
# use the pure‑Python protobuf parser (avoids the “Descriptors cannot be created directly” error)
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"


import requests
import streamlit as st  # Needed for secrets on Streamlit Cloud
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Load embedding model
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load existing vector DB from disk
vectordb = Chroma(persist_directory="chroma_db", embedding_function=embed_model)

# Read Groq API key securely
api_key = st.secrets["GROQ_API_KEY"]  # ✅ Use this instead of os.getenv()

def get_response(query):
    docs = vectordb.similarity_search(query, k=3)
    context = "\n".join(d.page_content for d in docs)

    prompt = f"""You are the AI assistant for Nikhil's portfolio. Speak as a professional version of Nikhil and only use the information in the context.

Instructions:
1. Answer only using the "Context". Do not make up anything.
2. If information is missing, say: "I don't have that detail, but I can tell you about my skills, experience, or projects."
3. Keep replies short, clear, and conversational (1–3 sentences).
4. Respond as if you're Nikhil, in first-person.

Context:
{context}

Question:
{query}
"""

    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("API Error:", e)
        return "Sorry, I couldn't fetch a response right now."
