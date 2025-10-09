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

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache2.0 License - see LICENSE file for details

## Roadmap

- [ ] Implement log analysis with pattern detection
- [ ] Add support for multiple LLM providers
- [ ] Create template library for common infrastructure patterns
- [ ] Add interactive mode
- [ ] Support for custom plugins
- [ ] Integration with CI/CD pipelines

## Support

For issues and questions, please open an issue on GitHub.
