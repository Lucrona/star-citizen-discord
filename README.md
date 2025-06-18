# 🛰️ Star Citizen Discord Rich Presence

Display your current in-game location from **Star Citizen** directly in Discord Rich Presence — automatically.

![screenshot](https://i.imgur.com/PZC7QJg.png)    <img src="https://i.imgur.com/DGgfxVK.png" width="270" height="110" />
### Exe Version: **0.07**  |  Location Data Version: **0.04**

---

## 🚀 Features

- 📍 Shows your current in-game location in Discord
- 🪐 Stanton System, There may be errors with location names, Updates will come as we see them
- 🧠 Uses screen reading (OCR) with smart alias matching
- 🔁 Automatically updates location data from GitHub
- 📂 Stores all files neatly in your AppData folder
- 🛠️ Works in the background — plug and play

---

## 📘 Coming Soon

- 🖼️ GUI launcher with system tray icon  
- 🪐 Pyro System
- 🏴‍☠️ Stealth Mode, Hide for your pirate needs
- ![screenshot](https://i.imgur.com/3WOnWIo.png) RSI Profile link and ORG
- ⚡ Code optmizations 

---

## 🧰 Installation

1. [**Download the latest version**](https://github.com/Lucrona/star-citizen-discord/releases/download/v0.06/starcitizen_drp.exe)
2. **Run the tool** while you're in-game.
3. Ensure you have **r_displayinfo 1** displayed, As thats how it reads the data,  **Press ` then type r_displayinfo 1**
4. It will display your location on Discord — that's it!

You don't need to install anything else. It handles everything automatically.

---

## 🔄 Auto Update

- Automatically checks GitHub for the latest location data
- Downloads updates in the background
- No need to manually update alias files

---

## 📂 Where Files Are Stored

All support files are saved to: %APPDATA%\StarCitizenPresence


| Folder            | What it stores                      |
|-------------------|-------------------------------------|
| `Locations/`      | Auto-updated location data          |
| `Debugging/`      | Optional screenshots & unmatched logs|

Only the `.exe` is visible — all other data is stored behind-the-scenes.

---

## 🪵 Latest Changelog
### 📝Changelog: v0.07 18/06/2025

✅ Focus: CPU Performance, Stability, Logging

### ⚙️ Core Improvements
🧠 Lazy EasyOCR Initialization: easyocr.Reader is now only created after game launch is detected, improving startup time and reducing CPU strain.

🖤 Grayscale Capture: Screen capture is now converted to grayscale before OCR to reduce processing time.

⏱️ Accurate Interval Timing: CAPTURE_INTERVAL is now enforced by subtracting processing time for consistent capture pacing.

🧼 Numpy Removed: Eliminated np.array conversion for images to keep memory overhead minimal.

### 🛠️Stability & Crash Prevention

🚫 Reader Safety Check: If easyocr.Reader isn’t initialized, get_location_text() will safely return "Unknown" without crashing.

🛑 No-OCR Short-Circuit: Script now cleanly exits location parsing if OCR returns no results (NO_OCR_RESULTS).

### 📝Logging & Debugging

✂️ Trim Debug Logs: unmatched_locations.log is now trimmed to the last 100 entries to avoid bloat.

🧹 Stripped Empty Lines: Empty/whitespace lines are now excluded from log retention.

⚠️ Noise Detection Logs: Main menu noise entries now log as "INVALID_LOCATION_ID" to help with debugging.

---

## 📜 License

MIT License — free to use, copy, and modify.

---

**Created for the Verse by Lucrona**
