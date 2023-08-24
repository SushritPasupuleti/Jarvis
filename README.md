# Jarvis

Using Facebook's Llama to build myself a Jarvis.

## Setup

Ensure you have the following installed:

- [Python 3.x or higher](https://www.python.org/downloads/)

- [Go](https://golang.org/doc/install)

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

On `nix` systems, you can use the `shell.nix` file to setup the environment. This resolves certain issues with native bindings.

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

