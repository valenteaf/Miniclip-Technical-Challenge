"""
Compares localisation dictionaries from an older and a newer plist file.
    
    Usage:
        python compare_localisations.py path/to/older/file.plist path/to/newer/file.plist
        python compare_localisations.py path/to/older/file.plist path/to/newer/file.plist --console
"""
from __future__ import annotations

import argparse
import builtins
import plistlib
from pathlib import Path
import re
from collections import Counter

# VARIABLES
MAX_LINE_SIZE_THRESHOLD = 0
PLACEHOLDERS_TO_CHECK = [f"%@", f"%u", f"A:[", f"B:[", "]"] # includes options starter and ender
REPORT_PATH = Path("comparison_report.txt")

_report_file = None
_print_to_console = False


def report_print(*args, to_console: bool | None = None, **kwargs) -> None:
    """Write to comparison_report.txt, and optionally also to the command line.

    `to_console` overrides the default set by `--console` / `--no-console`.
    """
    echo = _print_to_console if to_console is None else to_console
    if _report_file is not None:
        builtins.print(*args, **kwargs, file=_report_file)
    if echo:
        builtins.print(*args, **kwargs)

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
    parser.add_argument(
        "--console",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Also print the report to the command line (default: false). Use --console to echo the report.",
    )
    return parser.parse_args(argv)

def get_new_keys(older: dict, newer: dict) -> list[str]:
    """ Returns any new keys not present in the older localisation dictionary """ 
    return [key for key in newer if key not in older]

def print_new_keys(new_keys: list[str]):
    report_print("1) NEW KEYS: (only present in newer file)")
    if new_keys:
        for key in new_keys:
            report_print(f"- {key};")
    else:
        report_print("   None.")
    report_print("")

def get_missing_keys(older: dict, newer: dict) -> list[str]:
    """ Returns any keys not present in the newer localisation dictionary """ 
    return [key for key in older if key not in newer]

def print_missing_keys(missing_keys: list[str]):
    report_print("2) MISSING KEYS: (only present in older file)")
    if missing_keys:
        for key in missing_keys:
            report_print(f"- {key};")
    else:
        report_print("   None.")
    report_print("")

def print_versions(older_name: str, older_version: str, newer_name: str, newer_version: str):
    report_print(f"> OLDER FILE: {older_name} ({older_version});\n> NEWER FILE: {newer_name} ({newer_version});\n")

def print_internal_missing_placeholders(older: dict, newer: dict, missing_placeholders: list[str] = [f"%@", f"%u"]):
    """ Print the missing placeholders of each localisation file. """

    report_print(f"3) MISSING PLACEHOLDERS for EACH FILE:")
    report_print(f"   Possible missing placeholders: {missing_placeholders}\n")

    report_print(f"   3.1) OLDER FILE:")
    print_missing_placeholders_for_each_file(older, missing_placeholders)

    report_print(f"\n   3.2) NEWER FILE:")
    print_missing_placeholders_for_each_file(newer, missing_placeholders)

    report_print("")

def print_missing_placeholders_for_each_file(file: dict, missing_placeholders: list[str]):
    for key in file.keys():
        for placeholder in missing_placeholders:
            missing = get_keys_w_missing_placeholder(file[key], placeholder)
            if missing:
                report_print(f"       - {key}: {missing} (missing '{placeholder}');")

def get_keys_w_missing_placeholder(strings: dict, placeholder: str) -> list[str]:
    """ Returns the strings with the missing placeholders, if any string includes said placeholder. """

    strings_use_placeholder = any(placeholder in value for value in strings.values())

    if strings_use_placeholder:
        return [key for key, value in strings.items() if placeholder not in value]

def get_missing_languages(file: dict, all_languages: list[str]) -> list[str]:
    return [(key, [lang for lang in all_languages if lang not in value]) 
        for key, value in file.items()
        if any(lang not in value for lang in all_languages)]

def get_language_list(file: dict) -> list[str]:
    """ Returns the list of languages present in the localisation files. """
    return list({lang for translations in file.values() for lang in translations})

def get_new_languages(older: dict, newer: dict) -> list[str]:
    return [lang for lang in get_language_list(newer) if lang not in get_language_list(older)]

def get_removed_languages(older: dict, newer: dict) -> list[str]:
    return [lang for lang in get_language_list(older) if lang not in get_language_list(newer)]

def print_languages(older: dict, newer: dict):
    report_print("4) LANGUAGES:")
    report_print(f"   All languages present: {set(get_language_list(older) + get_language_list(newer))}\n")

    report_print(f"   4.1) NEW LANGUAGES: (only present in newer file)")
    new_languages = get_new_languages(older, newer)
    if new_languages:
        report_print(f"   {new_languages}")
    else:
        report_print("   None.")
    report_print("")

    report_print(f"   4.2) REMOVED LANGUAGES: (only present in older file)")
    removed_languages = get_removed_languages(older, newer)
    if removed_languages:
        report_print(f"   {removed_languages}")
    else:
        report_print("   None.")
    report_print("")

    report_print(f"   4.3) MISSING LANGUAGES for OLDER FILE per KEY: ")
    missing_languages_old = get_missing_languages(older, get_language_list(older))
    if missing_languages_old:
        for key, langs in missing_languages_old:
            report_print(f"   - {key}: {langs}")
    else:
        report_print("   None.")
    report_print("")

    report_print(f"   4.3) MISSING LANGUAGES for NEWER FILE per KEY: ")
    missing_languages_new = get_missing_languages(newer, get_language_list(newer))
    if missing_languages_new:
        for key, langs in missing_languages_new:
            report_print(f"   - {key}: {langs}")
    else:
        report_print("   None.")
    report_print("")

