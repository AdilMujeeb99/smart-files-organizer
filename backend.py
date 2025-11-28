import os
import shutil
import time
import logging
import subprocess # <--- NEW: To run Mac commands
import platform   # <--- NEW: To check OS
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import settings 

# --- HELPER FUNCTIONS ---
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

    if extension in settings.TEMP_EXTENSIONS: return 

    for category, extension_list in settings.FILE_CATEGORIES.items():
        if extension in extension_list:
            destination_folder = os.path.join(settings.SOURCE_DIR, category)
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
                logging.info(f"Moved: {filename} --> {category}")
            except Exception as e:
                logging.error(f"Error moving {filename}: {e}")
            break

# --- WATCHDOG CLASSES ---
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if file_path.endswith(tuple(settings.TEMP_EXTENSIONS)): return

            for _ in range(5):
                if is_file_ready(file_path):
                    folder_organization(file_path)
                    break
                time.sleep(1)

class ServiceManager:
    def __init__(self):
        self.observer = None
        self.is_running = False

    def start(self):
        if self.is_running: return
        logging.info("--- Service Starting ---")
        
        # Run startup scan immediately
        self.run_startup_scan()

        self.event_handler = MoverHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, settings.SOURCE_DIR, recursive=False)
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
        logging.info("--- Running Startup Scan ---")
        try:
            for file in os.listdir(settings.SOURCE_DIR):
                full_path = os.path.join(settings.SOURCE_DIR, file)
                if os.path.isfile(full_path):
                    folder_organization(full_path)
            logging.info("--- Startup Scan Complete ---")
        except Exception as e:
            logging.error(f"Scan Error: {e}")

    def open_log_file(self):
        # FIX: Check OS to use correct open command
        if os.path.exists(settings.LOG_FILE):
            if platform.system() == "Darwin":       # MacOS
                subprocess.call(["open", settings.LOG_FILE])
            elif platform.system() == "Windows":    # Windows
                os.startfile(settings.LOG_FILE)
            else:                                   # Linux
                subprocess.call(["xdg-open", settings.LOG_FILE])
        else:
            print("Log file does not exist yet.")