import socket
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def ip_lookup(ip_or_host):
    """
    Teacher Note:
    1. Geolocation: We use a public API to map an IP to a physical location.
    2. Banner Grabbing: This is a technique used to gain information about a remote system and the services running on its open ports.
    """
    
    # Resolve host to IP if needed
    try:
        ip = socket.gethostbyname(ip_or_host)
        console.print(f"\n[bold cyan]Target IP:[/bold cyan] [yellow]{ip}[/yellow]\n")
    except Exception as e:
        console.print(f"[bold red][!][/bold red] Could not resolve host: {e}")
        return

    # 1. Geolocation
    console.print("[green][+][/green] Fetching Geolocation data...")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response['status'] == 'success':
            geo_table = Table(title="Geolocation Data", border_style="green")
            geo_table.add_column("Field", style="cyan")
            geo_table.add_column("Value", style="white")
            
            geo_table.add_row("Country", response.get('country'))
            geo_table.add_row("Region", response.get('regionName'))
            geo_table.add_row("City", response.get('city'))
            geo_table.add_row("ISP", response.get('isp'))
            geo_table.add_row("Lat/Lon", f"{response.get('lat')}, {response.get('lon')}")
            
            console.print(geo_table)
        else:
            console.print("[yellow][!][/yellow] API could not find IP details.")
    except Exception as e:
        console.print(f"[bold red][!][/bold red] Geolocation lookup failed: {e}")

    # 2. Basic Banner Grabbing (Ports 80, 443, 21, 22)
    console.print("\n[green][+][/green] Attempting Banner Grabbing on common ports...")
    ports = [21, 22, 80, 443]
    banner_table = Table(title="Service Banners", border_style="yellow")
    banner_table.add_column("Port", style="cyan")
    banner_table.add_column("Status", style="white")
    banner_table.add_column("Banner", style="white")

    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((ip, port))
            # Try to get banner
            if port == 80:
                s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip_or_host.encode() + b"\r\n\r\n")
            
            banner = s.recv(1024).decode().strip()
            banner_table.add_row(str(port), "OPEN", banner[:50] + "..." if len(banner) > 50 else banner)
            s.close()
        except Exception:
            banner_table.add_row(str(port), "CLOSED/FILTERED", "N/A")
            
    console.print(banner_table)

if __name__ == "__main__":
    target = input("Enter IP or Hostname: ")
    ip_lookup(target)
