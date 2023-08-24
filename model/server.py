from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from main import llm_chain
from pydantic import BaseModel
from web_answers import get_web_answers

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Hello There",
        "status": "OK"
    }

@app.get("/chat/{question}")
async def chat(question: str):
    answer = llm_chain.run(question)

    print("Question: ", question)
    print("Answer: ", answer)

    return {
        "question": question,
        "answer": answer
    }

class WebLinks(BaseModel):
    links: list
    question: str

@app.post("/web/chat/")
async def web_chat(web_links: WebLinks):
    result = get_web_answers(web_links.links, web_links.question)

    return {
        "question": web_links.question,
        "answer": result['answer'],
        "source": result['source_documents']
    }
