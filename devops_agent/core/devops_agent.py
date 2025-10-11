import asyncio
import os
from textwrap import dedent

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google.gemini import Gemini
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder
from qdrant_client.http.models import VectorParams, Distance
from rich.console import Console
from rich.panel import Panel

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

devops_prompt = prompt_from_poml('devops.poml')

console = Console()

def execute_devops_agent(provider: str) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]DevOps Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))
    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id="gpt-4o", api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id="claude-sonnet-4-5-20250929", temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id="gemini-2.5-flash", temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id="gpt-5-mini"), #default

    devops_assist = Agent(
        name="DevOps Agent",
        model=model,
        description="You help answer questions about the devops domain like kubernetes troubleshooting, docker troubleshooting etc.",
        instructions=devops_prompt,
        additional_input=dedent("""\
        Instruction: You should always answer scenarios like below (few examples as below).
        - Debug high memory usage in Kubernetes pods causing frequent OOMKills and restarts
        - Analyze distributed tracing data to identify performance bottleneck in microservices architecture
        - Troubleshoot intermittent 504 gateway timeout errors in production load balancer
        - Investigate CI/CD pipeline failures and implement automated debugging workflows
        - Root cause analysis for database deadlocks causing application timeouts
        - Debug DNS resolution issues affecting service discovery in Kubernetes cluster
        - Analyze logs to identify security breach and implement containment procedures
        - Troubleshoot GitOps deployment failures and implement automated rollback procedures                                                                 
        """),
        stream_intermediate_steps=True,
        markdown=True,
    )

    return devops_assist