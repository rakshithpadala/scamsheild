import io
import os
import shutil
import urllib.request
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "ml", "data", "raw")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def download_sms():
    dest_dir = os.path.join(RAW, "sms")
    os.makedirs(dest_dir, exist_ok=True)
    target = os.path.join(dest_dir, "SMSSpamCollection")
    if os.path.exists(target):
        print(f"SMS already exists at {target}")
        return

    url = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
    print(f"Downloading SMS Spam from {url}...")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()

    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        print("Zip contents:", zf.namelist())
        for member in zf.namelist():
            if os.path.basename(member).lower() == "smsspamcollection":
                with zf.open(member) as source, open(target, "wb") as f_out:
                    shutil.copyfileobj(source, f_out)
                print(f"Saved {target}")
                return
    raise RuntimeError("SMSSpamCollection not found in downloaded zip")

def download_tranco():
    dest_dir = os.path.join(RAW, "tranco")
    os.makedirs(dest_dir, exist_ok=True)
    target = os.path.join(dest_dir, "top-1m.csv")
    if os.path.exists(target):
        print(f"Tranco already exists at {target}")
        return

    url = "https://tranco-list.eu/top-1m.csv.zip"
    print(f"Downloading Tranco list from {url}...")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()

    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        print("Tranco zip contents:", zf.namelist())
        csv_name = [n for n in zf.namelist() if n.endswith(".csv")][0]
        with zf.open(csv_name) as source, open(target, "wb") as f_out:
            shutil.copyfileobj(source, f_out)
        print(f"Saved {target}")

def download_openphish():
    dest_dir = os.path.join(RAW, "openphish")
    os.makedirs(dest_dir, exist_ok=True)
    target = os.path.join(dest_dir, "feed_20261002.txt")
    target_today = os.path.join(dest_dir, "feed_20261003.txt")

    url = "https://openphish.com/feed.txt"
    print(f"Downloading OpenPhish feed from {url}...")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()

    with open(target, "wb") as f:
        f.write(content)
    print(f"Saved {target} ({len(content)} bytes)")

    # Also save as feed_20261003.txt if needed
    with open(target_today, "wb") as f:
        f.write(content)
    print(f"Saved {target_today}")

def download_urlhaus():
    dest_dir = os.path.join(RAW, "urlhaus")
    os.makedirs(dest_dir, exist_ok=True)
    target = os.path.join(dest_dir, "csv_recent.csv")
    if os.path.exists(target):
        print(f"URLhaus already exists at {target}")
        return

    url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
    print(f"Downloading URLhaus from {url}...")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()

    with open(target, "wb") as f:
        f.write(content)
    print(f"Saved {target} ({len(content)} bytes)")

if __name__ == "__main__":
    download_sms()
    download_tranco()
    download_openphish()
    download_urlhaus()
    print("All downloads finished!")
