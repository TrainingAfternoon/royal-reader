# Royal Reader
## Developer Set Up
Install [`uv`](https://docs.astral.sh/uv/)
```bash
curl -LsSf https://astral.sh/uv/install.sh | less
```

Install all developer packages
```bash
uv sync
```

Install [pre-commit](https://pre-commit.com/)
```bash
uv run pre-commit install
```

Run the app
```bash
uv run main.py
```
