# Notes

All the notes I took while working on this project.

## Copilot Requests

By intercepting the requests that the Copilot Extension makes, the following payload was found:

```json
{
    "prompt": "#!/usr/bin/env python3\nprint("Hello world")\nprint(",
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

