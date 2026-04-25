import os
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def change_mac():
    """
    Teacher Note:
    Changing the MAC address (MAC Spoofing) helps in anonymity and bypassing 
    MAC filters in some networks.
    Requires sudo on Linux.
    """
    console.print("\n[bold yellow][!][/bold yellow] MAC Changer requires [bold]sudo[/bold] and works on Linux.\n")
    interface = Prompt.ask("Enter interface (e.g., eth0, wlan0)")
    new_mac = Prompt.ask("Enter new MAC (e.g., 00:11:22:33:44:55)")
    
    console.print(f"[green][+][/green] Attempting to change {interface} to {new_mac}...")
    try:
        # Commands to change MAC
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac], check=True)
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
        console.print("[bold green][+][/bold green] MAC Address changed successfully!")
    except Exception as e:
        console.print(f"[red][!][/red] Error: {e}")

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            return port
        s.close()
    except:
        return None

def advanced_port_scan(target=None, start_port=1, end_port=1024):
    if not target:
        target = Prompt.ask("Enter target IP/Host")
        start_port = int(Prompt.ask("Start Port", default="1"))
        end_port = int(Prompt.ask("End Port", default="1024"))
    
    console.print(f"[cyan][+][/cyan] Scanning {target} from {start_port} to {end_port}...")
    
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            res = future.result()
            if res:
                open_ports.append(res)
                console.print(f"[green][+][/green] Port [bold]{res}[/bold] is OPEN")
                
    if not open_ports:
        console.print("[yellow][!][/yellow] No open ports found in that range.")

def network_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        console.print("[bold cyan]Network Security Tools[/bold cyan]\n")
        
        console.print("1. MAC Address Changer (Linux)")
        console.print("2. Advanced Port Scanner (Multi-threaded)")
        console.print("0. Back to Main Menu")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "0"], default="0")
        
        if choice == "1":
            change_mac()
            Prompt.ask("\nPress Enter to continue")
        elif choice == "2":
            advanced_port_scan()
            Prompt.ask("\nPress Enter to continue")
        elif choice == "0":
            break
