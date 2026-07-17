"""
database.py

Simple JSON database for installed web applications.
"""

from pathlib import Path
import json

from .app import App


DATABASE_DIR = (
    Path.home()
    / ".local"
    / "share"
    / "glass-db"
)


def ensure_database():
    """
    Create the database directory if required.
    """

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def database_file(app_id: str) -> Path:
    """
    Return the JSON file for an application.
    """

    return DATABASE_DIR / f"{app_id}.json"


def save_app(app: App):
    """
    Save an application's metadata.
    """

    ensure_database()

    data = {
        "name": app.name,
        "url": app.url,
        "app_id": app.app_id,
        "isolated": app.isolated,
        "profile_path": (
            str(app.profile_path)
            if app.profile_path is not None
            else None
        ),
        "desktop_path": str(app.desktop_path),
        "icon_path": str(app.icon_path),
    }

    with database_file(app.app_id).open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=4,
        )


def load_app(app_id: str) -> App | None:
    """
    Load an application from the database.
    """

    path = database_file(app_id)

    if not path.exists():
        return None

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    profile = data["profile_path"]

    if profile is not None:
        profile = Path(profile)

    return App(
        name=data["name"],
        url=data["url"],
        app_id=data["app_id"],
        isolated=data["isolated"],
        profile_path=profile,
        desktop_path=Path(data["desktop_path"]),
        icon_path=Path(data["icon_path"]),
    )


def delete_app(app_id: str):
    """
    Remove an application from the database.
    """

    path = database_file(app_id)

    if path.exists():
        path.unlink()


def list_apps() -> list[App]:
    """
    Return every installed application.
    """

    ensure_database()

    apps = []

    for file in sorted(
        DATABASE_DIR.glob("*.json")
    ):

        app = load_app(file.stem)

        if app is not None:
            apps.append(app)

    return apps


def app_exists(app_id: str) -> bool:
    """
    Check whether an application exists.
    """

    return database_file(app_id).exists()


if __name__ == "__main__":

    apps = list_apps()

    if not apps:

        print("No installed applications.")

    else:

        print("Installed applications:\n")

        for app in apps:

            print(
                f"{app.app_id:20}"
                f"{app.name}"
            )
