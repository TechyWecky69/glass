"""
desktop.py

Create Linux/KDE desktop launcher files.
"""

from pathlib import Path

from .app import App
from .browser import Browser, build_command


DESKTOP_TEMPLATE = """[Desktop Entry]
Version=1.0
Type=Application
Name={name}
Comment={comment}
Exec={exec}
Icon={icon}
Terminal=false
StartupNotify=true
Categories=Network;WebBrowser;
"""


def create_desktop_entry(
    app: App,
    browser: Browser,
):
    """
    Create a .desktop launcher for a web application.
    """

    if app.desktop_path is None:
        raise ValueError(
            "Application has no desktop path."
        )

    command = build_command(
        browser=browser,
        url=app.url,
        isolated=app.isolated,
        profile_path=app.profile_path,
    )

    content = DESKTOP_TEMPLATE.format(
        name=app.name,
        comment=f"Web application - {app.url}",
        exec=command,
        icon=app.icon_path
        if app.icon_path
        else "",
    )

    app.desktop_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    app.desktop_path.write_text(
        content,
        encoding="utf-8",
    )

    app.desktop_path.chmod(
        0o755
    )


def remove_desktop_entry(
    app: App,
):
    """
    Remove a desktop launcher.
    """

    if (
        app.desktop_path
        and app.desktop_path.exists()
    ):

        app.desktop_path.unlink()


if __name__ == "__main__":

    print(
        "desktop.py loaded successfully."
    )
