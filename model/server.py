from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from main import llm_chain

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
