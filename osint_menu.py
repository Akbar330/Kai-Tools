import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, IntPrompt
from rich.table import Table

# Import modules
from modules.domain_info import domain_lookup
from modules.ip_info import ip_lookup
from modules.social import username_search
from modules.subdomains import discover_subdomains
from modules.phone_info import phone_lookup
from modules.email_info import email_lookup
from modules.metadata import extract_metadata

console = Console()

def display_banner():
    banner = r"""
  [bold cyan]
  ____  __.         .__   ________    _________ .___  _______  ___________ 
 |    |/ _|  _____  |__|  \_____  \  /   _____/ |   | \      \ \__    ___/ 
 |      <   \__  \ |  |   /   |   \ \_____  \  |   | /   |   \  |    |    
 |    |  \   / __ \|  |  /    |    \/        \ |   |/    |    \ |    |    
 |____|__ \ (____  /__|  \_______  /_______  / |___|\____|__  / |____|    
         \/      \/              \/        \/               \/          
  [/bold cyan]
  [bold magenta]Kai OSINT - Ethical Hacking Intelligence Suite[/bold magenta]
  [italic yellow]Gather Intelligence. Stay Ethical.[/italic yellow]
    """
    console.print(Panel(Text.from_markup(banner), border_style="blue"))

def main_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_banner()
        
        table = Table(title="OSINT Modules", show_header=True, header_style="bold green")
        table.add_column("No", justify="center")
        table.add_column("Module Name")
        table.add_column("Description")
        
        table.add_row("1", "Domain Info", "WHOIS, DNS Records, IP Info")
        table.add_row("2", "Network Lookup", "IP Geolocation & Banner Grabbing")
        table.add_row("3", "Subdomain Discovery", "Search for hidden subdomains")
        table.add_row("4", "Social Finder", "Check username existence on platforms")
        table.add_row("5", "Phone Info", "Location (Lat/Lon) & Carrier info")
        table.add_row("6", "Email Info", "Breach check and MX records")
        table.add_row("7", "Image Metadata", "Exif, GPS, Device info from photos")
        table.add_row("0", "Exit", "Close the tool")
        
        console.print(table)
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7", "0"], default="0")
        
        if choice == "1":
            target = Prompt.ask("Enter domain to analyze (e.g., google.com)")
            domain_lookup(target)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "2":
            target = Prompt.ask("Enter IP or Hostname")
            ip_lookup(target)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "3":
            target = Prompt.ask("Enter domain to scan subdomains (e.g., example.com)")
            discover_subdomains(target)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "4":
            target = Prompt.ask("Enter username to search")
            username_search(target)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "5":
            target = Prompt.ask("Enter phone number (e.g., +62xxxxxx)")
            phone_lookup(target)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "6":
            target = Prompt.ask("Enter email address")
            email_lookup(target)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "7":
            target = Prompt.ask("Enter path to image (e.g., photo.jpg)")
            extract_metadata(target)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "0":
            console.print("[bold red]Exiting... Keep learning![/bold red]")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]Shutdown signal received. Exiting...[/bold red]")
        sys.exit(0)
