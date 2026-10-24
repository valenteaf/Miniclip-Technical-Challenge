# Findings on new localisation file

The localisation file `localisations_1_2_1.plist` is not ready for usage.
Here are the issues from most to least urgent:

[CODE-BREAKING BUGS]

- Typo in which type 'B' options do not close square brackets for 1 language and 1 key;
(key 1981dc5a-a6b8-4fd3-be04-052522e08c86, lang. it)

- A replacement character `%u` is missing from 2 languages for 1 key;
(key 2b827952-8d1a-4c31-9283-8753d1fc51be, lang. fr)

- A type 'B' option is missing for a key for 1 language;
(key 1981dc5a-a6b8-4fd3-be04-052522e08c86, lang. tk)

- `es` language is missing from all keys;

[WRONG CONTENT BUGS]

- All type 'A' options are missing for a key for 1 language;
(key 1981dc5a-a6b8-4fd3-be04-052522e08c86, lang. it)

- One line completely gone for 1 line and 1 language;
(key 2b827952-8d1a-4c31-9283-8753d1fc51be, lang. it)

- Small typo for 1 key for pt-BR language (`video` should be `vídeo`).
(key d8225439-0a23-404c-857d-8cd37032a606)

# When this script shoud be run

I believe this script should be ran manually as part of the the development process of the localisation file.

An updated, streamlined version of the script should be implemented in a pipeline/CI of some kind, maybe as part of a merge-to-master check, to make sure no code-breaking bugs are present.
