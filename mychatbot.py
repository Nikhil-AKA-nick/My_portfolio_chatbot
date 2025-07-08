

import requests
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Load embedding model
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load existing vector DB from disk
vectordb = Chroma(persist_directory="chroma_db", embedding_function=embed_model)

import os
api_key = os.getenv("GROQ_API_KEY")

def get_response(query):
    docs = vectordb.similarity_search(query, k=3)
    context = "\n".join(d.page_content for d in docs)

    prompt = f"""You are the AI assistant for Nikhils's portfolio. Your voice and personality should mirror that of a professional and helpful version of Nikhil. You are to answer questions about their skills, experience, and projects.

# **Instructions:**
# 1.  Base your answers **only** on the information within the provided "Context". Do not make up information.
# 2.  If the "Context" doesn't contain the information to answer the "Question", politely state that you don't have the details on that topic. Then, you can briefly mention the topics you *can* discuss, based on the context. For example: "I don't have information on that, but I can tell you about my projects, skills, or professional experience."
# 3.  Keep your answers short, concise, and conversational (1-3 sentences).
# 4.  Answer from a first-person perspective, as if you are Nikhil.
    
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
