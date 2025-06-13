# 🛰️ Star Citizen Discord Rich Presence

Display your in-game location from **Star Citizen** directly in Discord Rich Presence, powered by OCR, alias mapping, and auto-updating data.

Discord server coming soon for easier communication

![image](https://i.imgur.com/PZC7QJg.png)

---

## ✨ Features

- 🔍 **In-game location detection** using EasyOCR
- 🧠 **Alias matching** with fuzzy logic
- 🔄 **Auto-updating** location alias file via GitHub
- 🗺️ Supports both current player location and landing zone (LZ)
- 🤖 **Discord Rich Presence** integration
- 📸 Optional debug screenshots
- ⚙️ Easily configurable settings

---

## 🛠️ Requirements

- Python 3.8+
- Required packages (install with `pip install -r requirements.txt`):
  - `easyocr`
  - `pillow`
  - `screeninfo`
  - `pypresence`
  - `requests`
  - `numpy`

---

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/Lucrona/star-citizen-discord.git
   cd star-citizen-discord
2. ```bash
   pip install -r requirements.txt
4. ```bash
   python main.py

⚙️ Configuration
Inside main.py:

Option	Description
CAPTURE_INTERVAL	How often to update location (in seconds)
USE_DISCORD	Toggle Discord RPC on/off
SAVE_DEBUG_IMAGE	Saves a screenshot of the OCR region
AUTO_UPDATE_ALIASES	Pull updated aliases from GitHub

Alias mappings are stored in location_aliases.txt. Auto-updates check against the version in loc_version.txt.

🚧 GUI & Executable
GUI and executable (.exe) build coming soon.

The tool will be bundled with all dependencies and support auto-updating aliases.

🤝 Contributing
PRs welcome! Please test changes thoroughly and follow the current structure for aliases and logic.

📜 License
MIT – use freely, modify as needed.

Made for the Verse by Lucrona
