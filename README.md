# Jarvis

Using Facebook's Llama to build myself a Jarvis.

## Setup

Ensure you have the following installed:

- [Python 3.x or higher](https://www.python.org/downloads/)

Run the following commands:

Activate virtual environment

```bash
source venv/bin/activate
```

> [!NOTE]
> Depending on your shell, use the corresponding activate script in the `venv/bin` directory. (e.g. `venv/bin/activate.fish` for fish shell)

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

