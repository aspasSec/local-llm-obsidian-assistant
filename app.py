import os
from fastapi import FastAPI
from pydantic import BaseModel
from rag import load_db, create_db
from llm import ask_gemini

app = FastAPI()

if not os.path.exists("db"):
    create_db()

db = load_db()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    docs = db.similarity_search(q.question, k=3)

    context = "\n\n".join(
        f"[Doc {i+1}]\n{doc.page_content}"
        for i, doc in enumerate(docs)
    )

    prompt = f"""
Você é um especialista em cibersegurança.

Responda de forma direta e técnica.

Use SOMENTE o contexto abaixo:

{context}

Pergunta: {q.question}

Se não houver informação suficiente no contexto, diga que não sabe.
"""

    resposta = ask_gemini(prompt)

    return {"answer": resposta}
