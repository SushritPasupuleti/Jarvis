# Notes

All the notes I took while working on this project.

## Copilot Requests

> [!NOTE]
> Copilot's extensions utilize a lot of `wasm` code, which is hard to decipher, and a lot of important logic is implemented using the same, hence I had to intercept the requests using Postman's Interceptor and an empty `FastAPI` route.

By intercepting the requests that the Copilot Extension makes, the following payload was found:

```json
{
    "prompt": "#!/usr/bin/env python3\nprint(\"Hello world\")\nprint(",
    "suffix": "",
    "max_tokens": 500,
    "temperature": 0,
    "top_p": 1,
    "n": 1,
    "stop": [
        "\n"
    ],
    "stream": true,
    "extra": {
        "language": "python",
        "next_indent": 0,
        "trim_by_indentation": true,
        "prompt_tokens": 17,
        "suffix_tokens": 0
    }
}
```
## Copilot Responses

All requests seem to expect a Stream response, with the following payload:

```json
{
    "id": "<conversation_id>",
    "object": "text_completion",
    "created": "<epoch_timestamp>",
    "model": "codegen",
    "data": [{

        "index": 0,
        "finish_reason": "length/false",
        "text": "<generated_code>",
    }],
    "usage": {
        "prompt_tokens": "<total prompt tokens>",
        "prefix_tokens": "<total prefix tokens>",
        "total_tokens": "prompt_tokens + prefix_tokens"
    }
}
```

The data must be sent as a stringified JSON object, prefixed by `data: `. 

> [!NOTE]
> The `data` field, can return multiple responses, as Copilot can generate multiple suggestions. This however is not resource friendly nor quick enough for a local deployment.

Based on the documentation of the VSCode extension, the following settings can be changed to change the Copilot Extension's target URL:

```json
{
    "github.copilot.advanced": {
        "debug.overrideEngine": "codegen",
        "debug.testOverrideProxyUrl": "http://localhost:8000",
        "debug.overrideProxyUrl": "http://localhost:8000",
    }
}
```

And the endpoint that the extension calls is: `/v1/engines/codegen/completions`

