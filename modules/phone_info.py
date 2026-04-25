import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
from rich.console import Console
from rich.table import Table

console = Console()

def phone_lookup(phone_number):
    """
    Teacher Note:
    Phone OSINT helps identify the origin and legitimacy of a number.
    1. Geocoding: Finding the region/city.
    2. Carrier: Identifying the provider (useful for SIM swapping defense).
    3. Lat/Lon: We get this by 'geocoding' the location string.
    """
    console.print(f"\n[bold cyan]Analyzing Phone Number:[/bold cyan] [yellow]{phone_number}[/yellow]\n")
    
    try:
        # Parse the number (format: +628123...)
        parsed_number = phonenumbers.parse(phone_number)
        
        if not phonenumbers.is_valid_number(parsed_number):
            console.print("[bold red][!][/bold red] Invalid phone number format. Use E.164 format (e.g., +62...)")
            return

        # Basic Info
        location = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        info_table = Table(title="Phone Number Details", border_style="green")
        info_table.add_column("Field", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("Location (Region)", location)
        info_table.add_row("Carrier", service_provider)
        info_table.add_row("Timezones", str(time_zones))
        
        # Approximate Lat/Lon using OpenStreetMap (Free/Open)
        if location:
            console.print(f"[green][+][/green] Attempting to find approximate Lat/Lon for: [italic]{location}[/italic]...")
            try:
                # We use Nominatim (OpenStreetMap) to turn the location string into coordinates
                geo_resp = requests.get(f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1", headers={'User-Agent': 'GravityOSINT/1.0'}).json()
                if geo_resp:
                    lat = geo_resp[0].get('lat')
                    lon = geo_resp[0].get('lon')
                    info_table.add_row("Approx. Latitude", lat)
                    info_table.add_row("Approx. Longitude", lon)
                    info_table.add_row("Map Link", f"https://www.google.com/maps?q={lat},{lon}")
            except Exception as e:
                console.print(f"[yellow][!][/yellow] Could not fetch coordinates: {e}")

        console.print(info_table)
        
    except Exception as e:
        console.print(f"[bold red][!][/bold red] Error analyzing number: {e}")

if __name__ == "__main__":
    num = input("Enter phone number (+xxxx): ")
    phone_lookup(num)
