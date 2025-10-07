# DevOps Agent 🤖

An intelligent AI-powered CLI assistant for DevOps engineers, providing expert guidance on Kubernetes, Terraform, and DevOps best practices. Built with multi-agent architecture and supporting multiple LLM providers.

## ✨ Features

- **Multi-Agent Architecture**: Specialized agents for DevOps, Kubernetes, and Terraform domains
- **Multi-LLM Support**: Choose between OpenAI, Anthropic (Claude), or Google (Gemini)
- **Interactive Mode**: Conversational interface for continuous assistance
- **Log Analysis**: Automated analysis of log files with insights and error detection
- **GitOps & Cloud-Native**: Expert knowledge of modern DevOps practices
- **Memory System**: Uses Qdrant vector database for contextual memory across sessions
- **POML Prompts**: Structured prompts using POML (Prompt Markup Language) for consistent agent behavior

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/devops-agent.git
cd devops-agent

# Install dependencies
pip install -e .
```

### Configuration

Create a `.env` file in the project root with your API keys:

```env
# Choose one or more providers
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here

# Qdrant configuration (for memory)
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
```

## 📖 Usage Examples

### 1. Interactive Mode with Anthropic (Recommended)

```bash
devops-agent run --provider anthropic --interactive
```

Start a conversation with the DevOps team. Ask multiple questions in sequence, and the agents will remember context across the session.

### 2. Single Query with OpenAI

```bash
devops-agent run --provider openai --query "How do I set up a multi-region Kubernetes cluster on AWS EKS with GitOps?"
```

Get immediate answers to specific DevOps questions without entering interactive mode.

### 3. Terraform Infrastructure Code Generation

```bash
devops-agent run --provider anthropic --query "Create a Terraform module for Azure AKS cluster with monitoring and auto-scaling" --output terraform-aks.tf --format text
```

Generate infrastructure code and save it directly to a file.

### 4. Kubernetes Troubleshooting

```bash
devops-agent run --provider google --query "My pods are in CrashLoopBackOff state. How do I debug this issue systematically?"
```

Get step-by-step troubleshooting guidance for Kubernetes issues.

### 5. Log File Analysis

```bash
devops-agent run --provider anthropic --log-file ./logs/application.log
```

Analyze log files for critical errors, patterns, anomalies, and significant findings with AI-powered insights.

### 6. Save Conversation to File

```bash
devops-agent run --provider openai --query "Best practices for implementing GitOps with ArgoCD" --output gitops-guide.md --format markdown
```

Export responses in text, JSON, or Markdown format for documentation.

## 🏗️ Project Structure

```
devops-agent/
├── devops_agent/
│   ├── cli.py                          # Main CLI interface with Click
│   ├── core/                           # Core agent implementations
│   │   ├── master_agent.py            # Orchestrator agent routing queries
│   │   ├── devops_agent.py            # DevOps troubleshooting specialist
│   │   ├── kubernetes_agent.py        # Kubernetes architecture expert
│   │   ├── terraform_agent.py         # Terraform/IaC specialist
│   │   └── log_analysis_agent.py      # Log file analysis agent
│   ├── prompts/                        # POML-based structured prompts
│   │   ├── devops.poml                # DevOps troubleshooting instructions
│   │   ├── kubernetes.poml            # Kubernetes architecture guidelines
│   │   └── terraform.poml             # Terraform best practices
│   └── utils/                          # Utility functions
│       └── prompt_generator_from_poml.py  # POML to prompt converter
├── setup.py                            # Package setup configuration
├── pyproject.toml                      # Modern Python project config
├── requirements.txt                    # Project dependencies
├── .env                                # Environment variables (create this)
└── README.md                           # This file
```

### Key Components

- **`cli.py`**: Command-line interface handling user input, interactive mode, and output formatting
- **`master_agent.py`**: Routes queries to specialized agents based on domain (DevOps, K8s, Terraform)
- **`devops_agent.py`**: Handles incident response, observability, and general DevOps troubleshooting
- **`kubernetes_agent.py`**: Kubernetes architecture, GitOps workflows, and cloud-native practices
- **`terraform_agent.py`**: Infrastructure as Code, state management, and multi-cloud deployments
- **`log_analysis_agent.py`**: Analyzes log files for errors, patterns, and anomalies
- **`.poml` files**: Structured prompt definitions using POML markup language

## 🛠️ CLI Commands

### Run Command

```bash
devops-agent run [OPTIONS]

Options:
  --provider TEXT              LLM provider: openai, anthropic, or google
  --query TEXT                 Single query to process
  --log-file PATH              Path to log file for analysis
  --output PATH                Save response to file
  --format [text|json|markdown] Output format (default: text)
  -i, --interactive            Run in interactive conversation mode
  --help                       Show help message
```

### Version

```bash
devops-agent --version
```

## 🧠 How It Works

1. **Query Routing**: Master agent analyzes your question and routes it to the appropriate specialist agent
2. **Domain Expertise**: Each agent uses specialized POML-defined knowledge for accurate responses
3. **Memory System**: Qdrant vector database stores conversation history for contextual awareness
4. **Multi-LLM**: Choose the best model for your needs - Claude Sonnet 4.5, GPT-5-mini, or Gemini 2.5
5. **Streaming Responses**: See agent reasoning and responses in real-time

## 📋 Requirements

- Python >= 3.8
- API key for at least one LLM provider (OpenAI, Anthropic, or Google)
- Optional: Qdrant instance for persistent memory (can use in-memory fallback)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and commit: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Format code
black devops_agent/
isort devops_agent/

# Lint
flake8 devops_agent/
```

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and well-described
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Agno](https://github.com/agno-oss/agno) framework for multi-agent orchestration
- Uses [POML](https://github.com/poml-lang/poml) for structured prompt engineering
- Powered by Claude (Anthropic), GPT (OpenAI), and Gemini (Google)

## 📬 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/yourusername/devops-agent/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/yourusername/devops-agent/discussions)
- **Email**: manthapavankumar11@gmail.com

## 🗺️ Roadmap

- [ ] Add CI/CD pipeline integration
- [ ] Support for custom agent creation
- [ ] Web UI interface
- [ ] Docker and Helm chart templates generation
- [ ] Integration with monitoring tools (Prometheus, Grafana)
- [ ] Multi-language support for responses
- [ ] Plugin system for extensibility

---

Made with ❤️ by M K Pavan Kumar