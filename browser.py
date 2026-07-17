"""
browser.py

Browser detection and command generation.
"""

from dataclasses import dataclass
from pathlib import Path
from shutil import which
import shlex


@dataclass
class Browser:
    """
    Represents a supported browser.
    """

    name: str
    executable: str


BROWSERS = {
    "chrome": [
        "google-chrome-stable",
        "google-chrome",
    ],
    "chromium": [
        "chromium",
        "chromium-browser",
    ],
    "brave": [
        "brave-browser",
        "brave",
    ],
    "edge": [
        "microsoft-edge-stable",
        "microsoft-edge",
    ],
    "vivaldi": [
        "vivaldi-stable",
        "vivaldi",
    ],
    "firefox": [
        "firefox",
    ],
}


def _find_browser(name: str):
    """
    Locate a browser by name.
    """

    for executable in BROWSERS.get(name, []):

        path = which(executable)

        if path:

            return Browser(
                name=name,
                executable=path,
            )

    return None


def detect_browser(preferred="auto"):
    """
    Detect the first installed supported browser.
    """

    if preferred != "auto":
        return _find_browser(preferred)

    for browser in (
        "chrome",
        "chromium",
        "brave",
        "edge",
        "vivaldi",
        "firefox",
    ):

        found = _find_browser(browser)

        if found:
            return found

    return None


def list_installed_browsers():
    """
    Return every installed supported browser.
    """

    browsers = []

    for name in BROWSERS:

        browser = _find_browser(name)

        if browser:
            browsers.append(browser)

    return browsers


def build_command(
    browser: Browser,
    url: str,
    isolated=False,
    profile_path: Path | None = None,
):
    """
    Build the command stored inside the desktop launcher.
    """

    command = shlex.quote(browser.executable)

    #
    # Optional isolated profile
    #

    if isolated:

        if profile_path is None:
            raise ValueError(
                "profile_path is required when isolated=True."
            )

        command += (
            f" --user-data-dir="
            f"{shlex.quote(str(profile_path))}"
        )

    #
    # Firefox
    #

    if browser.name == "firefox":

        command += (
            f" --new-window "
            f"{shlex.quote(url)}"
        )

        return command

    #
    # Chromium browsers
    #

    command += (
        f" --app="
        f"{shlex.quote(url)}"
    )

    return command


if __name__ == "__main__":

    print("Installed browsers:\n")

    installed = list_installed_browsers()

    if not installed:

        print("No supported browsers found.")

    else:

        for browser in installed:

            print(
                f"{browser.name:12}"
                f"{browser.executable}"
            )

    print()

    default = detect_browser()

    if default:

        print(
            f"Default browser: {default.name}"
        )

    else:

        print(
            "No supported browser detected."
        )
