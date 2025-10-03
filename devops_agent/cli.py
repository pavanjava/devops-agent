import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from devops_agent.core.devops_agent import execute_devops_agent

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """DevOps Agent - Your AI-powered DevOps assistant"""
    pass


def default_provider() -> str:
    return "openai"


@cli.command()
@click.option('--log-file', type=click.Path(exists=True), help='Path to log file to analyze')
@click.option('--provider', type=str, help='Configure the agent with one of the enterprise grade providers like OpenAI, Anthropic, Gemini')
@click.option('--query', type=str, help='Query to ask the DevOps agent')
@click.option('--output', type=click.Path(), help='Output file path (optional)')
@click.option('--format', type=click.Choice(['text', 'json', 'markdown']), default='text', help='Output format')
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
def run(log_file, provider, query, output, format, interactive):
    """Run the DevOps agent with specified options"""

    if not provider:
        console.print("[yellow]No provider specified, defaulting to openai[/yellow]")
        provider = default_provider()

    # Interactive mode
    if interactive:
        run_interactive_mode(provider, output, format)
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
        console.print("[green]✓[/green] Log analysis will be implemented here")

    if query:
        process_query(provider, query, output, format)


def run_interactive_mode(provider: str, output: str = None, format: str = 'text'):
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
                "[bold cyan]DevOps Agent[/bold cyan] [dim]Thinking...[/dim]",
                border_style="cyan"
            ))

            try:
                response = execute_devops_agent(provider=provider, user_query=user_input)
                console.print(f"\n[bold cyan]Assistant:[/bold cyan]\n{response}")

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


def process_query(provider: str, query: str, output: str = None, format: str = 'text'):
    """Process a single query"""
    console.print(f"[yellow]Processing query:[/yellow] {query}")
    console.print(Panel.fit(
        "[bold cyan]DevOps Agent[/bold cyan] [dim]Thinking...[/dim]",
        border_style="cyan"
    ))

    try:
        response = execute_devops_agent(provider=provider, user_query=query)
        console.print(f"\n[bold cyan]Assistant:[/bold cyan]\n{response}")

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
            f.write("\n" + "="*50 + "\n\n")
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