"""
main.py

Command-line entry point for WebApp.
"""

import argparse
import os
import sys

from .browser import detect_browser
from .installer import (
    install_glass,
    remove_glass,
    list_glass,
)

from .database import load_app

def build_parser():
    parser = argparse.ArgumentParser(
        prog="glass",
        description="Install websites as desktop applications.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    #
    # INSTALL
    #

    install = subparsers.add_parser(
        "install",
        help="Install a website as a desktop application.",
    )

    install.add_argument(
        "url",
        help="Website URL",
    )

    install.add_argument(
        "--name",
        metavar="NAME",
        help="Override the detected application name.",
    )

    install.add_argument(
        "--isolated",
        metavar="DIRECTORY",
        help=(
            "Use a dedicated browser profile stored under DIRECTORY."
        ),
    )

    #
    # REMOVE
    #

    remove = subparsers.add_parser(
        "remove",
        help="Remove an installed web application.",
    )

    remove.add_argument(
        "id",
        help="Application ID (e.g. youtube-com)",
    )

    #
    # LIST
    #

    subparsers.add_parser(
        "list",
        help="List installed web applications.",
    )

    #
    # INFO
    #

    info = subparsers.add_parser(
        "info",
        help="Show information about an installed web application.",
    )

    info.add_argument(
        "id",
        help="Application ID",
    )

    #
    # HELP
    #

    subparsers.add_parser(
        "help",
        help="Show available commands.",
    )

    return parser


def main():

    #
    # Prevent accidental sudo usage
    #

    if os.geteuid() == 0:
        print("Do not run glass using sudo.")
        print("Run it as your normal user.")
        sys.exit(1)

    parser = build_parser()

    args = parser.parse_args()

    #
    # INSTALL
    #

    if args.command == "install":

        browser = detect_browser()

        if browser is None:
            print("No supported browser found.")
            sys.exit(1)

        install_glass(
            url=args.url,
            browser=browser,
            name=args.name,
            isolated=args.isolated is not None,
            profile_root=args.isolated,
        )

        return

    #
    # REMOVE
    #

    if args.command == "remove":

        remove_glass(args.id)

        return

    #
    # LIST
    #

    if args.command == "list":

        list_glass()

        return

    #
    # INFO
    #

    if args.command == "info":

        app = load_app(args.id)

        if app is None:
            print(f'No application with ID "{args.id}" found.')
            sys.exit(1)

        print(f"Name:       {app.name}")
        print(f"ID:         {app.app_id}")
        print(f"URL:        {app.url}")
        print(f"Isolated:   {'Yes' if app.isolated else 'No'}")

        if app.profile_path:
            print(f"Profile:    {app.profile_path}")

        print(f"Desktop:    {app.desktop_path}")
        print(f"Icon:       {app.icon_path}")

        return

        #
    # HELP
    #

    if args.command == "help":

        print(
            """
glass - Install websites as desktop applications

Commands:

  install <url>
        Install a website as an application.

        Options:
          --name "Name"
                Override the detected application name.

          --isolated <directory>
                Create a separate browser profile.
                Example:
                  glass install https://youtube.com --isolated ~/WebApps


  remove <id>
        Remove an installed web application.


  list
        List all installed web applications.


  info <id>
        Show details about an installed web application.


  help
        Show this help message.
"""
        )

        return


if __name__ == "__main__":
    main()
