import os
from rich.console import Console
from rich.prompt import Prompt
from modules.web.fuzzer import dir_fuzzer
from modules.web.auditor import audit_website
from modules.web.vuln_scanner import web_vuln_checker

console = Console()

def web_pentest_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        console.print("[bold red]Web Pentesting & Auto-Scan Suite[/bold red]\n")
        
        console.print("1. Directory Discovery (Fuzzer/Buster)")
        console.print("2. Automated Security Audit (Headers & Risk)")
        console.print("3. Vulnerability Checker (XSS/SQLi Probe)")
        console.print("4. Full Web Scan (Auto-Penetration Test)")
        console.print("0. Back to Main Menu")
        
        choice = Prompt.ask("Select an action", choices=["1", "2", "3", "4", "0"], default="0")
        
        if choice == "1":
            target = Prompt.ask("Enter Target URL (e.g., https://example.com)")
            dir_fuzzer(target)
            Prompt.ask("\nScan complete. Press Enter to continue")
        elif choice == "2":
            target = Prompt.ask("Enter Target URL")
            audit_website(target)
            Prompt.ask("\nScan complete. Press Enter to continue")
        elif choice == "3":
            target = Prompt.ask("Enter Target URL (e.g., http://example.com/page.php)")
            web_vuln_checker(target)
            Prompt.ask("\nScan complete. Press Enter to continue")
        elif choice == "4":
            target = Prompt.ask("Enter Target URL")
            console.print("[bold yellow]Starting Full Automated Penetration Test...[/bold yellow]")
            audit_website(target)
            web_vuln_checker(target)
            dir_fuzzer(target)
            Prompt.ask("\nFull-Scale Scan complete. Press Enter to continue")
        elif choice == "0":
            break
