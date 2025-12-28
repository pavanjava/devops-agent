from textwrap import dedent

from agno.agent import Agent
from devops_agent.utils.model_provider import get_model
from rich.console import Console
from rich.panel import Panel

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

devops_prompt = prompt_from_poml('devops.poml')

console = Console()

def execute_devops_agent(provider: str, model: str, debug_mode: bool = False, reasoning:bool=False) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]DevOps Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    model = get_model(provider=provider, model_str=model)

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
        debug_mode=debug_mode,
        reasoning=reasoning
    )

    return devops_assist