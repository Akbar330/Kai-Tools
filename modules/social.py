import requests
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def username_search(username):
    """
    Teacher Note:
    Social Media Hunting (Identification) works by checking if a specific URL exists for a username.
    If the status code is 200, the account likely exists. If 404, it doesn't.
    """
    
    platforms = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "YouTube": "https://www.youtube.com/@{}",
        "TikTok": "https://www.tiktok.com/@{}"
    }
    
    console.print(f"\n[bold cyan]Searching for username:[/bold cyan] [yellow]{username}[/yellow]\n")
    
    results_table = Table(title=f"Social Media Scan for '{username}'", border_style="magenta")
    results_table.add_column("Platform", style="cyan")
    results_table.add_column("Status", style="white")
    results_table.add_column("Profile URL", style="blue")
    
    # We use track(...) for a nice progress bar
    for platform, url_mask in track(platforms.items(), description="Scanning..."):
        url = url_mask.format(username)
        try:
            # Most sites require a User-Agent to avoid being blocked
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                # Double check content sometimes needed, but status 200 is a good indicator
                results_table.add_row(platform, "[bold green]FOUND[/bold green]", url)
            else:
                results_table.add_row(platform, "[red]NOT FOUND[/red]", "—")
        except Exception as e:
            results_table.add_row(platform, f"[yellow]ERROR: {str(e)[:20]}...[/yellow]", "—")
            
    console.print(results_table)

if __name__ == "__main__":
    uname = input("Enter username: ")
    username_search(uname)
