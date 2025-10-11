import os
from pathlib import Path

from agno.agent import Agent
from agno.media import File
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google.gemini import Gemini
from rich.console import Console
from rich.panel import Panel

console = Console()

def execute_log_analysis_agent(provider: str, log_file: Path) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]Log Analysis Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))
    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id="gtp-4o", api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id="claude-sonnet-4-5-20250929", temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id="gemini-2.5-flash", temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id="gpt-5-mini"), #default

    file_analysis_agent = Agent(
        name="LogFile Analysis Agent",
        role="Analyze log files",
        model=model,
        description="You are an AI agent that can analyze log files.",
        instructions=[
            "You are an AI agent that can analyze log files.",
            "You are given a log file and you need to analyse and give detailed answer to the question from the user.",
        ],
    )

    print("executing the log analysis")
    user_query = 'analyse and give all the insights such as critical errors, patterns, anomalies, or any other significant findings'
    response = file_analysis_agent.run(user_query, files=[File(filepath=log_file)])

    return response.content