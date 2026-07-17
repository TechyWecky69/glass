"""
app.py

Application data model.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class App:
    """
    Represents an installed web application.
    """

    # Display name
    name: str

    # Website URL
    url: str

    # Internal identifier (e.g. youtube-com)
    app_id: str

    # Whether the application uses its own browser profile
    isolated: bool = False

    # Browser profile location (None when not isolated)
    profile_path: Path | None = None

    # Desktop launcher
    desktop_path: Path | None = None

    # Application icon
    icon_path: Path | None = None
