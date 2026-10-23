# Introduction

The purpose of this exercise and repo is to compare two localisation '.plist' files with one another and identify bugs in either file.

This would greatly facilitate the update process for a localisation file for a new release, as problems would be easily identified and a new file could be validated quickly against its older version.

This repo includes a simple Python script, 'compare_localisations.py', that compares two localisation .plist files with one another and attempts to identify possible bugs in either file.

# How to use

To run the script, simply run this command on your command line:

```
python compare_localisations.py path/to/older/file.plist path/to/newer/file.plist
```

# Output

A number of potential issues is flagged by the script.

When the script is ran, a short report is printed on the command line with the number of each kind of potential bug.

A longer, more verbose report, specifying each potential bug, is produced and written in a .txt file called 'comparison_report.md'.

# Potential issues

A number of potential issues can be identified in each .plist file, whether those are issues with the file itself and its strings in relation to each other, or issues when comparing the newer .plist file to the older one.

To find these issues, I took the following steps:

1. Identify new keys:
New keys (that were absent in the old localisation file) can be present in the new file. 
This is probably not a bug, but still worth pointing out.

2. Identify missing keys;
Keys present in the old localisation file can be missing in the new file. 
This has the potential to be a bug.

3. Identify missing information in either file separately:

    a. Missing `%@`, `%u` placeholders:
    For the same key, these substrings might be missing in certain languages.
    This is very likely a bug.

    b. Missing language:
    For the same file and same key, all languages should be present.
    If one is missing, it is very likely a bug.

    c. Missing "options" (that is, 'A:[.../.../...]', 'B:[...]', etc):
    For the same key, it is important to check if all languages include the 'A:[', 'B:[' and ']' characters (that is, the options start and end characters), if they are supposed to.
    Then, it is important to check if the number of options (that is, the number of '/' characters in between '[]') is the same for the same key across languages.
    These are both very likely bugs.

4. Identify new or missing languages between files:
If a language from either file is completely missing from either file, it could be a bug.

5. Identify missing options between files:

6. Identify changes in size of text (number of newlines or size of each line) between files:
If the size of the text changes significantly (above a certain threshold), the text might fit awkwardly in its location, and might be worth pointing out.

7. Identify all text changes (for each key and language) between files:
These will include all differences in the string for the same key and language (and thus won't catch new or missing keys or languages), and serve as a catch-all for debugging previously-existing keys. 
They will include previously caught bugs, like missing placeholder characters.

# To-do: Future work and improvements

- Create separate file verbose report;
- Create short warnings report;
- Currently not checking for several placeholders in a string; if there should be more than one placeholder in a string but there is only one, the script will not accuse it of being wrong;
- Create possible spelling/punctuation checker (like the typo in vídeo -> video);
- Compare line sizes for each file, if a standard maximum line size or number of lines for each key is given;
- Extend the search for the 'options' starter characters ('A:[', 'B:[') for all possible letters, possibly with regex;

# Risk analysis

In my opinion, the biggest risk with running this script to analyze a new localisation file is the script missing a number of bugs that may exist in the localisation file, namely:

- Spelling/punctuaction errors on new keys and languages;
- A string for a new key being too large (too many line breaks/too lengthy lines), as no maximum size per key is provided;