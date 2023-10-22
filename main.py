from cmd.main import run_conversation
from prettytable import PrettyTable
from colorama import Fore, Style, init

def main():
    init()  # Initialize colorama for Windows compatibility
    print(Fore.GREEN + "Welcome to the Universal Fact-Checker!" + Style.RESET_ALL)
    while True:
        user_input = input(Fore.YELLOW + "Enter a claim to check (or type 'exit' to quit): " + Style.RESET_ALL)
        if user_input.lower() == 'exit':
            print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
            break
        evaluation_results = run_conversation(user_input)
        for result in evaluation_results:
            table = PrettyTable()
            table.field_names = ["Field", "Value"]
            table.align["Field"] = "l"
            table.align["Value"] = "l"
            table.add_row(["Claim", result['claim']])
            table.add_row(["Topic", result['topic']])
            table.add_row(["Genre", result['genre']])
            table.add_row(["Evaluation", result['evaluation']])
            table.add_row(["Evidence", result['evidence']])
            print(table)
            print(Fore.CYAN + "-"*40 + Style.RESET_ALL)

if __name__ == "__main__":
    main()
