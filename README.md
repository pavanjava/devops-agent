# DevOps Agent

An AI-powered CLI tool to assist with DevOps troubleshooting, Applications with Kubernetes architecture, log analysis, and infrastructure code generation.

## Features

- 📊 **Log Analysis**: Analyze log files and get actionable insights
- 💬 **Query Interface**: Ask questions about DevOps best practices, Terraform, Kubernetes, etc.
- 🛠️ **Template Generation**: Generate infrastructure code templates
- 🤖 **AI-Powered**: Leverages Claude AI for intelligent responses

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
```env
 export GEMINI_API_KEY=YOUR API KEY
 or 
 export ANTHROPIC_API_KEY=YOUR API KEY
 or
 export OPENAI_API_KEY=YOUR API KEY
```
#### Qdrant Config for Agent Memory
```env
export QDRANT_URL=YOUR QDRANT URL
export QDRANT_API_KEY=YOUR QDRANT API KEY
```
## Usage

### Analyze Log Files

```bash
devops-agent run --log-file /path/to/app.log
```

### Ask Questions

```bash
devops-agent run --query "I need terraform script to spin up Azure blob storage"
devops-agent run --query "How to increase my pod memory and CPU in k8s"
```

### Generate Templates

```bash
devops-agent template terraform
devops-agent template kubernetes
devops-agent template docker
```

### Configuration

```bash
devops-agent config
```

## Examples

```bash
# Analyze application logs
devops-agent run --log-file ./logs/app.log --format json

# Get Terraform help
devops-agent run --query "terraform script for AWS S3 bucket with versioning"

# Kubernetes troubleshooting
devops-agent run --query "pod is in CrashLoopBackOff status, how to debug?"

# Save output to file
devops-agent run --query "docker-compose for nginx and postgres" --output docker-compose.yml
```

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

## Common issues and fixes
- if you see any error like `INFO Error checking if content_hash ed7002b439e9ac845f22357d822bac1444730fbdb6016d3ec9432297b9ec9f73 exists: Unexpected Response: 400 (Bad Request)                                 
     Raw response content:                                                                                                                                                          
     b'{"status":{"error":"Bad request: Index required but not found for \\"content_hash\\" of one of the following types: [keyword]. Help: Create an index for this key or use a   
     different filter."},"time":2 ...' `
```text
curl --request PUT \
  --url https://9df18135-290c-45b3-8158-f73b103dc352.eu-west-2-0.aws.cloud.qdrant.io:6333/collections/devops-memory/index \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
  "field_name": "content_hash",
  "field_schema": {
    "type": "keyword",
    "on_disk": true
  }
}'
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache2.0 License - see LICENSE file for details

## RoadMap

- [ ] Implement log analysis with pattern detection
- [ ] Add support for multiple LLM providers with model params `--model gpt-5-mini`
- [ ] Add Support for self-hosted models `Ollama` & `vLLM`
- [ ] Add Support for Reasoning controls
- [ ] Add Support for MCP to use local file system for quick access
- [ ] Add support for Human-in-the-Loop for more focused and collaborated work
- [ ] Create direct pip package for easy install of the agent.

## Support

For issues and questions, please open an issue on GitHub.

## Special Credits
- Built with <b>Agno2.0</b> framework for multi-agent orchestration
- Uses <b>POML</b> for structured prompt engineering
- Uses <b>Qdrant</b> for memory management
- powered by Claude (Anthropic), GPT (OpenAI) and Gemini (Google)
