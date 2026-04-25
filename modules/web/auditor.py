import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def audit_website(url):
    """
    Teacher Note:
    Automated security audits check for common misconfigurations.
    Missing headers mean the browser doesn't have instructions to protect the user 
    against Clickjacking or XSS.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    console.print(f"\n[bold cyan][+][/bold cyan] Auditing Security Headers: [yellow]{url}[/yellow]\n")
    
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        table = Table(title="Security Header Audit", border_style="blue")
        table.add_column("Header", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Description/Risk", style="dim")
        
        # 1. HSTS
        hsts = headers.get('Strict-Transport-Security')
        table.add_row("HSTS", "FOUND" if hsts else "[bold red]MISSING[/bold red]", "Forces HTTPS usage.")
        
        # 2. X-Frame-Options
        xfo = headers.get('X-Frame-Options')
        table.add_row("X-Frame-Options", "FOUND" if xfo else "[bold red]MISSING[/bold red]", "Protects against Clickjacking.")
        
        # 3. CSP
        csp = headers.get('Content-Security-Policy')
        table.add_row("CSP", "FOUND" if csp else "[bold red]MISSING[/bold red]", "Strongest defense against XSS.")
        
        # 4. Server Version
        server = headers.get('Server')
        table.add_row("Server Info", f"[yellow]{server}[/yellow]" if server else "HIDDEN", "Exposing server version helps hackers.")
        
        console.print(table)
        
        # Summary
        if not xfo:
            console.print(Panel("[bold red]Vulnerability Detected:[/bold red] The site is vulnerable to [bold]Clickjacking[/bold] due to missing X-Frame-Options.", border_style="red"))
            
    except Exception as e:
        console.print(f"[red][!][/red] Audit failed: {e}")

if __name__ == "__main__":
    t = input("Enter website URL: ")
    audit_website(t)
