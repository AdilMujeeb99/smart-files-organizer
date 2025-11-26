#  Smart Desktop Organizer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**A background automation service that keeps your Downloads folder pristine.** It uses a Watchdog observer to detect file changes in real-time, automatically sorting files into intelligent categories (Images, Installers, Calendar Events, etc.) instantly. Includes a System Tray GUI for easy management.

---

##  Key Features

* **Real-Time Monitoring:** Uses `watchdog` to detect file drops instantly (Event-Driven).
* **System Tray Control:** Custom GUI built with `pystray` to Start/Stop/Scan from the taskbar.
* **Smart Logic:**
    * **Duplicate Handling:** Auto-renames files (`resume_1.pdf`) to prevent overwrites.
    * **Lock Detection:** Waits for browsers to finish writing files before moving them.
    * **Junk Filtering:** Automatically ignores `.tmp` and `.crdownload` files to save CPU.
* **Event Logging:** Tracks every movement in a local `organizer_history.log` file.

## 🛠️ Tech Stack

* **Python 3**
* **Watchdog** (Filesystem Events)
* **Pystray** (System Tray GUI)
* **Pillow** (Image Processing)
* **Threading** (Concurrency)

##  How to Run

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/AdilMujeeb99/smart-files-organizer.git](https://github.com/AdilMujeeb99/smart-files-organizer.git)
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Background Service**
    ```bash
    python organizer.pyw
    ```

##  Folder Structure

```text
/Downloads
    ├── /Images
    ├── /Documents
    ├── /Installers
    ├── /Code
    ├── /Archives
    └── /Calendar Events
