from textwrap import dedent

from agno.agent import Agent
from rich.console import Console
from rich.panel import Panel
from devops_agent.utils.model_provider import get_model

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

db_sql_pro_prompt = prompt_from_poml('db_sql_pro.poml')

console = Console()


def execute_db_sql_pro_agent(provider: str, model: str, debug_mode: bool = False, reasoning: bool = False) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]Sql Pro Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    model = get_model(provider=provider, model_str=model)

    db_optmization_assist = Agent(
        name="Sql Pro Agent",
        model=model,
        description=dedent("""\
        You are Master modern SQL with cloud-native databases, OLTP/OLAP optimization, and advanced query techniques. 
        Expert in performance tuning, data modeling, and hybrid analytical systems. Use PROACTIVELY for database 
        optimization or complex analysis.\
        """),
        instructions=db_sql_pro_prompt,
        stream_intermediate_steps=True,
        markdown=True,
        debug_mode=debug_mode,
        reasoning=reasoning
    )

    return db_optmization_assist
