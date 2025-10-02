import click
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """DevOps Agent - Your AI-powered DevOps assistant"""
    pass

@cli.command()
@click.option('--log-file', type=click.Path(exists=True), help='Path to log file to analyze')
@click.option('--query', type=str, help='Query to ask the DevOps agent')
@click.option('--output', type=click.Path(), help='Output file path (optional)')
@click.option('--format', type=click.Choice(['text', 'json', 'markdown']), default='text', help='Output format')
def run(log_file, query, output, format):
    """Run the DevOps agent with specified options"""

    if not log_file and not query:
        console.print("[red]Error: You must provide either --log-file or --query[/red]")
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
        console.print(f"[yellow]Processing query:[/yellow] {query}")


    if output:
        console.print(f"[blue]Output will be saved to:[/blue] {output}")

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