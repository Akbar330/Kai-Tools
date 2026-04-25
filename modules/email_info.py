import dns.resolver
from rich.console import Console
from rich.table import Table
import requests

console = Console()

def email_lookup(email):
    """
    Teacher Note:
    Email OSINT helps verify if an email address is valid and if it's leaked.
    1. MX Records: Tells us if the domain actually handles emails.
    2. Breach Check: We can use APIs to see if the email has been pwned.
    """
    console.print(f"\n[bold cyan]Analyzing Email:[/bold cyan] [yellow]{email}[/yellow]\n")
    
    try:
        domain = email.split('@')[1]
    except IndexError:
        console.print("[bold red][!][/bold red] Invalid email format.")
        return

    # 1. MX Record Check
    console.print(f"[green][+][/green] Checking MX records for domain: [italic]{domain}[/italic]")
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx_table = Table(title=f"MX Records for {domain}", border_style="blue")
        mx_table.add_column("Priority", style="cyan")
        mx_table.add_column("Mail Server", style="white")
        
        for rdata in answers:
            mx_table.add_row(str(rdata.preference), str(rdata.exchange))
        
        console.print(mx_table)
    except Exception as e:
        console.print(f"[yellow][!][/yellow] No MX records found or lookup failed: {e}")

    # 2. Breach Info (Educational)
    console.print("\n[green][+][/green] [bold]Breach Check Insight:[/bold]")
    console.print("   In a real-world scenario, you would use an API like [bold]Have I Been Pwned[/bold].")
    console.print("   Due to API key requirements, I recommend manually checking:")
    console.print(f"   [blue]https://haveibeenpwned.com/unifiedsearch/{email}[/blue]")
    
    # Simple check for common disposable email providers
    disposable_providers = ['yopmail.com', 'temp-mail.org', '10minutemail.com', 'guerrillamail.com']
    if domain in disposable_providers:
        console.print("\n[bold red][!][/bold red] This is a [bold]Disposable/Temporary[/bold] email provider.")
    else:
        console.print("\n[green][+][/green] Domain appears to be a standard provider.")

if __name__ == "__main__":
    em = input("Enter email: ")
    email_lookup(em)
