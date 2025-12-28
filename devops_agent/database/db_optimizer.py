from textwrap import dedent

from agno.agent import Agent
from rich.console import Console
from rich.panel import Panel
from devops_agent.utils.model_provider import get_model

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

db_optimization_prompt = prompt_from_poml('db_optimizer.poml')

console = Console()


def execute_db_optimization_agent(provider: str, model: str, debug_mode: bool = False, reasoning: bool = False) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]DB Optimization Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    model = get_model(provider=provider, model_str=model)

    db_optmization_assist = Agent(
        name="DB Optimization  Agent",
        model=model,
        description=dedent("""\
        You are Expert database optimizer with comprehensive knowledge of modern database performance tuning, query optimization
        , and scalable architecture design. Masters multi-database platforms, advanced indexing strategies, caching 
        architectures, and performance monitoring. Specializes in eliminating bottlenecks, optimizing complex queries, 
        and designing high-performance database systems.\
        """),
        instructions=db_optimization_prompt,
        stream_intermediate_steps=True,
        markdown=True,
        debug_mode=debug_mode,
        reasoning=reasoning
    )

    return db_optmization_assist
