📝 Changelog: v0.07
✅ Focus: CPU Performance, Stability, Logging

⚙️ Core Improvements
🧠 Lazy EasyOCR Initialization: easyocr.Reader is now only created after game launch is detected, improving startup time and reducing CPU strain.

🖤 Grayscale Capture: Screen capture is now converted to grayscale before OCR to reduce processing time.

⏱️ Accurate Interval Timing: CAPTURE_INTERVAL is now enforced by subtracting processing time for consistent capture pacing.

🧼 Numpy Removed: Eliminated np.array conversion for images to keep memory overhead minimal.

🛠️ Stability & Crash Prevention
🚫 Reader Safety Check: If easyocr.Reader isn’t initialized, get_location_text() will safely return "Unknown" without crashing.

🛑 No-OCR Short-Circuit: Script now cleanly exits location parsing if OCR returns no results (NO_OCR_RESULTS).

📝 Logging & Debugging
✂️ Trim Debug Logs: unmatched_locations.log is now trimmed to the last 100 entries to avoid bloat.

🧹 Stripped Empty Lines: Empty/whitespace lines are now excluded from log retention.

⚠️ Noise Detection Logs: Main menu noise entries now log as "INVALID_LOCATION_ID" to help with debugging.
---

# Changelog

All notable changes to this project will be documented in this file.

##[ 0.06] – 2025-06-16
### Added

Main script version check via drp_version.txt hosted on GitHub

Notification for users when a newer version is available

### Changed

Renamed script to starcitizen_drp.py

Cleaned version display: removed redundant “Location Version” label

### Fixed

False positives when comparing script version numbers (now uses proper version parsing)

---

## [0.05] – 2025-06-15
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

---

## [0.04] – 2025-06-15

### Added
- 🕹️ **Process detection** via `psutil` to pause/resume Rich Presence when `starcitizen.exe` starts or stops  
- ··· **Waiting animation** (“.” dots) while Star Citizen isn’t running  
- 🛑 **Clear Rich Presence** exactly once when the game closes  
- 📂 Store all alias/version files under `%APPDATA%/StarCitizenPresence/Locations`  
- 🗄️ Store logs and debug screenshots under `%APPDATA%/StarCitizenPresence/Debugging`

### Changed
- 🗃️ Moved `location_aliases.txt` and `loc_version.txt` into AppData folders instead of local directory  
- 🧹 Cleared the “Waiting for Star Citizen…” console line once the game launches  
- 📝 Streamlined console output to remove redundant update/version messages  

### Fixed
- ✅ Ensure the waiting-dot line fully clears on detection of Star Citizen  
- 🔄 Prevent repeated “Star Citizen detected!” messages on each loop iteration  
