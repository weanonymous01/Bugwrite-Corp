#!/usr/bin/env python3
"""
Local Background Daemon for Autonomous Trend Publishing on Bugwrite.

Runs in an endless loop:
1. Executes autonomous_trend_publisher.py to harvest live spikes, research,
   generate deep articles, pull Pinterest photos, and deploy.
2. Commits and pushes new articles directly to git main (triggering Vercel deployment).
3. Sleeps for the designated interval (default: 2 hours) and repeats.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERVAL_SECONDS = 2 * 60 * 60  # 2 hours

def run_cycle():
    print("\n" + "=" * 80)
    print(f" [AUTONOMOUS DAEMON CYCLE] Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    try:
        # Run publisher
        publisher_script = os.path.join(ROOT, "scripts", "autonomous_trend_publisher.py")
        res = subprocess.run([sys.executable, publisher_script, "--max-articles", "2"], text=True)

        # Check if git has changes
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=ROOT)
        if status.stdout.strip():
            print("[+] New articles staged. Committing and pushing to origin main...")
            subprocess.run(["git", "add", "."], cwd=ROOT, check=True)
            subprocess.run(["git", "commit", "-m", "Auto-publish live trending articles & sitemaps"], cwd=ROOT, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, check=True)
            print("[✔] Successfully pushed live to Vercel production!")
        else:
            print("[✔] No new articles to commit this cycle.")
    except Exception as e:
        print(f"[!] Daemon cycle notice: {e}")

def main():
    print("=" * 80)
    print(" BUGWRITE AUTONOMOUS PUBLISHING DAEMON STARTED")
    print(" Polling interval: Every 2 hours")
    print(" Press Ctrl+C at any time to stop.")
    print("=" * 80)

    while True:
        run_cycle()
        print(f"\n[Sleeping] Next cycle in 2 hours ({INTERVAL_SECONDS} seconds)...")
        try:
            time.sleep(INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n[Stopped] Autonomous daemon stopped by user.")
            break

if __name__ == "__main__":
    main()
