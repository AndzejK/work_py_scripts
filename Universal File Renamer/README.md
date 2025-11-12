Universal File Renamer

Change file extensions in bulk, keeping any trailing numbers.
Example: error.log → error.txt, error.log2 → error.2.txt, error.log.2 → error.2.txt.

Why? Lots of systems roll logs like file.log.1, file.log2, etc. This script normalizes them to a new extension without losing the roll number.

---

What it does

- Finds files in a folder that match:
  - name.<old_ext>
  - name.<old_ext><number> (e.g., app.log2)
  - name.<old_ext>.<number> (e.g., app.log.2)
- Renames them to:
  - name.<new_ext>
  - name.<number>.<new_ext> (if a number exists)
- No overwrite: if the target exists, appends _1, _2, … to avoid collisions.
- Case-insensitive match of the old extension.
- Supports dry run so you can preview changes.

---

Quick start

# 1) Save the script
curl -O https://example.com/rename_files.py  # or copy it locally

# 2) Run a preview (no changes)
python3 rename_files.py /path/to/folder log txt --dry-run

# 3) Apply changes
python3 rename_files.py /path/to/folder log txt

---

Usage

python3 rename_files.py FOLDER OLD_EXT NEW_EXT [--dry-run]

Arguments
- FOLDER – directory to scan (non-recursive).
- OLD_EXT – current extension to match (with or without dot, e.g., log or .log).
- NEW_EXT – new extension to apply (e.g., txt or .txt).
- --dry-run – print planned renames without changing files.

Examples
# Rename .log, .log2, .log.2 → .txt / .2.txt
python3 rename_files.py ./logs log txt

# Preview only
python3 rename_files.py ./logs log txt --dry-run

# Turn backups like file.bak, file.bak.3 → file.backup, file.3.backup
python3 rename_files.py ./data bak backup

---

Matching rules (plain English)

- It looks for filenames like:
  - something.<old_ext>
  - something.<old_ext>2
  - something.<old_ext>.2
- If a number exists, it’s kept before the new extension:
  - something.log2 → something.2.txt
  - something.log.2 → something.2.txt
- If no number exists:
  - something.log → something.txt

---

Collision handling

If the target filename already exists, the script adds a suffix:
name.2.txt → name.2_1.txt, then name.2_2.txt, etc., until a free name is found.

---

Notes

- Works on macOS, Linux, and Windows (use py on Windows if needed).
- Operates only in the top level of the given folder (no recursion).
- Old and new extensions are normalized (a leading dot is optional).
- The script prints each rename, so you have an audit trail.

---

Why this design?

- Predictable: numbering is preserved in a consistent place.
- Safe: nothing is overwritten by accident.
- Fast to verify: --dry-run shows exactly what will happen.

---

Troubleshooting

- “No files matching …”
  Check OLD_EXT spelling and the folder path. Remember it matches by extension, not by MIME type.
- Weird names after renaming
  Some files may already include extra dots/numbers. The script keeps everything before <old_ext> as the base name; that’s expected.

---

License

Do whatever you want. A credit is nice, but not required.
