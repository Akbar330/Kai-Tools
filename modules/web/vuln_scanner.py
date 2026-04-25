import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def test_xss(url):
    """
    Teacher Note:
    XSS (Cross-Site Scripting) happens when a website displays user input without cleaning it.
    We test this by injecting a probe like '<script>alert(1)</script>' and checking if it shows up in the source.
    """
    xss_payload = "<script>alert('GravityOSINT')</script>"
    # We assume 'id' or 'q' are common parameters to test
    test_params = ['q', 'id', 'search', 'query', 'name']
    
    console.print(f"\n[bold yellow][*][/bold yellow] Testing for basic XSS reflections on common parameters...")
    
    found = False
    for param in test_params:
        try:
            full_url = f"{url}?{param}={xss_payload}"
            response = requests.get(full_url, timeout=5)
            if xss_payload in response.text:
                console.print(f"[bold red][+][/bold red] [bold]Potential XSS Found![/bold] Parameter: [cyan]{param}[/cyan] reflects data without sanitization.")
                found = True
        except:
            continue
            
    if not found:
        console.print("[green][+][/green] No simple XSS reflections found in common parameters.")

def test_sqli(url):
    """
    Teacher Note:
    SQL Injection happens when a database query is manipulated via input.
    A common test is adding a single quote (') to see if the server triggers a database error.
    """
    sqli_payload = "'"
    test_params = ['id', 'item', 'cat', 'product']
    
    sql_errors = [
        "sql syntax", "mysql_fetch", "ora-", "postgre", "sqlite3", "unclosed quotation mark"
    ]
    
    console.print(f"\n[bold yellow][*][/bold yellow] Testing for SQL Injection error patterns...")
    
    found = False
    for param in test_params:
        try:
            full_url = f"{url}?{param}={sqli_payload}"
            response = requests.get(full_url, timeout=5)
            for error in sql_errors:
                if error.lower() in response.text.lower():
                    console.print(f"[bold red][+][/bold red] [bold]Potential SQLi Found![/bold] Parameter: [cyan]{param}[/cyan] triggered a database error.")
                    found = True
                    break
        except:
            continue
            
    if not found:
        console.print("[green][+][/green] No database error patterns detected during simple probe.")

def web_vuln_checker(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    test_xss(url)
    test_sqli(url)

if __name__ == "__main__":
    u = input("Enter target URL (e.g., http://testphp.vulnweb.com/listproducts.php): ")
    web_vuln_checker(u)
