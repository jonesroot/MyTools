#!/usr/bin/env python3

import subprocess
import sys
import os
import platform
import time
from datetime import datetime, timedelta

DESC="DateTools - Multi Date Utility Tool."
VERSION = "1.0.2"
REPO_URL = "https://raw.githubusercontent.com/jonesroot/MyTools/refs/heads/main/Python/datetools.py"

REQUIRED_MODULES = ["pytz", "argparse"]

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
    pform = platform.system().lower()
    os.system("cls" if pform == "windows" else "clear")


def auto_install(package_name):
    try:
        __import__(package_name)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def check_update():
    print(f"{clr.CYAN}Checking for updates...{clr.RESET}")
    time.sleep(1)
    tmp_file = "/tmp/datetools_new"

    try:
        subprocess.run(["curl", "-s", "-o", tmp_file, REPO_URL], check=True)
        
        with open(tmp_file, "rb") as new_file, open(sys.argv[0], "rb") as old_file:
            if new_file.read() == old_file.read():
                print(f"{clr.GREEN}You're already using the latest version.{clr.RESET}")
                return

        os.replace(tmp_file, sys.argv[0])
        print(f"{clr.GREEN}Updated to latest version! Restarting in 3 seconds...{clr.RESET}")
        time.sleep(3)
        os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        print(f"{clr.YELLOW}Failed to update: {e}{clr.RESET}")
        if os.path.exists(tmp_file):
            os.remove(tmp_file)


def main():
    clear_screen()
    for module in REQUIRED_MODULES:
        auto_install(module)
    import argparse
    import pytz

    parser = argparse.ArgumentParser(
        description=DESC
    )
    parser.add_argument(
        "--now",
        action="store_true",
        help="Show current time."
    )
    parser.add_argument(
        "--timezone",
        type=str,
        help="Show time in specific timezone."
    )
    parser.add_argument(
        "--add",
        type=int,
        help="Add days to current date."
    )
    parser.add_argument(
        "--countdown",
        type=str,
        help="Countdown to specific date (YYYY-MM-DD)."
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Check and update to latest version."
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show tool version."
    )

    args = parser.parse_args()

    if args.version:
        print(f"{clr.GREEN}{DESC}\nVersion: {VERSION}{clr.RESET}")
        sys.exit()

    if args.update:
        check_update()

    now = datetime.now()

    if args.now:
        print(f"{clr.CYAN}Current Time: {now}{clr.RESET}")

    if args.timezone:
        try:
            tz = pytz.timezone(args.timezone)
            print(f"{clr.CYAN}Time in {args.timezone}: {datetime.now(tz)}{clr.RESET}")
        except pytz.UnknownTimeZoneError:
            print(f"{clr.RED}Unknown timezone.{clr.RESET}")

    if args.add:
        future_date = now + timedelta(days=args.add)
        print(f"{clr.CYAN}Date after {args.add} days: {future_date.date()}{clr.RESET}")

    if args.countdown:
        try:
            target_date = datetime.strptime(args.countdown, "%Y-%m-%d")
            delta = target_date - now
            print(f"{clr.CYAN}Countdown: {delta.days} days left.{clr.RESET}")
        except ValueError:
            print(f"{clr.RED}Invalid date format. Use YYYY-MM-DD.{clr.RESET}")


if __name__ == "__main__":
    main()
