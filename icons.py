"""
icons.py

Download and save icons for web applications.
"""

from pathlib import Path
from urllib.parse import urljoin
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image


USER_AGENT = (
    "Mozilla/5.0 "
    "(X11; Linux x86_64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/138 Safari/537.36"
)


def fetch_html(url: str) -> BeautifulSoup:
    """
    Download and parse webpage HTML.
    """

    response = requests.get(
        url,
        headers={
            "User-Agent": USER_AGENT
        },
        timeout=15,
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser",
    )


def choose_best_icon(
    soup: BeautifulSoup,
    url: str,
) -> str | None:
    """
    Find the best available website icon.
    """

    priorities = [
        "apple-touch-icon",
        "apple-touch-icon-precomposed",
        "icon",
        "shortcut icon",
    ]

    for rel in priorities:

        tag = soup.find(
            "link",
            rel=lambda value:
                value and rel in value,
        )

        if tag and tag.get("href"):

            return urljoin(
                url,
                tag["href"],
            )

    #
    # Fallback
    #

    return urljoin(
        url,
        "/favicon.ico",
    )


def download_image(
    icon_url: str,
) -> bytes:
    """
    Download image data.
    """

    response = requests.get(
        icon_url,
        headers={
            "User-Agent": USER_AGENT
        },
        timeout=20,
    )

    response.raise_for_status()

    return response.content


def save_png(
    data: bytes,
    destination: Path,
):
    """
    Convert image to PNG.
    """

    image = Image.open(
        BytesIO(data)
    )

    image.save(
        destination,
        format="PNG",
    )


def create_fallback_icon(
    destination: Path,
):
    """
    Create a basic fallback icon.

    Used when a website has no usable icon.
    """

    image = Image.new(
        "RGBA",
        (512, 512),
        (0, 0, 0, 0),
    )

    image.save(
        destination,
        format="PNG",
    )


def download_icon(
    url: str,
    metadata,
    destination: Path,
) -> Path:
    """
    Download a website icon.

    The filename is controlled by the caller.

    Example:
        youtube-com.png

    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:

        soup = fetch_html(url)

        icon_url = choose_best_icon(
            soup,
            url,
        )

        if icon_url is None:
            raise RuntimeError(
                "No icon found."
            )

        print(
            f"Downloading icon: {icon_url}"
        )

        image = download_image(
            icon_url
        )

        save_png(
            image,
            destination,
        )

    except Exception as error:

        print(
            f"Warning: icon download failed: {error}"
        )

        create_fallback_icon(
            destination
        )

    return destination


if __name__ == "__main__":

    from metadata import get_metadata

    test_url = (
        "https://chat.openai.com"
    )

    metadata = get_metadata(
        test_url
    )

    icon = download_icon(
        test_url,
        metadata,
        Path("./icons/test.png"),
    )

    print(icon)