def print_missing_options(older: dict, newer: dict):
    report_print("5) MISSING OPTIONS:")
    #report_print(f"   5.1) Between files:")
    #print_different_options(older, newer)
    report_print(f"\n   5.1) In each file:")
    report_print(f"\n      5.1.1) IN OLDER FILE:")
    print_missing_options_for_each_file(older)
    report_print(f"\n      5.1.2) IN NEWER FILE:")
    print_missing_options_for_each_file(newer)
    report_print("")

#def print_different_options(older: dict, newer: dict):
#    ''' Between the older and newer files, print the different option types (A, B, ...) and the number of options for each type, if it is different. '''

def print_missing_options_for_each_file(file: dict):
    ''' Print the missing 'options' (A and B) for each file. '''
    ''' For each key and language, find how many A or B options (how many '/' are in each option), and compare them to the most common number of options, for each type of option. '''
    any_found = False
    for key, values in file.items():
        nb_options_A = []
        nb_options_B = []
        for lang, string in values.items():
            # For each language, find how many A or B options (how many / are in each option)
            if ":[" in string:
                options_A = re.findall(r"A:\[([^\]]*)\]", string)
                options_B = re.findall(r"B:\[([^\]]*)\]", string)
                if options_A:
                    if len(options_A) == 1:
                        nb_options_A.append((lang, len(options_A[0].split("/"))))
                    else:
                        report_print(f"      - {key}: {lang} - Too many A options found: {len(options_A)};")
                if options_B:
                    if len(options_B) == 1: 
                            nb_options_B.append((lang, len(options_B[0].split("/"))))
                    else:
                        report_print(f"      - {key}: {lang} - Too many B options found: {len(options_B)};")

        # Compare to most common number of /
        if nb_options_A and len({n for _, n in nb_options_A}) != 1:
            most_common_value, how_often = Counter([n for _, n in nb_options_A]).most_common(1)[0]
            for lang, nb_options in nb_options_A:
                if nb_options != most_common_value:
                    report_print(f"      - {key}: {lang} - {nb_options} A options -> should be {most_common_value} A options;")
                    any_found = True
        if nb_options_B and len({n for _, n in nb_options_B}) != 1:
            most_common_value, how_often = Counter([n for _, n in nb_options_B]).most_common(1)[0]
            for lang, nb_options in nb_options_B:
                if nb_options != most_common_value:
                    report_print(f"      - {key}: {lang} - {nb_options} B options -> should be {most_common_value} B options;")
                    any_found = True

    if not any_found:
        report_print("      None.")

def print_size_changes(older: dict, newer: dict, line_size_threshold: int = 0):
    report_print("6) SIZE CHANGES: (for existing keys)")

    # Compare sizes between lines for the same file, if a standard max line size or line nb. for each key is given
    
    # Compare old sizings with new sizings for existing keys
    print_size_changes_between_files(older, newer, line_size_threshold)

    report_print("")

def print_size_changes_between_files(older: dict, newer: dict, line_size_threshold: int):
    ''' Compares sizes of string between files for the same key and language '''
    any_found = False
    for key, values in older.items():
        if key in newer:
            for lang, old_value in values.items():
                if lang in newer[key] and old_value != newer[key][lang]:
                    old_value_lines = old_value.splitlines()
                    new_value_lines = newer[key][lang].splitlines()
                   
                   # Check if nb. of lines is the same
                    if len(old_value_lines) != len(new_value_lines):
                        report_print(f"   - {key}: {lang} - Old nb. lines: {len(old_value_lines)} -> New nb. lines: {len(new_value_lines)}")
                        any_found = True
                    
                    # Check if size of lines is the same within a certain threshold
                    for i in range(len(old_value_lines)):
                        if i < len(new_value_lines) and abs(len(old_value_lines[i]) - len(new_value_lines[i])) > line_size_threshold:
                            report_print(f"   - {key}: {lang} (line {i}) - Old size: {len(old_value_lines[i])} -> New size: {len(new_value_lines[i])}")
                            any_found = True

    if not any_found:
        report_print("   None.")

def print_text_changes(older: dict, newer: dict):
    report_print("7) ALL TEXT CHANGES: (for existing keys and languages)")
    report_print("  (- key: language - old text -> new text)\n")

    any_found = False
    
    for key, values in older.items():
        if key in newer:
            for lang, value in values.items():
                if lang in newer[key] and value != newer[key][lang]:
                    report_print(f"   - {key}: {lang} - {value} -> {newer[key][lang]}")
                    any_found = True
    
    if not any_found:
        report_print("   None.")

    report_print("")

def main(argv: list[str] | None = None) -> dict[str, dict]:
    global _report_file, _print_to_console
    args = parse_args(argv)
    _print_to_console = args.console

    with REPORT_PATH.open("w", encoding="utf-8") as report_file:
        _report_file = report_file

        report_print("\n------------------- LOCALISATION FILE COMPARER TOOL ------------------- \n")

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

        print_internal_missing_placeholders(older, newer, PLACEHOLDERS_TO_CHECK)

        print_languages(older, newer)

        print_missing_options(older, newer)

        print_size_changes(older, newer, MAX_LINE_SIZE_THRESHOLD)

        print_text_changes(older, newer)

    _report_file = None


if __name__ == "__main__":
    main()
