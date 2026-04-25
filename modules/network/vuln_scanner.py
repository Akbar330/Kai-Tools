import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def search_cve(service_name=None):
    if not service_name:
        service_name = Prompt.ask("Enter service name & version")
    
    """
    Teacher Note:
    Once we know a service name and version (e.g., Apache 2.4.49), we check for CVEs.
    CVE (Common Vulnerabilities and Exposures) is a list of publicly disclosed safety flaws.
    """
    console.print(f"\n[bold cyan][+][/bold cyan] Searching vulnerabilities for: [bold white]{service_name}[/bold white]...\n")
    
    try:
        search_url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={service_name.replace(' ', '+')}"
        table = Table(title=f"Vulnerability Intelligence: {service_name}", border_style="red")
        table.add_column("ID", style="cyan")
        table.add_column("Source", style="dim")
        table.add_column("Link", style="blue")
        
        table.add_row("Exploit-DB", "Offensive Security", f"https://www.exploit-db.com/search?q={service_name}")
        table.add_row("NVD Search", "NIST", f"https://nvd.nist.gov/vuln/search/results?query={service_name}")
        table.add_row("CVE Mitre", "Mitre Corp", search_url)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red][!][/red] CVE Search failed: {e}")
