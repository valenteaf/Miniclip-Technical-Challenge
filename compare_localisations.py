"""Load localisation dictionaries from an older and a newer plist file."""

from __future__ import annotations

import argparse
import plistlib
from pathlib import Path


def load_localisations(path: str | Path) -> dict:
    """ Return the `localisations` dictionary from a plist file. """
    plist_path = Path(path)
    if not plist_path.is_file():
        raise FileNotFoundError(f"Plist file not found: {plist_path}")

    with plist_path.open("rb") as handle:
        data = plistlib.load(handle)

    if not isinstance(data, dict) or "localisations" not in data:
        raise KeyError(f"Missing 'localisations' dictionary in {plist_path}")

    localisations = data["localisations"]
    if not isinstance(localisations, dict):
        raise TypeError(f"'localisations' in {plist_path} is not a dictionary")

    return localisations


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """ Parses the command line arguments. Should be 2 arguments: the path to the older and the newer localisation plist files. """
    parser = argparse.ArgumentParser(
        description="Load localisation dictionaries from an older and a newer plist file."
    )
    parser.add_argument(
        "older",
        type=Path,
        help="Path to the older localisation plist.",
    )
    parser.add_argument(
        "newer",
        type=Path,
        help="Path to the newer localisation plist.",
    )
    return parser.parse_args(argv)

def get_new_keys(older: dict, newer: dict) -> list[str]:
    """ Returns any new keys not present in the older localisation dictionary """ 
    return [key for key in newer if key not in older]

def get_missing_keys(older: dict, newer: dict) -> list[str]:
    """ Returns any keys not present in the newer localisation dictionary """ 
    return [key for key in older if key not in newer]

def new_keys(older: dict, newer: dict):
    print("")


def main(argv: list[str] | None = None) -> dict[str, dict]:
    args = parse_args(argv)

    older = load_localisations(args.older)
    newer = load_localisations(args.newer)

    print(get_new_keys(older, newer))
    print(get_missing_keys(older, newer))


if __name__ == "__main__":
    main()
