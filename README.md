# Potential issues

1. Identify new keys;
2. Identify missing keys;
3. Identify bugs in either file:
    a. Missing `%@`, `%u` placeholders;
    b. Missing language;
    c. Missing option in [];
4. New size of text differs much from the previous size:
    a. Check nb. of newlines;
    b. Check size of each line;
5. Text changes for each key;

# To-do

- Create separate file verbose report;
- Create short warnings report;
- Currently not checking for several placeholders in a string; if there should be more than one placeholder in a string but there is only one, the script will not accuse it of being wrong;
- Create possible spelling/punctuation checker (like the typo in vídeo -> video);
- Compare sizes between lines for the same file, if a standard maximum line size or number of lines for each key is given;
- Extend the search for the 'options' starter characters ("A:[", "B:[") for all possible letters, possibly with regex;