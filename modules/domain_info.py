import whois
import dns.resolver
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def domain_lookup(domain):
    """
    Teacher Note: 
    Domain lookup consists of two main parts:
    1. WHOIS: Tells us who owns the domain and when it expires.
    2. DNS: Tells us where the traffic goes (A for IP, MX for email, etc).
    """
    console.print(f"\n[bold cyan]Analyzing Domain:[/bold cyan] [yellow]{domain}[/yellow]\n")
    
    # 1. WHOIS Info
    try:
        console.print("[green][+][/green] Fetching WHOIS data...")
        w = whois.whois(domain)
        
        whois_table = Table(title="WHOIS Information", border_style="magenta")
        whois_table.add_column("Field", style="cyan")
        whois_table.add_column("Value", style="white")
        
        whois_table.add_row("Registrar", str(w.registrar))
        whois_table.add_row("Creation Date", str(w.creation_date))
        whois_table.add_row("Expiry Date", str(w.expiration_date))
        whois_table.add_row("Name Servers", str(w.name_servers))
        
        console.print(whois_table)
    except Exception as e:
        console.print(f"[bold red][!][/bold red] WHOIS lookup failed: {e}")

    # 2. DNS Info
    record_types = ['A', 'MX', 'NS', 'TXT']
    dns_table = Table(title="DNS Records", border_style="blue")
    dns_table.add_column("Type", style="cyan")
    dns_table.add_column("Value", style="white")
    
    console.print("\n[green][+][/green] Querying DNS records...")
    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            for rdata in answers:
                dns_table.add_row(record, str(rdata))
        except Exception:
            # Skip if record type doesn't exist
            continue
            
    if dns_table.row_count > 0:
        console.print(dns_table)
    else:
        console.print("[yellow]No DNS records found.[/yellow]")

if __name__ == "__main__":
    # Test script independently
    d = input("Enter domain: ")
    domain_lookup(d)
