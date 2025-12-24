# DevOps Agent

An AI-powered CLI tool to assist with DevOps troubleshooting, Applications with Kubernetes architecture, log analysis, and infrastructure code generation.

## Features

- 📊 **Log Analysis**: Analyze log files and get actionable insights
- 💬 **Query Interface**: Ask questions about DevOps best practices, Terraform, Kubernetes, etc.
- 🛠️ **Template Generation**: Generate infrastructure code templates
- 🤖 **AI-Powered**: Leverages multiple LLM providers (OpenAI, Anthropic, Gemini, Ollama, vLLM)
- 🎯 **Flexible Provider Selection**: Choose your preferred LLM provider and model dynamically
- 🔒 **Self-Hosted Options**: Run privately with Ollama or vLLM
- 🧠 **Reasoning Mode**: Enable advanced reasoning capabilities for complex queries
- 🐛 **Debug Mode**: Troubleshoot agent behavior with detailed logging
- 💾 **Memory Management**: Persistent context using Qdrant vector database
- 🎨 **Interactive Mode**: Engage in continuous conversations with the agent
- 📝 **Multiple Output Formats**: Export results as text, JSON, or Markdown

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/devops-agent.git
cd devops-agent

# Install in development mode
pip install -e .

# Or install from PyPI (when published)
pip install devops-agent
```

## Configuration
#### LLM API KEYS
```bash
# For OpenAI
export OPENAI_API_KEY=YOUR_API_KEY

# For Anthropic Claude
export ANTHROPIC_API_KEY=YOUR_API_KEY

# For Google Gemini
export GEMINI_API_KEY=YOUR_API_KEY

# For Ollama (self-hosted, typically no API key needed)
export OLLAMA_API_KEY=YOUR_API_KEY  # Optional

# For vLLM (self-hosted)
export VLLM_API_KEY=YOUR_API_KEY
```
#### Qdrant Config for Agent Memory
(If not configured fall backs to in-memory vector store)
```env
export QDRANT_URL=YOUR QDRANT URL
export QDRANT_API_KEY=YOUR QDRANT API KEY
```
## Usage

#### Ask Questions

```bash
devops-agent run --query "I need terraform script to spin up Azure blob storage"
devops-agent run --query "How to increase my pod memory and CPU in k8s"
```

#### Interactive Mode

```bash
devops-agent run --interactive
# or
devops-agent run -i
```

### Advanced Options

#### Choose Your LLM Provider and Model

```bash
# Use OpenAI with a specific model
devops-agent run --provider openai --model gpt-4o --query "your question"

# Use Anthropic Claude
devops-agent run --provider anthropic --model claude-sonnet-4-20250514 --query "your question"

# Use Google Gemini
devops-agent run --provider google --model gemini-2.0-flash-exp --query "your question"

# Use Ollama (self-hosted)
devops-agent run --provider ollama --model llama3 --query "your question"

# Use vLLM (self-hosted)
devops-agent run --provider vllm --model your-model-name --query "your question"
```

#### Enable Debug Mode

```bash
devops-agent run --query "your question" --debug_mode true
```

#### Enable Reasoning Mode

```bash
devops-agent run --query "your question" --reasoning_enabled true
```

#### Combine Multiple Options

```bash
# Interactive mode with specific provider, model, and reasoning
devops-agent run -i --provider anthropic --model claude-sonnet-4-20250514 --reasoning_enabled true

# Query with debug mode and custom output
devops-agent run --query "docker setup for microservices" --provider openai --model gpt-4o --debug_mode true --output result.md --format markdown
```

## CLI Options Reference

### `devops-agent run` Options

| Option | Type | Description |
|--------|------|-------------|
| `--log-file` | Path | Path to log file to analyze |
| `--provider` | String | LLM provider (openai, anthropic, google, ollama, vllm) |
| `--model` | String | Model name (e.g., gpt-4o, claude-sonnet-4-20250514, gemini-2.0-flash-exp) |
| `--query` | String | Query to ask the DevOps agent |
| `--output` | Path | Output file path for saving results |
| `--format` | Choice | Output format: text, json, or markdown (default: text) |
| `--interactive, -i` | Flag | Run in interactive mode for continuous conversation |
| `--debug_mode` | Boolean | Enable debug mode with detailed logging |
| `--reasoning_enabled` | Boolean | Enable reasoning mode for complex problem-solving |

### Provider-Specific Model Examples

**OpenAI:**
- `gpt-4o`
- `gpt-5-mini`
- `gpt-5.1`

**Anthropic:**
- `claude-sonnet-4-20250514`
- `claude-sonnet-4-5-20250929`
- `claude-3-5-sonnet-20241022`

**Google:**
- `gemini-3-pro`
- `gemini-2.5-pro`
- `gemini-2.5-flash`

**Ollama (Self-hosted):**
- `granite4:3b`
- `qwen3:8b`
- `cogito:latest`
- Any model you have pulled locally

**vLLM (Self-hosted):**
- Any model served by your vLLM instance

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black devops_agent/
isort devops_agent/

# Lint
flake8 devops_agent/
```

## Project Structure

```
devops-agent/
├── devops_agent/          # Main package
│   ├── cli.py            # CLI interface
│   ├── core/             # Core functionality
│   ├── templates/        # Template generators
│   ├── utils/            # Utilities
│   └── prompts/          # LLM prompts
└── docs/                 # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache2.0 License - see LICENSE file for details

## RoadMap

- [ ] Implement log analysis with pattern detection
- [ ] Add Support for MCP to use local file system for quick access
- [ ] Add support for Human-in-the-Loop for more focused and collaborated work
- [ ] Support for custom prompt templates
- [ ] Agent as a Service with privacy first concept

## Support

For issues and questions, please open an issue on GitHub.

## Special Credits
- Built with <b>Agno2.0</b> framework for multi-agent orchestration
- Uses <b>POML</b> for structured prompt engineering
- Uses <b>Qdrant</b> for memory management
- powered by Claude (Anthropic), GPT (OpenAI) and Gemini (Google)
