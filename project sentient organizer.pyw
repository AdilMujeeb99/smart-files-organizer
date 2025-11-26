import os
import shutil
import time
import threading
import logging # <--- NEW LIBRARY
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pystray
from PIL import Image, ImageDraw

# --- CONFIGURATION ---
source_dir = os.path.join(os.path.expanduser("~"), "Downloads")
log_file = "organizer_history.log" # The name of your log file

# --- SETUP LOGGING ---
# This tells Python: "Write everything to a file, and include the time."
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Also print to console (optional, helpful for debugging)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

file_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".heic", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".iso", ".msix"],
    "Code": [".py", ".java", ".js", ".html", ".css", ".cpp", ".json"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Calender Events": [".ics", ".ical", ".ifb"]
}

# --- CORE LOGIC ---
def is_file_ready(file_path):
    try:
        if not os.path.exists(file_path): return False
        os.rename(file_path, file_path)
        return True
    except OSError:
        return False

def folder_organization(file_path):
    if not os.path.exists(file_path): return
    
    filename = os.path.basename(file_path)
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    if extension in [".tmp", ".crdownload", ".part", ".ini", ".db"]: return 

    for category, extension_list in file_categories.items():
        if extension in extension_list:
            destination_folder = os.path.join(source_dir, category)
            if not os.path.exists(destination_folder): os.makedirs(destination_folder)
            
            destination_file_path = os.path.join(destination_folder, filename)

            if os.path.exists(destination_file_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(destination_file_path):
                    new_name = f"{base}_{counter}{ext}"
                    destination_file_path = os.path.join(destination_folder, new_name)
                    counter += 1
            
            try:
                shutil.move(file_path, destination_file_path)
                # CHANGE: Use logging instead of print
                logging.info(f"Moved: {filename} --> {category}")
            except Exception as e:
                logging.error(f"Error moving {filename}: {e}")
            break

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if file_path.endswith((".tmp", ".crdownload", ".part", ".ini")): return

            for _ in range(5):
                if is_file_ready(file_path):
                    folder_organization(file_path)
                    break
                time.sleep(1)

# --- SERVICE MANAGER ---
class ServiceManager:
    def __init__(self):
        self.observer = None
        self.is_running = False

    def start(self):
        if self.is_running: return
        logging.info("--- Service Starting ---")
        self.event_handler = MoverHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, source_dir, recursive=False)
        self.observer.start()
        self.is_running = True

    def stop(self):
        if not self.is_running: return
        logging.info("--- Service Stopping ---")
        self.observer.stop()
        self.observer.join()
        self.is_running = False

    def restart(self):
        logging.info("--- Service Restarting ---")
        self.stop()
        time.sleep(0.5)
        self.start()
    
    def run_startup_scan(self):
        logging.info("--- Running Manual Scan ---")
        try:
            for file in os.listdir(source_dir):
                full_path = os.path.join(source_dir, file)
                if os.path.isfile(full_path):
                    folder_organization(full_path)
            logging.info("--- Scan Complete ---")
        except Exception as e:
            logging.error(f"Scan Error: {e}")

    def open_log_file(self):
        # This opens the text file in Notepad (or your default editor)
        if os.path.exists(log_file):
            os.startfile(log_file)
        else:
            print("Log file does not exist yet.")

manager = ServiceManager()

# --- SYSTEM TRAY GUI ---

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
    elif str(item) == "View Logs": manager.open_log_file() # <--- NEW BUTTON
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
        pystray.MenuItem("View Logs", on_clicked), # <--- Add to menu
        pystray.MenuItem("Exit", on_clicked)
    )
    
    icon = pystray.Icon("Organizer", image, "Smart Organizer", menu)
    manager.start()
    icon.run()

if __name__ == "__main__":
    setup_tray()