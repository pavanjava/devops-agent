import asyncio
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google.gemini import Gemini
from rich.console import Console
from rich.panel import Panel

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

terraform_prompt = prompt_from_poml('terraform.poml')

console = Console()

def execute_terraform_agent(provider: str) -> Agent:

    console.print(Panel.fit(
        "[bold cyan]Terraform Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id="gpt-5-mini", api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id="claude-sonnet-4-5-20250929", temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id="gemini-2.5-flash", temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id="gpt-5-mini"),  # default

    terraform_assist = Agent(
        name="Kubernetes Agent",
        model=model,
        description="You help answer questions about the terraform technology with respect to platforms like Azure, AWS, and GCP. Always ask the cloud provider if not provided in the user_query before proceeding.",
        instructions=terraform_prompt,
        stream_intermediate_steps=True,
        markdown=True,
    )

    return terraform_assist
