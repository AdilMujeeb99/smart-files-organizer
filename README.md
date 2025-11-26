# Smart Desktop Organizer 

A background automation tool built in Python that automatically keeps your Downloads folder clean. It uses the `watchdog` library to detect file changes in real-time and sorts them into categories (Images, Docs, Installers, etc.) instantly.

## Features
- **Real-time Monitoring:** detects files the moment they are downloaded.
- **System Tray Integration:** Control the app (Start/Stop/Scan) from the Windows taskbar.
- **Smart Logic:** - Ignores temporary browser files (`.crdownload`, `.tmp`).
    - Handles duplicate files automatically (renames to `file (1).jpg`).
    - waits for file locks to release before moving.
- **Logging:** Keeps a history of all moved files.

## Built With
- Python 3
- [Watchdog](https://pypi.org/project/watchdog/) (File System Events)
- [Pystray](https://pypi.org/project/pystray/) (System Tray GUI)
- [Pillow](https://pypi.org/project/Pillow/) (Image Processing)

## Installation

1. Clone the repo:
   ```bash
   git clone [https://github.com/AdilMujeeb99/smart-organizer.git](https://github.com/AdilMujeeb99/smart-organizer.git)