from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from main import llm_chain
from web_answers import get_web_answers

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

cache_duration = 60 * 60 # 1 hour

@app.get("/")
@cache(namespace="jarvis", expire=cache_duration)
async def read_root():
    return JSONResponse({
        "message": "Hello There",
        "status": "OK",
    })

@app.get("/clear-cache")
async def clear():
    return await FastAPICache.clear(namespace="jarvis")

@app.get("/chat/{question}")
@cache(namespace="jarvis", expire=cache_duration)
async def chat(question: str):
    answer = llm_chain.run(question)

    # print("Question: ", question)
    # print("Answer: ", answer)

    return JSONResponse({
        "question": question,
        "answer": answer,
    })

class WebLinks(BaseModel):
    links: list
    question: str

class DocLinks(WebLinks):
    links: list
    question: str

@app.post("/web/chat/")
@cache(namespace="jarvis", expire=cache_duration)
async def web_chat(web_links: WebLinks):
    result = get_web_answers(web_links.links, "web", web_links.question)

    return {
        "question": web_links.question,
        "answer": result['answer'],
        "source": result['source_documents'],
    }

@app.post("/doc/chat/")
@cache(namespace="jarvis", expire=cache_duration)
async def doc_chat(doc_links: DocLinks):
    result = get_web_answers(doc_links.links, "doc", doc_links.question)

    return {
        "question": doc_links.question,
        "answer": result['answer'],
        "source": result['source_documents'],
    }
