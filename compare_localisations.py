"""
Compares localisation dictionaries from an older and a newer plist file.
    
    Usage:
        python compare_localisations.py path/to/older/file.plist path/to/newer/file.plist
"""

from __future__ import annotations

import argparse
import plistlib
from pathlib import Path


def load_plist(path: str | Path) -> dict:
    """ Return the root dictionary from a localisation plist file. """
    plist_path = Path(path)
    if not plist_path.is_file():
        raise FileNotFoundError(f"Plist file not found: {plist_path}")

    with plist_path.open("rb") as handle:
        data = plistlib.load(handle)

    if not isinstance(data, dict):
        raise TypeError(f"Root of {plist_path} is not a dictionary")

    return data


def load_localisations(path: str | Path) -> dict:
    """ Return the `localisations` dictionary from a plist file. """
    plist_path = Path(path)
    data = load_plist(plist_path)

    if "localisations" not in data:
        raise KeyError(f"Missing 'localisations' dictionary in {plist_path}")

    localisations = data["localisations"]
    if not isinstance(localisations, dict):
        raise TypeError(f"'localisations' in {plist_path} is not a dictionary")

    return localisations


def load_version(path: str | Path) -> str:
    """ Return the `version` string from a localisation plist file. """
    plist_path = Path(path)
    data = load_plist(plist_path)

    if "version" not in data:
        raise KeyError(f"Missing 'version' in {plist_path}")

    version = data["version"]
    if not isinstance(version, str):
        raise TypeError(f"'version' in {plist_path} is not a string")

    return version


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

def print_new_keys(new_keys: list[str]):
    print("1) NEW KEYS: (only present in newer file)")
    if new_keys:
        for key in new_keys:
            print(f"- {key};")
    else:
        print("   None.")
    print("")

def get_missing_keys(older: dict, newer: dict) -> list[str]:
    """ Returns any keys not present in the newer localisation dictionary """ 
    return [key for key in older if key not in newer]

def print_missing_keys(missing_keys: list[str]):
    print("2) MISSING KEYS: (only present in older file)")
    if missing_keys:
        for key in missing_keys:
            print(f"- {key};")
    else:
        print("   None.")
    print("")

def print_versions(older_name: str, older_version: str, newer_name: str, newer_version: str):
    print(f"> OLDER FILE: {older_name} ({older_version});\n> NEWER FILE: {newer_name} ({newer_version});\n")

def main(argv: list[str] | None = None) -> dict[str, dict]:
    args = parse_args(argv)

    print("\n------------------- LOCALISATION FILE COMPARER TOOL ------------------- \n")

    older_name = args.older.name
    older_version = load_version(args.older)
    newer_name = args.newer.name
    newer_version = load_version(args.newer)

    print_versions(older_name, older_version, newer_name, newer_version)

    older = load_localisations(args.older)
    newer = load_localisations(args.newer)

    new_keys = get_new_keys(older, newer)
    missing_keys = get_missing_keys(older, newer)

    print_new_keys(new_keys)
    print_missing_keys(missing_keys)


if __name__ == "__main__":
    main()
