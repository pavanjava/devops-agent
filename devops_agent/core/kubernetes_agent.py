import os
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google.gemini import Gemini
from rich.console import Console
from rich.panel import Panel

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

k8s_prompt = prompt_from_poml('kubernetes.poml')

console = Console()

def execute_k8s_agent(provider: str, model:str, debug_mode: bool=False) -> Agent:

    console.print(Panel.fit(
        "[bold cyan]Kubernetes Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id=model, api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id=model, temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id=model, temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id="gpt-5-mini"),  # default

    k8s_assist = Agent(
        name="Kubernetes Agent",
        model=model,
        description="You help answer questions about the application with kubernetes design and implementation domain of"
                    " any infrastructure like Azure(AKS), AWS(EKS), and GCP(GKS)",
        instructions=k8s_prompt,
        additional_input=dedent("""\
        Instruction: You should always answer scenarios like below (few examples as below).
        - Design a multi-cluster Kubernetes platform with GitOps for a financial services company
        - Implement progressive delivery with Argo Rollouts and service mesh traffic splitting
        - Create a secure multi-tenant Kubernetes platform with namespace isolation and RBAC
        - Design disaster recovery for stateful applications across multiple Kubernetes clusters
        - Optimize Kubernetes costs while maintaining performance and availability SLAs
        - Implement observability stack with Prometheus, Grafana, and OpenTelemetry for microservices
        - Create CI/CD pipeline with GitOps for container applications with security scanning
        - Design Kubernetes operator for custom application lifecycle management
        """),
        stream_intermediate_steps=True,
        markdown=True,
        debug_mode=debug_mode
    )

    return k8s_assist
