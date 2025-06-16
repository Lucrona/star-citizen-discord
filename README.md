# 🛰️ Star Citizen Discord Rich Presence
## Exe Version: 0.06 | Location Data Version: 0.04
 
Display your current in-game location from **Star Citizen** directly in Discord Rich Presence — automatically.

![screenshot](https://i.imgur.com/PZC7QJg.png)    <img src="https://i.imgur.com/DGgfxVK.png" width="270" height="110" />


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
- ![screenshot](https://i.imgur.com/3WOnWIo.png) RSI Profile link and ORG
- Code optmizations 

---

## 🧰 Installation

1. [**Download the latest version**](https://github.com/Lucrona/star-citizen-discord/releases/download/v0.06/starcitizen_drp.exe)
2. **Run the tool** while you're in-game.
3. Ensure you have **r_displayinfo 2** displayed, As thats how it read the data,  **Press ` then type r_displayinfo 2**
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
## [ 0.06] – 2025-06-16
### Added

Main script version check via drp_version.txt hosted on GitHub

Notification for users when a newer version is available

### Changed

Renamed script to starcitizen_drp.py

Cleaned version display: removed redundant “Location Version” label

### Fixed

False positives when comparing script version numbers (now uses proper version parsing)

---

## 📜 License

MIT License — free to use, copy, and modify.

---

**Created for the Verse by Lucrona**
