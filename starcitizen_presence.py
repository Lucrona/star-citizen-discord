# ================================
# 🛰️ STAR CITIZEN DISCORD PRESENCE
# ================================

__version__ = "0.03"

print(f"🚀 Star Citizen Rich Presence v{__version__} Started")

import os
import time
import requests
import numpy as np
import easyocr
from PIL import ImageGrab
from screeninfo import get_monitors
from pypresence import Presence
import difflib

from pathlib import Path

# ================================
# 🗂️ DIRECTORY SETUP
# ================================
APPDATA_BASE = Path(os.getenv("APPDATA")) / "StarCitizenPresence"
LOC_DIR = APPDATA_BASE / "Locations"
DBG_DIR = APPDATA_BASE / "Debugging"

LOC_DIR.mkdir(parents=True, exist_ok=True)
DBG_DIR.mkdir(parents=True, exist_ok=True)

ALIAS_FILE = LOC_DIR / "location_aliases.txt"
VERSION_FILE = LOC_DIR / "loc_version.txt"
UNMATCHED_LOC_LOG = DBG_DIR / "unmatched_locations.log"
UNMATCHED_LZ_LOG = DBG_DIR / "unmatched_lz.log"
DEBUG_IMAGE_PATH = DBG_DIR / "debug_capture.png"

# ================================
# 🔧 CONFIGURATION
# ================================
DISCORD_CLIENT_ID = "1382616912412016801"
USE_DISCORD = True
CAPTURE_INTERVAL = 15
SAVE_DEBUG_IMAGE = True
ENABLE_LOGGING_LOCATION = True
ENABLE_LOGGING_LZ = True
AUTO_UPDATE_ALIASES = True

GITHUB_RAW_ALIAS_URL = "https://raw.githubusercontent.com/Lucrona/star-citizen-discord/main/Locations/location_aliases.txt"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Lucrona/star-citizen-discord/main/Locations/loc_version.txt"

MAIN_MENU_NOISE = {
    "o,_qdfinalize", "qdfinalize", "2,_qdfinalize"
}

# ================================
# 🌐 AUTO-UPDATE FROM GITHUB
# ================================
def get_local_version():
    if not VERSION_FILE.exists():
        return "0.0.0"
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_remote_version():
    try:
        r = requests.get(GITHUB_VERSION_URL, timeout=5)
        if r.status_code == 200:
            return r.text.strip()
    except Exception as e:
        print(f"⚠️ Version check failed: {e}")
    return None

def update_location_aliases_from_github(remote_version=None):
    print("🔄 Checking for location data update...")
    if remote_version is None:
        remote_version = get_remote_version()

    if not remote_version:
        print("⚠️ Could not fetch remote version. Skipping update.")
        return

    local_version = get_local_version()
    if remote_version != local_version:
        print(f"📦 New version available: {remote_version} (Local: {local_version})")
        try:
            r = requests.get(GITHUB_RAW_ALIAS_URL, timeout=5)
            if r.status_code == 200:
                with open(ALIAS_FILE, "w", encoding="utf-8") as f:
                    f.write(r.text)
                with open(VERSION_FILE, "w", encoding="utf-8") as f:
                    f.write(remote_version)
                print("✅ location_aliases.txt updated from GitHub.")
            else:
                print(f"❌ Failed to download alias file: HTTP {r.status_code}")
        except Exception as e:
            print(f"❌ GitHub update error: {e}")
    else:
        print("✔️ location_aliases.txt is up to date.")

def display_alias_version(remote_version=None):
    print(f"📄 Local alias version:  {get_local_version()}")
    if remote_version is None:
        remote_version = get_remote_version()
    if remote_version:
        print(f"🌐 Remote alias version: {remote_version}")
    else:
        print("⚠️ Could not fetch remote alias version.")

# ================================
# 📂 LOAD LOCATION ALIASES
# ================================
def normalize_ocr(text):
    return (
        text.lower()
            .replace(" ", "_")
            .replace("1", "l")
            .replace("0", "o")
            .replace("|", "i")
    )

