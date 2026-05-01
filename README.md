# Student Productivity Dashboard

A multi-tab desktop application built with Python and wxPython designed to help students stay focused and organized. Combines a Pomodoro timer, a music player, and a persistent to-do list in a single GUI application.

---

## Features

### Pomodoro Timer
- Configurable study time, break time, and number of cycles
- Automatic switching between study and break sessions
- Pause, resume, and stop controls
- Audio alerts on session transitions using background threads
- Skips final break after the last study cycle

### Music Player
- One-click access to curated YouTube study music playlists
- Genres: Lo-fi, Classical, Jazz

### To-Do List
- Add and remove tasks with a clean checklist interface
- Tasks persist between sessions using a local SQLite3 database
- Supports adding tasks via button click or Enter key

---

## Technical Highlights

- **OOP Design** — each tab is an independent `wx.Panel` subclass, keeping concerns separated and code modular
- **Multithreading** — audio playback runs on a background thread using Python's `threading` module, preventing GUI freezes
- **SQLite3 Integration** — tasks are stored in a local database with full CRUD operations, persisting across app restarts
- **Event-Driven Architecture** — uses `wx.Timer` and wxPython event binding instead of blocking loops, keeping the UI responsive

---

## Tech Stack

- Python 3
- wxPython
- SQLite3 (built-in)
- threading (built-in)
- webbrowser (built-in)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JCano22/Timer
cd Timer
```

2. Install dependencies:
```bash
pip install wxPython
```

3. Run the app:
```bash
python timer.py
```

---

## Usage

- **Pomodoro Timer** — click "Set Timer", enter your study time, break time, and number of cycles, then the timer starts automatically
- **Music Player** — click a genre button to open a curated YouTube playlist in your browser
- **To-Do List** — type a task and press Add or Enter to save it; check items and click Remove to delete them

---

## Author

Jorge Cano — [jcano3659@sdsu.edu](mailto:jcano3659@sdsu.edu)
