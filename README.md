# 🛰️ Star Citizen Discord Rich Presence

Display your in-game location from **Star Citizen** directly in Discord Rich Presence, powered by OCR, alias mapping, and auto-updating data.

> Discord server coming soon for easier communication

![image](https://i.imgur.com/PZC7QJg.png)

---

## 🚀 Features

- 🔍 **Detects and displays** your current Star Citizen location
- 🧠 **Uses EasyOCR** to scan your screen dynamically
- 🔄 **Auto-updating** location alias file via GitHub
- 🤖 **Discord Rich Presence** integration
- 📸 Optional debug screenshots
- ⚙️ Easily configurable settings
- 🪐 Stanton System added(Still testing every location as it has to be added manually)
- 🪐 Pyro coming soon

---

## 🛠️ Requirements

- Python **3.8+**
- Required packages (install with `pip install -r requirements.txt`):
  - `easyocr`
  - `pillow`
  - `screeninfo`
  - `pypresence`
  - `requests`
  - `numpy`
  - `torch`

---

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/Lucrona/star-citizen-discord.git
   cd star-citizen-discord
2. ```bash
   pip install -r requirements.txt
4. ```bash
   python starcitizen_presence.py

---

## 💡 Customization
You can edit the following options at the top of starcitizen_presence.py:

| Option                | Description                               |
| --------------------- | ----------------------------------------- |
| `CAPTURE_INTERVAL`    | How often to update location (in seconds) |
| `USE_DISCORD`         | Toggle Discord Rich Presence on/off       |
| `SAVE_DEBUG_IMAGE`    | Save OCR region as image for debugging    |
| `AUTO_UPDATE_ALIASES` | Enable auto-updating from GitHub          |


- Alias mappings are stored in location_aliases.txt. Auto-updates check against the version in loc_version.txt.
- Version checks are managed via loc_version.txt

 ---

## 📘 Coming Soon

-🖼️ GUI launcher

-🧊 Standalone .exe version (no Python required)

-🪐 Fixes for Stanton and Add Pyro

-🏴‍☠️ Stealth mode to hide your location on discord

-![image](https://i.imgur.com/QnL33pl.png) Display RSI Name and Org

---

## 🤝 Contributing
- PRs welcome! Please test changes thoroughly and follow the current structure for aliases and logic.

---
## 📜 License
- MIT – use freely, modify as needed.
---
# Made for the Verse by Lucrona
