import requests
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def request_url(url, path):
    full_url = f"{url.rstrip('/')}/{path}"
    try:
        # We follow redirects but check the final status
        response = requests.get(full_url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            return (full_url, response.status_code, len(response.content))
        elif response.status_code in [403, 401]:
            return (full_url, response.status_code, "N/A (Hidden/Protected)")
        return None
    except:
        return None

def dir_fuzzer(target_url):
    """
    Teacher Note:
    Directory discovery/fuzzing is the process of guessing file names. 
    Hackers look for hidden gems like .env, config.php, /backup/ or /admin/
    """
    console.print(f"\n[bold cyan][+][/bold cyan] Fuzzing target: [yellow]{target_url}[/yellow]\n")
    
    # Default common wordlist
    common_paths = [
        "admin", "login", "config.php", ".env", ".git", "wp-admin", 
        "backup", "db.sql", "uploads", "api", "v1", "v2", "test", 
        "development", "README.md", "robots.txt", "sitemap.xml", ".htaccess"
    ]
    
    results_table = Table(title=f"Discovered Resources on {target_url}", border_style="green")
    results_table.add_column("Path", style="cyan")
    results_table.add_column("Status", style="bold white")
    results_table.add_column("Size/Info", style="dim")
    
    found_count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(request_url, target_url, path) for path in common_paths]
        for future in track(futures, description="Fuzzing directories..."):
            res = future.result()
            if res:
                url, status, size = res
                status_color = "green" if status == 200 else "yellow"
                results_table.add_row(url, f"[{status_color}]{status}[/{status_color}]", str(size))
                found_count += 1
                
    if found_count > 0:
        console.print(results_table)
    else:
        console.print("[yellow][!][/yellow] No common hidden directories found.")

if __name__ == "__main__":
    url = input("Enter Target URL (with http/https): ")
    dir_fuzzer(url)
