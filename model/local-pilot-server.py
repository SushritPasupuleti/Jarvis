import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time

from transformers.configuration_utils import json
from codegen import generate, generate_skip_filling

app = FastAPI()

TRUNCATE_LENGTH = 2048

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

cache_duration = 60 * 60 # 1 hour

@app.post("/v1/engines/codegen/completions")
# Cache similar requests
# @cache(namespace="jarvis", expire=cache_duration)
async def code_completion(body: dict):
    print("Body:", body)
    body["n"] = 1
    if "max_tokens" in body:
        del body["max_tokens"]

    object_type = 'text_completion'
    created_time = int(time.time())
    cmpl_id = "conv-%d" % (int(time.time() * 1000000000))
    is_legacy = False
    resp_list = 'data' if is_legacy else 'choices'

    # answer = "\n print('Hello, world!')\n"
    answer = generate_skip_filling(body["prompt"])

    print("Answer:", answer)

    total_prompt_token_count = len(body["prompt"].split())
    total_completion_token_count = len(answer.split())

    respi = {
            "index": 0,
            "finish_reason": 'stop',
            "text": answer,
            # "logprobs": {'top_logprobs': [logprob_proc.token_alternatives]} if logprob_proc else None,
        }

    resp_list_data = [respi]

    resp = {
        "id": cmpl_id,
        "object": object_type,
        "created": created_time,
        "model": 'codegen',  # TODO: add Lora info?
        resp_list: resp_list_data,
        "usage": {
            "prompt_tokens": total_prompt_token_count,
            "completion_tokens": total_completion_token_count,
            "total_tokens": total_prompt_token_count + total_completion_token_count
        }
    }

    async def stream():
        yield "data: %s\n\n" % json.dumps(resp)

    if "stream" in body and body["stream"]:
        return StreamingResponse(stream(), media_type="application/json")
        # return "data: %s\n\n" % answer
    else:
        return "data: %s" % answer
