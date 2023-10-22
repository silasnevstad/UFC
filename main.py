from cmd.main import run_conversation
from rich.console import Console
from rich.table import Table
from rich.progress import track
from colorama import Fore, Style, init
import textwrap

console = Console()

def main():
    init(autoreset=True)
    console.print("Welcome to the Universal Fact-Checker!", style="green")

    while True:
        user_input = console.input("[yellow]Enter a claim to check (or type 'q' or 'quit' to quit):[/yellow] ").strip()
        if user_input.lower() in ['q', 'quit']:
            console.print("Goodbye!", style="green")
            break

        evaluation_results = []
        for result in track(run_conversation(user_input), description="[cyan]Evaluating input...[/cyan]"):
            evaluation_results.append(result)

        for result in evaluation_results:
            display_result(result)

def display_result(result):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Field")
    table.add_column("Value")

    wrapped_claim = textwrap.fill(str(result['claim']), width=50)
    wrapped_fixed_claim = textwrap.fill(str(result.get('fixedClaim', '')), width=50) if result.get('fixedClaim') else None
    wrapped_evaluation = textwrap.fill(str(result['evaluation']), width=50)
    wrapped_evidence = textwrap.fill(str(result['evidence']), width=50)

    table.add_row("Claim", wrapped_claim)
    if wrapped_fixed_claim:
        table.add_row("Fixed Claim", wrapped_fixed_claim)
    table.add_row("Topic", result['topic'])
    table.add_row("Genre", result['genre'])
    table.add_row("Evaluation", wrapped_evaluation)
    table.add_row("Evidence", wrapped_evidence)
    
    console.print(table)

if __name__ == "__main__":
    main()
