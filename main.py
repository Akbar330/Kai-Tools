import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table

# Placeholder for future imports
# from osint_menu import osint_main_menu
# from modules.wireless.scanner import wifi_scan_menu
# from modules.crypto.cracker import crypto_menu

console = Console()

def display_main_banner():
    banner = r"""
 [bold cyan]
  ____  __.         .__   ___________           .__          
 |    |/ _|  _____  |__|  \__    ___/___   ____ |  |   ______
 |      <   \__  \ |  |    |    | /  _ \ /  _ \|  |  /  ___/
 |    |  \   / __ \|  |    |    |(  <_> |  <_> )  |__\___ \ 
 |____|__ \ (____  /__|    |____| \____/ \____/|____/____  >
         \/      \/                                      \/ 
 [/bold cyan]
 [bold magenta]Kai Tools v3.0 - The Ultimate Security Suite[/bold magenta]
 [italic white]Be Kind, Be Ethical, Be Infinite[/italic white]
    """
    console.print(Panel(Text.from_markup(banner), border_style="bold blue"))

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_main_banner()
        
        table = Table(title="Select a Tool Category", show_header=True, header_style="bold green")
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Category", style="bold white")
        table.add_column("Tools Included")
        
        table.add_row("1", "OSINT Suite", "Domain, IP, Phone, Email, Social Search")
        table.add_row("2", "Wireless Auditor", "WiFi Scanning, Security Analysis")
        table.add_row("3", "Network Security", "Port Scanning, MAC Changer, Vuln Search")
        table.add_row("4", "Cryptographic Tools", "Hash Cracker, Hash Identifier")
        table.add_row("5", "Web Pentesting", "Auto-Scan, Fuzzing, Header Audit")
        table.add_row("6", "Exploitation Lab", "Reverse Shell Payload Generator")
        table.add_row("0", "Exit", "Close the suite")
        
        console.print(table)
        
        choice = Prompt.ask("Enter Category ID", choices=["1", "2", "3", "4", "5", "6", "0"], default="0")
        
        if choice == "1":
            # Direct call to the existing OSINT logic (which we'll adapt slightly)
            import osint_menu
            osint_menu.main_menu()
        elif choice == "2":
            from modules.wireless.scanner import wifi_menu
            wifi_menu()
        elif choice == "3":
            from modules.network.tools import network_menu
            network_menu()
        elif choice == "4":
            from modules.crypto.tools import crypto_menu
            crypto_menu()
        elif choice == "5":
            from modules.web.menu import web_pentest_menu
            web_pentest_menu()
        elif choice == "6":
            from modules.exploitation.payloads import generate_payloads
            generate_payloads()
            Prompt.ask("\nPress Enter to return to main menu")
        elif choice == "0":
            console.print("[bold red]Shutting down systems... Goodbye![/bold red]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupt received. Exiting GravityTools...[/bold red]")
        sys.exit(0)
    except ModuleNotFoundError as e:
        console.print(f"[bold red]Fatal Error:[/bold red] {e}")
        console.print("[yellow]Hint: Ensure you are running in the virtual environment (source venv/bin/activate)[/yellow]")
