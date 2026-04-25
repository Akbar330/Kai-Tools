import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def get_geotagging(exif):
    if not exif:
        return None
    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                return None
            for (t, val) in GPSTAGS.items():
                if t in exif[idx]:
                    geotagging[val] = exif[idx][t]
    return geotagging

def extract_metadata(image_path):
    """
    Teacher Note:
    Exif (Exchangeable Image File Format) is data embedded in photos. 
    It can reveal where a person is (GPS), what device they used, and when the photo was taken.
    """
    if not os.path.exists(image_path):
        console.print(f"[red][!][/red] File not found: {image_path}")
        return

    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        table = Table(title=f"Metadata Analysis: {os.path.basename(image_path)}", border_style="cyan")
        table.add_column("Tag", style="bold white")
        table.add_column("Value", style="yellow")
        
        if not exif_data:
            console.print("[yellow][!][/yellow] No Exif metadata found in this image.")
            return

        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                continue
            table.add_row(str(tag_name), str(value)[:50])
            
        console.print(table)
        
        # Pulling GPS Data
        gps_data = get_geotagging(exif_data)
        if gps_data:
            console.print("\n[bold green][+][/bold green] [bold]GPS Coordinates Found![/bold]")
            lat = gps_data.get('GPSLatitude')
            lon = gps_data.get('GPSLongitude')
            if lat and lon:
                # Simple conversion to decimal (approximate)
                lat_deg = float(lat[0]) + float(lat[1])/60 + float(lat[2])/3600
                lon_deg = float(lon[0]) + float(lon[1])/60 + float(lon[2])/3600
                console.print(f"   Latitude: {lat_deg}")
                console.print(f"   Longitude: {lon_deg}")
                console.print(f"   [blue]Google Maps Link: https://www.google.com/maps?q={lat_deg},{lon_deg}[/blue]")
        
    except Exception as e:
        console.print(f"[red][!][/red] Metadata extraction failed: {e}")

if __name__ == "__main__":
    p = input("Enter path to image: ")
    extract_metadata(p)
