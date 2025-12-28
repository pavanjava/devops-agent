from textwrap import dedent

from agno.agent import Agent
from rich.console import Console
from rich.panel import Panel
from devops_agent.utils.model_provider import get_model

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

db_architect_prompt = prompt_from_poml('db_architect.poml')

console = Console()


def execute_db_architect_agent(provider: str, model: str, debug_mode: bool = False, reasoning: bool = False) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]DB Architect Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    model = get_model(provider=provider, model_str=model)

    db_optmization_assist = Agent(
        name="DB Architect Agent",
        model=model,
        description=dedent("""\
        You are Expert database architect specializing in data layer design from scratch, technology selection, schema modeling,
        and scalable database architectures. Masters SQL/NoSQL/TimeSeries database selection, normalization strategies,
        migration planning, and performance-first design. Handles both greenfield architectures and re-architecture of
        existing systems. Use PROACTIVELY for database architecture, technology selection, or data modeling decisions.\
        """),
        instructions=db_architect_prompt,
        stream_intermediate_steps=True,
        markdown=True,
        debug_mode=debug_mode,
        reasoning=reasoning
    )

    return db_optmization_assist
