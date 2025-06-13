import sys
sys.stderr = open("error_log.txt", "w", encoding="utf-8")
import time
import os
import requests
import numpy as np
import easyocr
from PIL import ImageGrab
from screeninfo import get_monitors
from pypresence import Presence
import difflib

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

GITHUB_RAW_ALIAS_URL = "https://raw.githubusercontent.com/Lucrona/star-citizen-discord/main/location_aliases.txt"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Lucrona/star-citizen-discord/main/loc_version.txt"
LOCAL_VERSION_FILE = "loc_version.txt"

# ================================
# 🌐 AUTO-UPDATE FROM GITHUB
# ================================
def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_remote_version():
    try:
        r = requests.get(GITHUB_VERSION_URL, timeout=5)
        if r.status_code == 200:
            return r.text.strip()
    except Exception as e:
        print(f"⚠️ Version check failed: {e}")
    return None

def update_location_aliases_from_github():
    print("🔄 Checking for location data update...")
    remote_version = get_remote_version()
    local_version = get_local_version()

    if not remote_version:
        print("⚠️ Could not fetch remote version. Skipping update.")
        return

    if remote_version != local_version:
        print(f"📦 New version available: {remote_version} (Local: {local_version})")
        try:
            r = requests.get(GITHUB_RAW_ALIAS_URL, timeout=5)
            if r.status_code == 200:
                with open("location_aliases.txt", "w", encoding="utf-8") as f:
                    f.write(r.text)
                with open(LOCAL_VERSION_FILE, "w", encoding="utf-8") as f:
                    f.write(remote_version)
                print("✅ location_aliases.txt updated from GitHub.")
            else:
                print(f"❌ Failed to download alias file: HTTP {r.status_code}")
        except Exception as e:
            print(f"❌ GitHub update error: {e}")
    else:
        print("✔️ location_aliases.txt is up to date.")

# ================================
# 📂 LOAD LOCATION ALIASES
# ================================
def load_location_aliases(filename="location_aliases.txt"):
    if not os.path.exists(filename):
        print("❌ Alias file not found. Creating fallback.")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# No aliases found.\n")
    aliases = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                aliases[key.strip()] = val.strip()
    return aliases

location_aliases = {}

# ================================
# 📝 LOGGING UNMATCHED NAMES
# ================================
logged_location_misses = set()
logged_lz_misses = set()

def log_unmatched_location(name):
    if ENABLE_LOGGING_LOCATION and len(name) >= 3 and name not in logged_location_misses:
        with open("unmatched_locations.log", "a", encoding="utf-8") as f:
            f.write(f"{name}\n")
        logged_location_misses.add(name)

def log_unmatched_lz(name):
    if ENABLE_LOGGING_LZ and len(name) >= 3 and name not in logged_lz_misses:
        with open("unmatched_lz.log", "a", encoding="utf-8") as f:
            f.write(f"{name}\n")
        logged_lz_misses.add(name)

# ================================
# 🔍 FUZZY RESOLUTION
# ================================
def resolve_location_name(ocr_name):
    if not ocr_name or len(ocr_name) < 3:
        return "Unknown"

    replacements = {"tonz": "stanton2"}
    for wrong, right in replacements.items():
        ocr_name = ocr_name.lower().replace(wrong, right)

    keys = list(location_aliases.keys())
    best = difflib.get_close_matches(ocr_name, keys, n=1, cutoff=0.6)

    if best:
        return location_aliases[best[0]]

    log_unmatched_location(ocr_name)
    return ocr_name

# ================================
# 💻 MONITOR SETUP
# ================================
try:
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height
except Exception as e:
    print(f"❌ Unable to detect monitor resolution: {e}")
    screen_width = 1920
    screen_height = 1080

# ================================
# 🔠 EASYOCR INITIALIZATION
# ================================
try:
    reader = easyocr.Reader(['en'], gpu=True)
except Exception as e:
    print(f"⚠️ GPU OCR init failed: {e}. Trying CPU mode...")
    reader = easyocr.Reader(['en'], gpu=False)

# ================================
# 📸 BOUNDING BOX FOR SCREEN CAPTURE
# ================================
def get_location_bbox():
    left = int(screen_width * 0.75)
    top = int(screen_height * 0.00)
    right = int(screen_width * 1.50)
    bottom = int(screen_height * 0.60)
    return (left, top, right, bottom)

# ================================
# 🔎 OCR TEXT DETECTION
# ================================
def get_location_text():
    bbox = get_location_bbox()
    screenshot = ImageGrab.grab(bbox=bbox)

    if SAVE_DEBUG_IMAGE:
        screenshot.save("debug_capture.png")

    img_np = np.array(screenshot)
    results = reader.readtext(img_np)
    texts = [text for (_, text, _) in results]
    flat_text = " ".join([t.lower() for t in texts])

    # --- Check for 'Current player location' ---
    if "current player location" in flat_text:
        for i, text in enumerate(texts):
            if "location" in text.lower():
                for j in range(i + 1, len(texts)):
                    loc_candidate = texts[j].strip(" :–-_()")
                    if len(loc_candidate) >= 3 and any(c.isalnum() or c == "_" for c in loc_candidate):
                        return resolve_location_name(loc_candidate)
        log_unmatched_location("NO_VALID_LOCATION_TEXT")

    # --- Fuzzy match for "LZ" ---
    for i, text in enumerate(texts):
        clean_text = text.lower().strip("()[]: ")
        if difflib.get_close_matches(clean_text, ["lz", "lz:"], n=1, cutoff=0.6):
            for j in range(i + 1, len(texts)):
                lz_candidate = texts[j].strip(" :–-_()")
                if len(lz_candidate) >= 3 and any(c.isalnum() or c == "_" for c in lz_candidate):
                    resolved = resolve_location_name(lz_candidate)
                    if resolved == lz_candidate:
                        log_unmatched_lz(lz_candidate)
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
# 🚀 MAIN LOOP
# ================================
def main():
    print("🚀 Star Citizen Rich Presence Started")

    if AUTO_UPDATE_ALIASES:
        update_location_aliases_from_github()

    global location_aliases
    location_aliases = load_location_aliases()

    start_time = time.time()
    rpc = None

    if USE_DISCORD:
        try:
            rpc = init_discord()
        except Exception as e:
            print("⚠️ Discord RPC error:")
            print(e)

    while True:
        try:
            location = get_location_text()
            print(f"📍 Location: {location}")

            if USE_DISCORD and rpc:
                rpc.update(
                    details=f"At {location}",
                    large_image="starcitizen",
                    start=int(start_time)
                )
        except Exception as e:
            print("❌ Error during loop:")
            print(e)

        time.sleep(CAPTURE_INTERVAL)

# ================================
# 🎯 ENTRY POINT
# ================================
if __name__ == "__main__":
    main()
