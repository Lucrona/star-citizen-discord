# 📝 Changelog

All notable changes to this project will be documented here.  

---

## [0.08] – 2025-06-17  
### ✅ Focus: Build Stability, Compression, Redundancy Cleanup

### ⚙️ Core Improvements
- 📦 **EXE Compression Enabled:** Integrated UPX compression using external UPX path to reduce executable size.

### 🔧 Code Cleanup
- 🧹 **Removed Unused Imports:** Removed `Image` from `PIL` as it was unused.
- 🧼 **Simplified Version Print Logic:** Eliminated double "Location Version" display.
- 🪶 **Removed Unused Variables:** Removed `flat` text from OCR parsing as it was no longer used.

---

## 📦 [0.07] – 2025-06-17  
**✅ Focus: CPU Performance, Stability, Logging**

### ⚙️ Core Improvements
- 🧠 **Lazy EasyOCR Initialization**  
  `easyocr.Reader` is now only created after game launch is detected, improving startup time and reducing CPU strain.

- 🖤 **Grayscale Capture**  
  Screen captures are now converted to grayscale before OCR to reduce processing time.

- ⏱️ **Accurate Interval Timing**  
  `CAPTURE_INTERVAL` now compensates for OCR+processing duration for consistent pacing.

- 🧼 **Numpy Removed**  
  Removed the `np.array` conversion from image capture to reduce memory usage and boost performance.

---

### 🛠️ Stability & Crash Prevention
- 🚫 **Reader Safety Check**  
  If `easyocr.Reader` isn’t initialized, `get_location_text()` will safely return `"Unknown"`.

- 🛑 **No-OCR Short-Circuit**  
  If OCR returns no results, the script skips parsing and logs `NO_OCR_RESULTS`.

---

### 📝 Logging & Debugging
- ✂️ **Trim Debug Logs**  
  `unmatched_locations.log` is trimmed to the last 100 lines to prevent bloat.

- 🧹 **Stripped Empty Lines**  
  Empty/whitespace lines are now excluded from log retention.

- ⚠️ **Noise Detection Logging**  
  Known main menu entries are logged as `"INVALID_LOCATION_ID"` for clarity.

---

## 📦 [0.06] – 2025-06-16

### 🆕 Added
- 📢 Main script version check using `drp_version.txt` from GitHub.
- 🔔 Notification for users when a newer version is available.

### ♻️ Changed
- 🐍 Renamed script to `starcitizen_drp.py`.
- 🧽 Cleaned version display: removed redundant “Location Version” label.

### 🐛 Fixed
- 🔢 Proper version comparison logic to prevent false updates.

---

## 📦 [0.05] – 2025-06-15

### 🆕 Added
- ❌ Removed `“LZ”` fallback — now only uses `"Current player location"` block.
- 🗂️ Centralized data into `%APPDATA%\StarCitizenPresence\Locations\`.
- 🔄 GitHub auto-update for `location_aliases.txt` & `loc_version.txt`.
- ⏳ Waiting loop displays animated dots, clears RPC on game exit.
- 🧠 Refined OCR logic and fuzzy-matching.

### ♻️ Changed
- 🔺 Script version bumped to **0.05**.
- 🎯 Fuzzy matching tuned: cutoff 0.7, top 3 matches.
- 🌐 Shows local vs remote alias version on launch.

### 🐛 Fixed
- 🧼 Removed duplicate “aliases up to date” message.
- 🧹 Consolidated main menu noise list handling.

---

## 📦 [0.04] – 2025-06-15

### 🆕 Added
- 🕹️ Game detection via `psutil`, pauses/resumes RPC automatically.
- 💬 “Waiting…” animation with dot updates.
- 🛑 Proper RPC clearing when game exits.
- 📁 Organized AppData structure for locations and logs.
- 📸 Debug screenshots stored under `Debugging` folder.

### ♻️ Changed
- 📂 Moved alias files into AppData locations.
- 🧼 Cleaned console output, removed duplicate messages.
- 🧽 Clears console line on game detection.

### 🐛 Fixed
- ✅ Ensures clean transition from waiting state to active presence.
- 🔁 Prevents multiple “Star Citizen detected!” prints.
