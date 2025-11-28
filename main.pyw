import os
import sys
import logging
import threading
import tkinter as tk
from tkinter import messagebox
import platform
import pystray
from PIL import Image, ImageDraw
import settings
from backend import ServiceManager

# --- SETUP LOGGING ---
logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

manager = ServiceManager()

# --- CRITICAL: HELPER FOR MAC APP BUNDLES ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- GUI FUNCTIONS ---
def create_fallback_icon():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((0, 0, width, height), fill=(34, 139, 34)) 
    dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image

# --- ABOUT POPUP LOGIC ---
def run_about_popup():
    root = tk.Tk()
    root.withdraw() 
    
    title = "About Smart Organizer"
    message = (
        "Smart Desktop Organizer v1.2\n"
        "Created by: Adil Mujeeb\n"
        "Github: AdilMujeeb99\n\n"
        "A background utility that automatically sorts your files."
    )
    
    messagebox.showinfo(title, message)
    root.destroy()

def show_about(icon=None, item=None):
    if platform.system() == "Darwin":
        run_about_popup()
    else:
        popup_thread = threading.Thread(target=run_about_popup, daemon=True)
        popup_thread.start()

# --- MENU CLICKS ---
def on_clicked(icon, item):
    if str(item) == "Start": manager.start()
    elif str(item) == "Stop": manager.stop()
    elif str(item) == "Restart": manager.restart()
    elif str(item) == "Scan Now": manager.run_startup_scan()
    elif str(item) == "View Logs": manager.open_log_file()
    elif str(item) == "About": show_about()
    elif str(item) == "Exit":
        manager.stop()
        icon.stop()

# --- TRAY SETUP ---
def setup_tray():
    # Use resource_path to find the icon inside the App Bundle
    icon_name = "app_icon.icns" 
    icon_path = resource_path(icon_name)
    
    if os.path.exists(icon_path):
        image = Image.open(icon_path)
    else:
        # Fallback logic
        alt_path = resource_path("app_icon.ico")
        if os.path.exists(alt_path):
            image = Image.open(alt_path)
        else:
            image = create_fallback_icon()

    menu = pystray.Menu(
        pystray.MenuItem("Smart Organizer", lambda icon, item: None, enabled=False),
        pystray.MenuItem("Start", on_clicked),
        pystray.MenuItem("Stop", on_clicked),
        pystray.MenuItem("Restart", on_clicked),
        pystray.MenuItem("Scan Now", on_clicked),
        pystray.MenuItem("View Logs", on_clicked),
        pystray.MenuItem("About", show_about),
        pystray.MenuItem("Exit", on_clicked)
    )
    
    icon = pystray.Icon("Organizer", image, "Smart Organizer", menu)
    manager.start()
    icon.run()

if __name__ == "__main__":
    setup_tray()