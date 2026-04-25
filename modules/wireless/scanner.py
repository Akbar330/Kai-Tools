import os
import subprocess
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def scan_networks():
    """
    Teacher Note:
    Scanning for networks allows us to identify targets, signal strength (proximity), 
    and security protocols (WPA2/WPA3).
    """
    console.print("\n[bold cyan][+][/bold cyan] Scanning for nearby WiFi networks via nmcli...\n")
    try:
        # Running nmcli with specific fields to handle spaces efficiently
        result = subprocess.check_output(["nmcli", "-f", "SSID,BSSID,BARS,SECURITY,CHAN,RATE", "dev", "wifi", "list"]).decode()
        
        table = Table(title="Wireless Security Analysis", border_style="magenta", show_lines=True)
        lines = result.strip().split('\n')
        
        if len(lines) <= 1:
            console.print("[yellow][!][/yellow] No networks found. Ensure WiFi is on.")
            return

        table.add_column("SSID", style="bold white")
        table.add_column("MAC (BSSID)", style="dim")
        table.add_column("Signal", style="green")
        table.add_column("Security Protocol", style="bold yellow")
        table.add_column("CH", style="cyan")
        table.add_column("Speed", style="blue")
            
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 6:
                # We show the security protocol clearly
                table.add_row(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
                
        console.print(table)
        console.print("\n[bold red][!][/bold red] [italic]Security Alert:[/italic] Jaringan tanpa enkripsi (WPA/WEP) sangat mudah disadap.")
    except Exception as e:
        console.print(f"[bold red][!][/bold red] Scan failed: {e}")
        console.print("[yellow]Note: Ensure nmcli is installed and you have permission to scan.[/yellow]")

def wifi_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        console.print("[bold cyan]Wireless Auditor[/bold cyan]\n")
        
        console.print("1. Scan Networks (SSID Discovery)")
        console.print("2. Check Interface Info")
        console.print("0. Back to Main Menu")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "0"], default="0")
        
        if choice == "1":
            scan_networks()
            Prompt.ask("\nPress Enter to continue")
        elif choice == "2":
            os.system("nmcli dev show")
            Prompt.ask("\nPress Enter to continue")
        elif choice == "0":
            break
