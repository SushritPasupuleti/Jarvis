# Jarvis

Using Facebook's Llama to build myself a versatile set of AI-powered tools.

This repo also serves as a testbed for various frameworks I want to experiment with.

## Features

- [x] Simple ChatGPT style chatbot

- [x] Question Answering from given data sources (Web links, PDFs, etc.)

- [x] Summarization of given text

- [x] gRPC server to allow calls from a better web framework like Axum, Chi, etc.

- [ ] Code generation like ChatGPT???

- [ ] A service that provides Multi-User access???

## Stack

- [Python](https://www.python.org/) + [Rust](https://www.rust-lang.org/) + [Go](https://golang.org/)

- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework

- [gRPC](https://grpc.io/) - Remote Procedure Call framework, to overcome the inherent inefficiencies of Python web frameworks + [Protocol Buffers](https://developers.google.com/protocol-buffers) - Data serialization

- [LangChain](https://www.langchain.com/) + [HuggingFace](https://huggingface.co/) - Language models + [PyTorch](https://pytorch.org/)

- [Leptos](https://leptos.dev/) - WASM Powered Web App

- [Trunk](https://trunkrs.dev/) - Rust Web Assembly bundler

- [TailwindCSS](https://tailwindcss.com/) - CSS Framework

- [BubbleTea](https://github.com/charmbracelet/bubbletea) - Terminal UI framework

## Setup

Ensure you have the following installed:

- [Python 3.x or higher](https://www.python.org/downloads/)

- [Go](https://golang.org/doc/install)

- [Rust](https://www.rust-lang.org/tools/install)

    - [Trunk](https://trunkrs.dev/)
    
        May need to run the following:

        ```bash
        rustup target add wasm32-unknown-unknown
        ```

    - [Riff Shell](https://www.riff.sh/) - For `nix` systems.

- [Node.js](https://nodejs.org/en/download/)
        
    - [Yarn](https://classic.yarnpkg.com/en/docs/install/)

    - [tailwindcss](https://tailwindcss.com/docs/installation)

Run the following commands:

Activate virtual environment

```bash
source venv/bin/activate
```

> [!NOTE]
> Depending on your shell, use the corresponding activate script in the `venv/bin` directory. (e.g. `venv/bin/activate.fish` for fish shell)

Provide permissions to `shell` scripts

```bash
chmod +x model/run.sh
```

### Nix Setup

On `nix` systems, you can use the `shell.nix` file to setup the environment. This resolves certain issues with native dependencies and provides the necessary tooling.

```bash
nix-shell
```

Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Activate virtual environment

```bash
source venv/bin/activate
```

## Usage

### Running as server

```bash
cd model
uvicorn server:app --reload
```

> Visit http://localhost:8000/docs to view the API documentation

### Running as CLI

```bash
cd cli
go run .
```

> [!WARNING]
> This is still a work in progress. The CLI is fully blocking and will not return until the process is complete. It is advised to let the result appear before trying again, as too many calls will crash your computer. This is not an issue with the server.

### Running the Web App

```bash
cd web
trunk serve
```

> Visit http://localhost:8080 to view the web app

## Development

Generating code from `.proto` files

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./model.proto
```

