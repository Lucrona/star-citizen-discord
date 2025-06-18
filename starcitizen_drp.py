# ================================
# 🛰️ STAR CITIZEN DISCORD PRESENCE
# ================================

__version__ = "0.07"

print(f"      🚀 Star Citizen Rich Presence v{__version__} ")
print("Powered by Lucrona | https://github.com/Lucrona")
print("-" * 60)

import os
import time
import requests
from PIL import ImageGrab, Image
from screeninfo import get_monitors
from pypresence import Presence
import difflib
import psutil
from pathlib import Path
import easyocr

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
DEBUG_IMAGE_PATH = DBG_DIR / "debug_capture.png"

# ================================
# 🔧 CONFIGURATION
# ================================
DISCORD_CLIENT_ID = "1382616912412016801"
USE_DISCORD = True
CAPTURE_INTERVAL = 15
SAVE_DEBUG_IMAGE = True
ENABLE_LOGGING_LOCATION = True
AUTO_UPDATE_ALIASES = True

GITHUB_RAW_ALIAS_URL = "https://raw.githubusercontent.com/Lucrona/star-citizen-discord/main/Locations/location_aliases.txt"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Lucrona/star-citizen-discord/main/Locations/loc_version.txt"
GITHUB_PY_VERSION_URL = "https://raw.githubusercontent.com/Lucrona/star-citizen-discord/main/drp_version.txt"
REPO_LINK = "https://github.com/Lucrona/star-citizen-discord/releases"

MAIN_MENU_NOISE = {"o,_qdfinalize", "qdfinalize", "2,_qdfinalize"}

# ================================
# 🌐 AUTO-UPDATE LOCATION DATA
# ================================
def get_local_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "0.0.0"

def get_remote_version() -> str:
    try:
        r = requests.get(GITHUB_VERSION_URL, timeout=5)
        return r.text.strip() if r.status_code == 200 else ""
    except Exception as e:
        print(f"⚠️ Version check failed: {e}")
        return ""

def update_location_aliases_from_github() -> tuple[str, str]:
    print("🔄 Checking for location data update…")
    remote = get_remote_version()
    local = get_local_version()
    if not remote:
        print("⚠️ Could not fetch remote version. Skipping update.")
        return local, remote
    if remote != local:
        print(f"📦 New location data v{remote} available (Local v{local})")
        try:
            r = requests.get(GITHUB_RAW_ALIAS_URL, timeout=5)
            r.raise_for_status()
            ALIAS_FILE.write_text(r.text, encoding="utf-8")
            VERSION_FILE.write_text(remote, encoding="utf-8")
            print("✅ Aliases updated from GitHub.")
        except Exception as e:
            print(f"❌ GitHub update error: {e}")
    else:
        print("✔️ Location data is up to date.")
    return local, remote

def display_alias_versions(local: str, remote: str):
    print(f"📄 Local aliases version: {local.replace('Location Version', '').strip()}")
    if remote:
        print(f"🌐 Remote aliases version: {remote.replace('Location Version', '').strip()}")
    else:
        print("⚠️ Could not fetch remote alias version.")

# ================================
# 🔔 MAIN SCRIPT UPDATE CHECK
# ================================
def check_main_script_update():
    def version_tuple(v: str) -> tuple:
        return tuple(map(int, v.strip().split(".")))
    try:
        r = requests.get(GITHUB_PY_VERSION_URL, timeout=5)
        if r.status_code == 200:
            remote_version = r.text.strip()
            if version_tuple(remote_version) > version_tuple(__version__):
                print(f"\n🔔 New version available! ({remote_version})")
                print(f"⬇️  Download: {REPO_LINK}\n")
    except Exception as e:
        print(f"⚠️ Could not check for script update: {e}")

# ================================
# 📂 LOAD LOCATION ALIASES
# ================================
def normalize_ocr(text: str) -> str:
    return text.lower().replace(" ", "_").replace("1", "l").replace("0", "o").replace("|", "i")

def load_location_aliases() -> dict:
    if not ALIAS_FILE.exists():
        ALIAS_FILE.write_text("# no aliases\n", encoding="utf-8")
    aliases = {}
    for line in ALIAS_FILE.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, val = line.split("=", 1)
            aliases[normalize_ocr(key.strip())] = val.strip()
    return aliases

