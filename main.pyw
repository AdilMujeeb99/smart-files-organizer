import os
import logging
import pystray
from PIL import Image, ImageDraw
import settings
from backend import ServiceManager # <--- Import the class from backend

# --- SETUP LOGGING ---
logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize Manager
manager = ServiceManager()

# --- GUI FUNCTIONS ---
def create_fallback_icon():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((0, 0, width, height), fill=(34, 139, 34)) 
    dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image

def on_clicked(icon, item):
    if str(item) == "Start": manager.start()
    elif str(item) == "Stop": manager.stop()
    elif str(item) == "Restart": manager.restart()
    elif str(item) == "Scan Now": manager.run_startup_scan()
    elif str(item) == "View Logs": manager.open_log_file()
    elif str(item) == "Exit":
        manager.stop()
        icon.stop()

def setup_tray():
    icon_path = "app_icon.ico" 
    if os.path.exists(icon_path):
        image = Image.open(icon_path)
    else:
        image = create_fallback_icon()

    menu = pystray.Menu(
        pystray.MenuItem("Smart Organizer", lambda icon, item: None, enabled=False),
        pystray.MenuItem("Start", on_clicked),
        pystray.MenuItem("Stop", on_clicked),
        pystray.MenuItem("Restart", on_clicked),
        pystray.MenuItem("Scan Now", on_clicked),
        pystray.MenuItem("View Logs", on_clicked),
        pystray.MenuItem("Exit", on_clicked)
    )
    
    icon = pystray.Icon("Organizer", image, "Smart Organizer", menu)
    manager.start()
    icon.run()

if __name__ == "__main__":
    setup_tray()