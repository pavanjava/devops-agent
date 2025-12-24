from agno.agent import Agent
from rich.console import Console
from rich.panel import Panel
from devops_agent.utils.model_provider import get_model

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

terraform_prompt = prompt_from_poml('terraform.poml')

console = Console()


def execute_terraform_agent(provider: str, model: str, debug_mode: bool = False, reasoning: bool = False) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]Terraform Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    model = get_model(provider=provider, model_str=model)

    terraform_assist = Agent(
        name="Terraform Agent",
        model=model,
        description="You help answer questions about the terraform technology with respect to platforms like Azure, AWS,"
                    " and GCP. Always ask the cloud provider if not provided in the user_query before proceeding.",
        instructions=terraform_prompt,
        stream_intermediate_steps=True,
        markdown=True,
        debug_mode=debug_mode,
        reasoning=reasoning
    )

    return terraform_assist