# ================================
# 📝 LOGGING
# ================================
logged_location_misses = set()

def log_unmatched_location(name: str):
    if ENABLE_LOGGING_LOCATION and name not in logged_location_misses:
        with UNMATCHED_LOC_LOG.open("a+", encoding="utf-8") as f:
            f.write(name + "\n")
        logged_location_misses.add(name)

        # Trim file to last 100 non-empty lines
        lines = [line.strip() for line in UNMATCHED_LOC_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(lines) > 100:
            UNMATCHED_LOC_LOG.write_text("\n".join(lines[-100:]), encoding="utf-8")

# ================================
# 🔍 FUZZY MATCHING
# ================================
def resolve_location_name(ocr_name: str) -> str:
    key = normalize_ocr(ocr_name.strip())
    best = difflib.get_close_matches(key, location_aliases.keys(), n=3, cutoff=0.7)
    if best:
        return location_aliases[best[0]]
    log_unmatched_location(key)
    return "Unknown"

# ================================
# 📸 OCR & SCREEN CAPTURE
# ================================
reader = None
monitor = get_monitors()[0]

def get_location_bbox():
    w, h = monitor.width, monitor.height
    return (int(w * 0.75), 0, int(w * 1.50), int(h * 0.60))

def get_location_text() -> str:
    if reader is None:
        return "Unknown"

    bbox = get_location_bbox()
    img = ImageGrab.grab(bbox=bbox).convert("L")  # grayscale
    if SAVE_DEBUG_IMAGE:
        img.save(DEBUG_IMAGE_PATH)

    results = reader.readtext(img)
    if not results:
        log_unmatched_location("NO_OCR_RESULTS")
        return "Unknown"

    texts = [t for (_, t, conf) in results if conf > 0.4 and len(t.strip()) > 2]
    flat = " ".join(t.lower() for t in texts)

    for t in texts:
        if normalize_ocr(t) in MAIN_MENU_NOISE:
            log_unmatched_location("INVALID_LOCATION_ID")
            return resolve_location_name("INVALID_LOCATION_ID")

    if "current player location" in flat:
        for i, t in enumerate(texts):
            if "location" in t.lower() and i + 1 < len(texts):
                return resolve_location_name(texts[i + 1].strip("()"))

    log_unmatched_location("NO_VALID_LOCATION_TEXT")
    return "Unknown"

# ================================
# 💬 DISCORD RPC
# ================================
def init_discord():
    rpc = Presence(DISCORD_CLIENT_ID)
    rpc.connect()
    return rpc

# ================================
# 🧠 PROCESS DETECTION
# ================================
def is_star_citizen_running() -> bool:
    return any('starcitizen.exe' in (p.info['name'] or '').lower() for p in psutil.process_iter(['name']))

# ================================
# 🚀 MAIN LOOP
# ================================
if __name__ == "__main__":
    check_main_script_update()

    if AUTO_UPDATE_ALIASES:
        local_v, remote_v = update_location_aliases_from_github()
        display_alias_versions(local_v, remote_v)

    location_aliases = load_location_aliases()
    rpc = init_discord() if USE_DISCORD else None

    game_running = False
    start_time = 0
    dots = ""

    while True:
        if not is_star_citizen_running():
            if game_running:
                game_running = False
                if rpc:
                    rpc.clear()
                    print("🛑 Star Citizen closed. Rich Presence cleared.")
            dots = (dots + ".")[-3:]
            print(f"🕹️ Waiting for Star Citizen{dots}", end="\r")
            time.sleep(3)
            continue

        if not game_running:
            print("\n✅ Star Citizen detected! Initializing...")
            game_running = True
            start_time = time.time()
            reader = easyocr.Reader(['en'], gpu=False)

        cycle_start = time.time()
        loc = get_location_text()
        print(f"📍 Location: {loc}      ")
        if USE_DISCORD and rpc:
            rpc.update(details=loc, large_image="starcitizen", start=int(start_time))

        elapsed = time.time() - cycle_start
        time.sleep(max(0, CAPTURE_INTERVAL - elapsed))
