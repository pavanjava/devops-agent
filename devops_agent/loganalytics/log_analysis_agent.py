import os
from pathlib import Path

from agno.agent import Agent
from agno.media import File
from agno.tools.mcp import MultiMCPTools

from devops_agent.utils.model_provider import get_model
from rich.console import Console
from rich.panel import Panel

console = Console()

async def execute_log_analysis_agent(provider: str, model: str, log_file: Path, debug_mode: bool= False,
                               reasoning:bool=False, filesystem_paths:str=None) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]Log Analysis Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    model = get_model(provider=provider, model_str=model)

    # Initialize and connect to multiple MCP servers
    mcp_tools = MultiMCPTools(
        commands=[
            f"npx -y @modelcontextprotocol/server-filesystem {filesystem_paths}",
        ],
    )

    await mcp_tools.connect()

    file_analysis_agent = Agent(
        name="LogFile Analysis Agent",
        role="Analyze log files",
        tools=[mcp_tools],
        model=model,
        description="You are an AI agent that can analyze log files.",
        instructions=[
            "You are an AI agent that can analyze log files.",
            "You are given a log file and you need to analyse and give detailed answer to the question from the user.",
        ],
        debug_mode=debug_mode,
        reasoning=reasoning
    )

    print("executing the log analysis")
    user_query = ('analyse and give all the insights such as critical errors, patterns, anomalies, or any other '
                  'significant findings')
    response = file_analysis_agent.run(user_query, files=[File(filepath=log_file)])

    return response.content