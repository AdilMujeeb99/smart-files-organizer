import os

# Paths
SOURCE_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
LOG_FILE = "organizer_history.log"

# Rules
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".heic", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Installers": [
        ".exe", ".msi", ".msix",   # Windows
        ".dmg", ".pkg", ".app",    # Mac (Added these)
        ".deb", ".rpm", ".iso"     # Linux/Universal
    ],
    "Code": [".py", ".java", ".js", ".html", ".css", ".cpp", ".json"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Calendar Events": [".ics", ".ical", ".ifb"]
}

# Ignore list
TEMP_EXTENSIONS = [".tmp", ".crdownload", ".part", ".ini", ".db"]