import os

# Paths
# This automatically finds the correct user folder on Mac OR Windows
USER_HOME = os.path.expanduser("~")
SOURCE_DIR = os.path.join(USER_HOME, "Downloads")

# We save the log in Downloads because writing inside the App Bundle is forbidden on Mac
LOG_FILE = os.path.join(SOURCE_DIR, "organizer_history.log")

# Rules
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".heic", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".pages"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Installers": [".exe", ".msi", ".msix", ".dmg", ".pkg", ".app", ".deb", ".rpm", ".iso"],
    "Code": [".py", ".java", ".js", ".html", ".css", ".cpp", ".json"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Calendar Events": [".ics", ".ical", ".ifb"]
}

# Ignore list
TEMP_EXTENSIONS = [".tmp", ".crdownload", ".part", ".ini", ".db"]