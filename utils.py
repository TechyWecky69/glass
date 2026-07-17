"""
utils.py

Shared helper functions.
"""

from pathlib import Path
import re


def ensure_directory(
    path: Path,
):
    """
    Create a directory if it does not exist.
    """

    path.mkdir(
        parents=True,
        exist_ok=True,
    )


def expand_path(
    path: str | Path,
) -> Path:
    """
    Expand shortcuts like ~/Documents.

    Example:
        ~/glass
        ->
        /home/user/glass
    """

    return Path(
        path
    ).expanduser()


def app_id(
    url: str,
) -> str:
    """
    Convert a URL into a safe application ID.

    Example:
        https://youtube.com
        ->
        youtube-com
    """

    from urllib.parse import urlparse

    parsed = urlparse(url)

    domain = parsed.netloc

    if not domain:
        domain = parsed.path

    domain = domain.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    domain = re.sub(
        r"[^a-z0-9]+",
        "-",
        domain,
    )

    return domain.strip("-")


def safe_filename(
    value: str,
) -> str:
    """
    Convert text into a safe filename.
    """

    value = value.lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value,
    )

    return value.strip("-")


def remove_file(
    path: Path,
):
    """
    Remove a file if it exists.
    """

    if path.exists():

        path.unlink()


if __name__ == "__main__":

    print(
        app_id(
            "https://www.youtube.com/watch?v=test"
        )
    )

    print(
        expand_path(
            "~/Documents"
        )
    )
