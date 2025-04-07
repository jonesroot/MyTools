#!/usr/bin/env python3

import subprocess
import sys
import os
import platform
import time
from datetime import datetime, timedelta

VERSION = "1.0.0"
REPO_URL = "https://raw.githubusercontent.com/jonesroot/MyTools/refs/heads/main/Python/datetools.py"

required_modules = ["pytz", "argparse"]

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"

clr = Colors()


def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")


def auto_install(package_name):
    try:
        __import__(package_name)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def check_update():
    print(f"{clr.CYAN}Checking for updates...{clr.RESET}")
    try:
        subprocess.run(["curl", "-o", "/tmp/datetools", REPO_URL], check=True)
        os.replace("/tmp/datetools", sys.argv[0])
        print(f"{clr.GREEN}Updated to latest version! Restarting...{clr.RESET}")
        time.sleep(1)
        os.execv(sys.executable, ['python3'] + sys.argv)
    except Exception:
        print(f"{clr.YELLOW}Failed to update. Continuing...{clr.RESET}")


def main():
    for module in required_modules:
        auto_install(module)
    import argparse
    import pytz
    parser = argparse.ArgumentParser(description="DateTools - Multi Date Utility Tool")
    parser.add_argument("--now", action="store_true", help="Show current time")
    parser.add_argument("--timezone", type=str, help="Show time in specific timezone")
    parser.add_argument("--add", type=int, help="Add days to current date")
    parser.add_argument("--countdown", type=str, help="Countdown to specific date (YYYY-MM-DD)")
    parser.add_argument("--update", action="store_true", help="Update to latest version")

    args = parser.parse_args()

    print(f"{clr.BOLD}DateTools v{VERSION}{clr.RESET}")

    if args.update:
        check_update()

    now = datetime.now()

    if args.now:
        if args.timezone:
            tz = pytz.timezone(args.timezone)
            print(f"Current Time [{args.timezone}]: {datetime.now(tz)}")
        else:
            print(f"Current Time [UTC]: {datetime.utcnow()}")

    if args.add:
        future = now + timedelta(days=args.add)
        print(f"Now: {now}\nFuture (+{args.add} days): {future}")

    if args.countdown:
        target = datetime.strptime(args.countdown, "%Y-%m-%d")
        delta = target - now
        print(f"Countdown to {args.countdown}: {delta.days} days left")


if __name__ == "__main__":
    main()
