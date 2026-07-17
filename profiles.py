"""
profiles.py

Manage isolated browser profiles.
"""

from pathlib import Path


def create_profile(
    profile_path: Path,
):
    """
    Create an isolated browser profile directory.
    """

    profile_path.mkdir(
        parents=True,
        exist_ok=True,
    )


def remove_profile(
    profile_path: Path,
):
    """
    Remove an isolated browser profile directory.
    """

    if profile_path.exists():

        import shutil

        shutil.rmtree(
            profile_path,
            ignore_errors=True,
        )


def profile_exists(
    profile_path: Path,
) -> bool:
    """
    Check if a profile exists.
    """

    return profile_path.exists()


if __name__ == "__main__":

    test = Path(
        "./test-profile"
    )

    create_profile(test)

    print(
        f"Created profile: {test}"
    )

    print(
        f"Exists: {profile_exists(test)}"
    )

    remove_profile(test)

    print(
        "Removed profile"
    )
