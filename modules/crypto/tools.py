import hashlib
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

console = Console()

def identify_hash(hash_str):
    """
    Teacher Note:
    Different algorithms produce different length hashes.
    MD5: 32 chars
    SHA1: 40 chars
    SHA256: 64 chars
    """
    length = len(hash_str)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    else:
        return "Unknown"

def hash_cracker(target_hash=None, wordlist_path=None):
    if not target_hash:
        console.print("\n[bold cyan]Hash Dictionary Cracker[/bold cyan]")
        target_hash = Prompt.ask("Enter the hash to crack").strip().lower()
        wordlist_path = Prompt.ask("Enter path to wordlist (or press Enter for default 'passwords.txt')")
    
    hash_type = identify_hash(target_hash)
    
    console.print(f"[yellow][!][/yellow] Identified possible type: [bold]{hash_type}[/bold]")
    
    wordlist_path = Prompt.ask("Enter path to wordlist (or press Enter for default 'passwords.txt')")
    if not wordlist_path:
        wordlist_path = "passwords.txt"
        if not os.path.exists(wordlist_path):
            with open(wordlist_path, "w") as f:
                f.write("password\n123456\nadmin\nqwerty\npassword123\n")
            console.print("[green][+][/green] Created default wordlist 'passwords.txt'")

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            passwords = f.readlines()
        
        found = False
        for password in track(passwords, description="Cracking..."):
            password = password.strip()
            # Generate hash for the candidate
            if hash_type == "MD5":
                guess = hashlib.md5(password.encode()).hexdigest()
            elif hash_type == "SHA1":
                guess = hashlib.sha1(password.encode()).hexdigest()
            elif hash_type == "SHA256":
                guess = hashlib.sha256(password.encode()).hexdigest()
            else:
                console.print("[red][!][/red] Unsupported hash type for auto-cracking.")
                return

            if guess == target_hash:
                console.print(f"\n[bold green][+][/bold green] MATCH FOUND: [bold white]{password}[/bold white]")
                found = True
                break
        
        if not found:
            console.print("\n[red][!][/red] Hash not found in wordlist.")
            
    except Exception as e:
        console.print(f"[red][!][/red] Error: {e}")

def crypto_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        console.print("[bold magenta]Cryptographic Suite[/bold magenta]\n")
        
        console.print("1. Identify Hash Type")
        console.print("2. Hash Dictionary Cracker")
        console.print("0. Back to Main Menu")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "0"], default="0")
        
        if choice == "1":
            h = Prompt.ask("Enter hash")
            console.print(f"Probable Type: [bold green]{identify_hash(h)}[/bold green]")
            Prompt.ask("\nPress Enter to continue")
        elif choice == "2":
            hash_cracker()
            Prompt.ask("\nPress Enter to continue")
        elif choice == "0":
            break
