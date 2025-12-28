from pathlib import Path
import os

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from devops_agent.core.master_agent import execute_master_agent
from devops_agent.loganalytics.log_analysis_agent import execute_log_analysis_agent

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """DevOps Agent - Your AI-powered DevOps assistant"""
    pass


def default_provider() -> str:
    """Automatically detect which LLM provider to use based on available API keys."""
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    elif os.environ.get("GEMINI_API_KEY"):
        return "google"
    elif os.environ.get("OLLAMA_API_KEY"):
        return "ollama"
    elif os.environ.get("VLLM_API_KEY"):
        return "vllm"
    else:
        # If nothing found, fallback and warn
        console.print("[bold yellow]⚠️  No API key found. Defaulting to OpenAI (if set later).[/bold yellow]")
        return "openai"


def default_model() -> str:
    return "gpt-4o"


@cli.command()
@click.option('--log-file', type=click.Path(exists=True), help='Path to log file to analyze')
@click.option('--provider', type=str,
              help='Configure the agent with one of the enterprise grade providers like OpenAI, Anthropic, Gemini')
@click.option('--model', type=str,
              help='Configure the model name in accordance with the provider selected like gpt-4o, gemini-flash-2.5, etc.')
@click.option('--query', type=str, help='Query to ask the DevOps agent')
@click.option('--output', type=click.Path(), help='Output file path for saving responses')
@click.option('--format', type=click.Choice(['text', 'json', 'markdown']), default='text', help='Output format')
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
@click.option('--debug_mode', type=bool, help='Run all agents in debug mode, don\'t use in production')
@click.option('--reasoning_enabled', type=bool, help='Run all agents in debug mode, don\'t use in production')
def run(log_file, provider, model, query, output, format, interactive, debug_mode, reasoning_enabled):
    """Run the DevOps agent with specified options"""

    if not provider:
        console.print("[yellow]No provider specified[/yellow]")
        provider = default_provider()

    if not model:
        console.print("[yellow]No model specified, defaulting to gpt-4o[/yellow]")
        provider = default_model()

        # Interactive mode
    if interactive:
        run_interactive_mode(provider, model, output, format, debug_mode, reasoning_enabled)
        return

    # Single query mode (original behavior)
    if not log_file and not query:
        console.print("[red]Error: You must provide either --log-file, --query, or use --interactive mode[/red]")
        raise click.Abort()

    if log_file and query:
        console.print("[red]Error: Cannot use both --log-file and --query simultaneously[/red]")
        raise click.Abort()

    console.print(Panel.fit(
        "[bold cyan]DevOps Agent[/bold cyan]\n[dim]Initializing...[/dim]",
        border_style="cyan"
    ))

    if log_file:
        console.print(f"[yellow]Analyzing log file:[/yellow] {log_file}")
        try:
            file_path = Path(__file__).parent.joinpath(log_file)
            response = execute_log_analysis_agent(provider=provider, model=model, log_file=file_path,
                                                  debug_mode=debug_mode, reasoning=reasoning_enabled)
            console.print(Panel.fit(
                f"[bold yellow]Assistant:[/bold yellow] [dim]{response}[/dim]",
                border_style="yellow"
            ))

            if output:
                save_to_file(output, query, response, format)
                console.print(f"\n[dim]Response saved to {output}[/dim]")

        except Exception as e:
            console.print(f"\n[red]Error:[/red] {str(e)}")

    if query:
        process_query(provider, query, output, format, debug_mode, reasoning_enabled)


def run_interactive_mode(provider: str, model: str, output: str = None, format: str = 'text',
                         debug_mode: bool = False, reasoning_enabled: bool = False):
    """Run the agent in interactive mode with continuous conversation"""

    console.print(Panel.fit(
        "[bold cyan]DevOps Agent - Interactive Mode[/bold cyan]\n"
        "[dim]Type your questions or commands.[/dim]\n"
        "[dim]Type 'quit', 'exit', or 'bye' to exit.[/dim]",
        border_style="cyan"
    ))

    # Main interactive loop
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold green]You[/bold green]")

            # Check for exit commands
            if user_input.lower().strip() in ['quit', 'exit', 'bye', 'q']:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break

            # Skip empty inputs
            if not user_input.strip():
                continue

            # Process the query
            console.print(Panel.fit(
                "[bold cyan]DevOps Team[/bold cyan] [dim]Thinking...[/dim]",
                border_style="cyan"
            ))

            try:
                response = execute_master_agent(provider=provider, model_str=model, user_query=user_input,
                                                debug_mode=debug_mode, reasoning=reasoning_enabled)
                console.print(Panel.fit(
                    f"[bold yellow]Assistant:[/bold yellow] [dim]{response}[/dim]",
                    border_style="yellow"
                ))

                # Save to output file if specified
                if output:
                    save_to_file(output, user_input, response, format)
                    console.print(f"\n[dim]Response saved to {output}[/dim]")

            except Exception as e:
                console.print(f"\n[red]Error processing query:[/red] {str(e)}")

        except KeyboardInterrupt:
            console.print("\n\n[yellow]Interrupted. Type 'quit' to exit or continue with your next question.[/yellow]")
            continue
        except EOFError:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break


def process_query(provider: str, model: str, query: str, output: str = None, format: str = 'text',
                  debug_mode: bool = False, reasoning_enabled: bool = False):
    """Process a single query"""
    console.print(f"[yellow]Processing query:[/yellow] {query}")
    console.print(Panel.fit(
        "[bold cyan]DevOps Agent[/bold cyan] [dim]Thinking...[/dim]",
        border_style="cyan"
    ))

    try:
        response = execute_master_agent(provider=provider, model_str=model, user_query=query,
                                        debug_mode=debug_mode, reasoning=reasoning_enabled)
        console.print(Panel.fit(
            f"[bold yellow]Assistant:[/bold yellow] [dim]{response}[/dim]",
            border_style="yellow"
        ))

        if output:
            save_to_file(output, query, response, format)
            console.print(f"\n[dim]Response saved to {output}[/dim]")

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")


def save_to_file(filepath: str, query: str, response: str, format: str):
    """Save the conversation to a file"""
    import json
    from pathlib import Path

    output_path = Path(filepath)

    if format == 'json':
        content = json.dumps({
            "query": query,
            "response": response
        }, indent=2)
    elif format == 'markdown':
        content = f"# Query\n\n{query}\n\n# Response\n\n{response}\n"
    else:  # text
        content = f"Query: {query}\n\nResponse: {response}\n"

    # Append mode for interactive sessions
    mode = 'a' if output_path.exists() else 'w'
    with open(output_path, mode) as f:
        if mode == 'a':
            f.write("\n" + "=" * 50 + "\n\n")
        f.write(content)


@cli.command()
def config():
    """Configure the DevOps agent"""
    console.print("[yellow]Configuration interface will be implemented here[/yellow]")


@cli.command()
@click.argument('template_type', type=click.Choice(['terraform', 'kubernetes', 'docker']))
def template(template_type):
    """Generate templates for various DevOps tools"""
    console.print(f"[yellow]Generating {template_type} template...[/yellow]")


def main():
    cli()


if __name__ == '__main__':
    main()
