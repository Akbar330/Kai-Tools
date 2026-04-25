import socket
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def discover_subdomains(domain):
    """
    Teacher Note:
    Subdomain Brute-forcing is the process of trying common names (like 'dev', 'staging', 'mail') 
    before the main domain to see if they resolve to an IP address.
    This helps find hidden infrastructure.
    """
    
    console.print(f"\n[bold cyan]Scanning for subdomains on:[/bold cyan] [yellow]{domain}[/yellow]\n")
    
    try:
        with open("subdomains.txt", "r") as f:
            subdomains = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        subdomains = ["www", "mail", "dev", "test", "staging", "api"]
    
    results_table = Table(title="Subdomain Scan Results", border_style="blue")
    results_table.add_column("Subdomain", style="cyan")
    results_table.add_column("Full Domain", style="white")
    results_table.add_column("IP Address", style="green")
    
    found_count = 0
    for sub in track(subdomains, description="Brute-forcing..."):
        full_domain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            results_table.add_row(sub, full_domain, ip)
            found_count += 1
        except Exception:
            # Domain doesn't exist
            continue
            
    if found_count > 0:
        console.print(results_table)
        console.print(f"\n[green][+][/green] Success: Found [bold]{found_count}[/bold] subdomains.")
    else:
        console.print("[yellow][!][/yellow] No subdomains found with the current wordlist.")

if __name__ == "__main__":
    target = input("Enter domain: ")
    discover_subdomains(target)
