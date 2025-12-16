# Fast-MCP-Research-Agent

Fast-MCP-Research-Agent is an **Enterprise Research OS** powered by FastMCP, LangChain, and Retrieval Augmented Generation (RAG). It provides a modular, extensible platform for research, knowledge retrieval, and advanced computation, with a focus on academic rigor and transparency.

## Features

- **Retrieval Augmented Generation (RAG):** Query a knowledge base using top-k vector search and dynamic prompt templates.
- **Domain-Specific Research:** Supports Physics, Math, Tech, and Social Science with academic tone and LaTeX support for formulas.
- **Source-Cited Answers:** All answers cite sources from the provided context.
- **Structured Logging:** All interactions are logged in a local SQLite database and JSON log files.
- **Extensible Tooling:** Easily add new tools to the server using the FastMCP framework.
- **Rich CLI Client:** Interactive client with a modern terminal UI using `rich`.

## Project Structure

```
├── client/           # CLI client to interact with the server
│   └── main.py
├── server/           # FastMCP server and core logic
│   ├── main.py
│   ├── core.py
│   └── __init__.py
├── data/             # Vector store and SQLite DB
├── logs/             # JSON structured logs
├── prompts/          # Prompt registry (YAML)
│   └── registry.yaml
├── requirements.txt  # Python dependencies
├── LICENSE
└── README.md
```

## Setup

1. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

2. **Configure OpenAI/embedding keys:**
	- Set your API keys as environment variables if using real LLMs/embeddings.

3. **Prepare data:**
	- Place your documents in the vector store directory (`data/vector_store/`).

## Usage

### Start the Server

```
python server/main.py
```

### Run the Client

```
python client/main.py
```

### Example Query

Interactively ask research questions, perform calculations, or use custom tools via the CLI.

## Prompt Registry

Prompts are managed in `prompts/registry.yaml` for easy customization. Example:

```
research_system_prompt: |
  You are an expert Enterprise Research Scientist.
  Domain: {domain}
  ...
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or improvements.

## License

This project is licensed under the MIT License.