def load_location_aliases():
    if not ALIAS_FILE.exists():
        print("❌ Alias file not found. Creating fallback.")
        with open(ALIAS_FILE, "w", encoding="utf-8") as f:
            f.write("# No aliases found.\n")

    aliases = {}
    with open(ALIAS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                aliases[normalize_ocr(key.strip())] = val.strip()
    return aliases

# ================================
# 📝 LOGGING
# ================================
logged_location_misses = set()
logged_lz_misses = set()

def log_unmatched_location(name):
    if ENABLE_LOGGING_LOCATION and len(name) >= 3 and name not in logged_location_misses:
        with open(UNMATCHED_LOC_LOG, "a", encoding="utf-8") as f:
            f.write(f"{name}\n")
        logged_location_misses.add(name)

def log_unmatched_lz(name):
    if ENABLE_LOGGING_LZ and len(name) >= 3 and name not in logged_lz_misses:
        with open(UNMATCHED_LZ_LOG, "a", encoding="utf-8") as f:
            f.write(f"{name}\n")
        logged_lz_misses.add(name)

# ================================
# 🔍 FUZZY LOCATION RESOLUTION
# ================================
def resolve_location_name(ocr_name):
    if not ocr_name or len(ocr_name) < 3:
        return "Unknown"
    ocr_name = normalize_ocr(ocr_name.strip())
    keys = list(location_aliases.keys())
    best = difflib.get_close_matches(ocr_name, keys, n=3, cutoff=0.7)
    if best:
        return location_aliases[best[0]]
    log_unmatched_location(ocr_name)
    return "Unknown"

# ================================
# 🔠 OCR SETUP
# ================================
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height
reader = easyocr.Reader(['en'], gpu=False)

def get_location_bbox():
    left = int(screen_width * 0.75)
    top = int(screen_height * 0.00)
    right = int(screen_width * 1.50)
    bottom = int(screen_height * 0.60)
    return (left, top, right, bottom)

def get_location_text():
    screenshot = ImageGrab.grab(bbox=get_location_bbox())
    if SAVE_DEBUG_IMAGE:
        screenshot.save(DEBUG_IMAGE_PATH)
    img_np = np.array(screenshot)
    results = reader.readtext(img_np)
    texts = [text for (_, text, conf) in results if conf > 0.4 and len(text.strip()) > 2]
    flat_text = " ".join([t.lower() for t in texts])

    for text in texts:
        if normalize_ocr(text) in MAIN_MENU_NOISE:
            return resolve_location_name("INVALID_LOCATION_ID")

    if "current player location" in flat_text:
        for i, text in enumerate(texts):
            if "location" in text.lower():
                for j in range(i + 1, len(texts)):
                    candidate = texts[j].strip("()")
                    if len(candidate) >= 3:
                        return resolve_location_name(candidate)
        log_unmatched_location("NO_VALID_LOCATION_TEXT")

    for i, text in enumerate(texts):
        if difflib.get_close_matches(text.lower().strip("()[] "), ["lz", "lz:"], n=1, cutoff=0.6):
            for j in range(i + 1, len(texts)):
                candidate = texts[j].strip("()")
                if len(candidate) >= 3:
                    resolved = resolve_location_name(candidate)
                    if resolved == candidate:
                        log_unmatched_lz(candidate)
                    return resolved
            log_unmatched_lz("NO_VALID_LZ_TEXT")

    log_unmatched_location("NO_MATCH_FOUND")
    return "Unknown"

# ================================
# 💬 DISCORD INTEGRATION
# ================================
def init_discord():
    rpc = Presence(DISCORD_CLIENT_ID)
    rpc.connect()
    return rpc

# ================================
# 🚀 MAIN
# ================================
def main():
    if AUTO_UPDATE_ALIASES:
        remote_version = get_remote_version()
        update_location_aliases_from_github(remote_version)
        display_alias_version(remote_version)

    global location_aliases
    location_aliases = load_location_aliases()

    start_time = time.time()
    rpc = init_discord() if USE_DISCORD else None

    while True:
        try:
            location = get_location_text()
            print(f"📍 Location: {location}")
            if USE_DISCORD and rpc:
                rpc.update(
                    details=f" {location}",
                    large_image="starcitizen",
                    start=int(start_time)
                )
        except Exception as e:
            print("❌ Error during loop:")
            print(e)
        time.sleep(CAPTURE_INTERVAL)

# ================================
# 🎯 ENTRY
# ================================
if __name__ == "__main__":
    main()
