"""
installer.py

Install, remove and list web applications.
"""

from pathlib import Path
import shutil

from .app import App
from .browser import build_command
from .database import (
    save_app,
    load_app,
    delete_app,
    list_apps,
    app_exists,
)
from .desktop import create_desktop_entry
from .icons import download_icon
from .metadata import get_metadata
from .profiles import create_profile
from .utils import (
    app_id,
    ensure_directory,
)


APP_DIR = (
    Path.home()
    / ".local"
    / "share"
    / "applications"
)

ICON_DIR = (
    Path.home()
    / ".local"
    / "share"
    / "icons"
    / "glass"
)


def install_glass(
    url,
    browser,
    name=None,
    isolated=False,
    profile_root=None,
):
    """
    Install a web application.
    """

    metadata = get_metadata(url)

    if not name:
        name = metadata.name

    identifier = app_id(url)

    if app_exists(identifier):
        print(f'"{identifier}" is already installed.')
        return

    ensure_directory(APP_DIR)
    ensure_directory(ICON_DIR)

    profile_path = None

    if isolated:

        if profile_root is None:
            raise RuntimeError(
                "profile_root must be supplied when using isolated mode."
            )

        profile_root = Path(profile_root).expanduser()

        ensure_directory(profile_root)

        profile_path = profile_root / identifier

        create_profile(profile_path)

    icon_path = ICON_DIR / f"{identifier}.png"

    desktop_path = APP_DIR / f"{identifier}.desktop"

    app = App(
        name=name,
        url=url,
        app_id=identifier,
        isolated=isolated,
        profile_path=profile_path,
        desktop_path=desktop_path,
        icon_path=icon_path,
    )

    print("Downloading icon...")

    try:
        download_icon(
            url=url,
            metadata=metadata,
            destination=icon_path,
        )

    except Exception as e:

        print(f"Warning: could not download icon ({e})")

    print("Creating launcher...")

    create_desktop_entry(
        app,
        browser,
    )

    save_app(app)

    print()
    print(f'Installed "{app.name}"')
    print(f"ID: {app.app_id}")

    if app.isolated:
        print(f"Profile: {app.profile_path}")


def remove_glass(app_id_value):
    """
    Remove an installed web application.
    """

    app = load_app(app_id_value)

    if app is None:
        print(f'Application "{app_id_value}" not found.')
        return

    print(f'Removing "{app.name}"...')

    #
    # Desktop file
    #

    if (
        app.desktop_path is not None
        and app.desktop_path.exists()
    ):
        app.desktop_path.unlink()

    #
    # Icon
    #

    if (
        app.icon_path is not None
        and app.icon_path.exists()
    ):
        app.icon_path.unlink()

    #
    # Browser profile
    #

    if (
        app.isolated
        and app.profile_path is not None
        and app.profile_path.exists()
    ):
        shutil.rmtree(
            app.profile_path,
            ignore_errors=True,
        )

    #
    # Database
    #

    delete_app(app.app_id)

    print("Done.")


def list_glass():
    """
    List every installed web application.
    """

    apps = list_apps()

    if not apps:
        print("No installed web applications.")
        return

    print()

    print(
        f'{"ID":25}'
        f'{"Name":30}'
        f'{"Isolated"}'
    )

    print("-" * 70)

    for app in apps:

        isolated = "Yes" if app.isolated else "No"

        print(
            f"{app.app_id:25}"
            f"{app.name[:29]:30}"
            f"{isolated}"
        )


def reinstall_icon(app_id_value):
    """
    Re-download an application's icon.
    """

    app = load_app(app_id_value)

    if app is None:
        print("Application not found.")
        return

    metadata = get_metadata(app.url)

    download_icon(
        url=app.url,
        metadata=metadata,
        destination=app.icon_path,
    )

    print("Icon updated.")


def rename_app(app_id_value, new_name):
    """
    Rename an installed application.
    """

    app = load_app(app_id_value)

    if app is None:
        print("Application not found.")
        return

    app.name = new_name

    save_app(app)

    print("Application renamed.")


def reinstall_desktop_file(
    app_id_value,
    browser,
):
    """
    Recreate the desktop launcher.
    """

    app = load_app(app_id_value)

    if app is None:
        print("Application not found.")
        return

    create_desktop_entry(
        app,
        browser,
    )

    print("Desktop file recreated.")


if __name__ == "__main__":

    print("Installed WebApps")
    print()

    list_glass()
