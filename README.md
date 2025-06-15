# 🛰️ Star Citizen Discord Rich Presence

Display your current in-game location from **Star Citizen** directly in Discord Rich Presence — automatically.

![screenshot](https://i.imgur.com/PZC7QJg.png)

---

## 🚀 Features

- 📍 Shows your current in-game location in Discord
- 🪐 Stanton System, There may be errors with location names, Updates will come as we see them
- 🧠 Uses screen reading (OCR) with smart alias matching
- 🔁 Automatically updates location data from GitHub
- 📂 Stores all files neatly in your AppData folder
- 🛠️ Works in the background — plug and play

---

## 🪵 Latest Changelog
### [0.05] – 2025-06-15
### Added
- ❌ **Removed “LZ” fallback** entirely – now only scans for the “Current player location” block.
- 🗂️ **AppData storage** for all alias, version, and debug files under `%APPDATA%\StarCitizenPresence\`.
- 🔄 **GitHub auto-update** simplified: only pulls `location_aliases.txt` & `loc_version.txt` from the `Locations/` folder.
- 🧵 **Waiting loop** now clears RPC on game exit and shows animated dots until SC launches.
- 🔍 **OCR logic** and fuzzy-matching refactored for speed and clarity.

### Changed
- ✨ Bumped internal script version to **0.05** and display on startup.
- 📈 Fuzzy matching cutoff tuned to 0.7, showing top 3 candidates.
- 🚀 Startup now shows local vs remote alias version once.

### Fixed
- 🐛 Double-print of “alias file up to date” removed.
- 📄 Main-menu noise handling consolidated into a single list.


## 📘 Coming Soon

- 🖼️ GUI launcher with system tray icon  
- 🪐 Pyro System  
- ![screenshot](https://i.imgur.com/3WOnWIo.png) RSI Profile link and ORG
- Code optmizations 

---

## 🧰 Installation

1. [**Download the latest version**](https://github.com/Lucrona/star-citizen-discord/releases/download/discord/starcitizen_presence.exe)
2. **Run the tool** while you're in-game.
3. It will display your location on Discord — that's it!

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

## 📜 License

MIT License — free to use, copy, and modify.

---

**Created for the Verse by Lucrona**
