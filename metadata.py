"""
metadata.py

Extract website metadata.
"""

from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 "
    "(X11; Linux x86_64) "
    "Chrome/138"
)


@dataclass
class WebsiteMetadata:
    """
    Website information.
    """

    name: str
    title: str
    icon_url: str | None


def get_metadata(
    url: str,
) -> WebsiteMetadata:
    """
    Extract website title and icon.
    """

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=15,
            allow_redirects=True,
        )

        response.encoding = (
            response.apparent_encoding
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        title = None


        #
        # Prefer OpenGraph metadata
        #

        og_title = soup.find(
            "meta",
            property="og:site_name",
        )

        if og_title:

            title = og_title.get(
                "content"
            )


        if not title:

            og_title = soup.find(
                "meta",
                property="og:title",
            )

            if og_title:

                title = og_title.get(
                    "content"
                )


        #
        # Fallback to HTML title
        #

        if not title and soup.title:

            title = soup.title.text


        if not title:

            title = url


        icon = urljoin(
            url,
            "/favicon.ico",
        )


        return WebsiteMetadata(
            name=title.strip(),
            title=title.strip(),
            icon_url=icon,
        )


    except Exception:

        return WebsiteMetadata(
            name=url,
            title=url,
            icon_url=None,
        )


if __name__ == "__main__":

    result = get_metadata(
        "https://youtube.com"
    )

    print(
        result
    )
