# Combine Files — Text Merger CLI

A tiny Python CLI that **combines multiple text files** from a directory into **one master file**, with per-file headers (name, path, size, line count, creation time) and a summary footer.

---

## Features

- Match files by **pattern** (e.g., `*.txt`, `*.log`, or `*` for all).
- Sort by **creation date** (default, oldest → newest) or **alphabetically**.
- **Recursive** mode to include subfolders.
- Handles encodings (default **UTF‑8**) and replaces invalid chars safely.
- Skips binaries (avoids decoding errors) and prints a per‑file status.
- Adds clear separators and metadata for each file.

---

## Installation

Requires Python 3.8+.

```bash
# Option A: run directly
python3 combine_files.py --help

# Option B: make it executable (macOS/Linux)
chmod +x combine_files.py
./combine_files.py --help
```

---

## Usage

```bash
python3 combine_files.py SOURCE_DIR OUTPUT_FILE [options]
```

### Positional arguments
- `SOURCE_DIR` — directory containing files to combine
- `OUTPUT_FILE` — path to the combined output file (e.g., `combined.txt`)

### Options
- `--pattern "<glob>"` — file pattern to match. Default: `*`  
  Examples: `--pattern "*.txt"`, `--pattern "*.log"`
- `--sort-by-name` — sort alphabetically instead of by creation date
- `--encoding ENC` — text encoding (default: `utf-8`), e.g., `utf-16`
- `--recursive` — include files from subdirectories

---

## Examples

```bash
# 1) Combine EVERYTHING in a folder (sorted by creation time)
python3 combine_files.py ./notes combined.txt

# 2) Only .txt files, alphabetically
python3 combine_files.py ./notes combined.txt --pattern "*.txt" --sort-by-name

# 3) Include subfolders (e.g., logs from nested dates)
python3 combine_files.py ./logs all-logs.txt --pattern "*.log" --recursive

# 4) Special encoding (Windows-1257 / Baltic)
python3 combine_files.py ./texts combined.txt --encoding "cp1257"
```

---

## Output format

The tool writes:

1. A **header** block (timestamp, source dir, total files, sort method, encoding)  
2. For each file:
   - Separator line
   - `FILE: <filename>`
   - `Path: <relative path>`
   - `Size: <bytes>`
   - `Lines: <count>`
   - `Created: <YYYY-MM-DD HH:MM:SS>`
   - Then the **file contents**
3. A **footer** with totals

This makes the master file easy to search, diff, and read.

---

## Tips

- To avoid including the output file in the merge, write it **outside** `SOURCE_DIR` or just keep the default behavior (the script already excludes the output file path).
- Creation time uses the filesystem’s `st_ctime` (on Unix it may be inode change time). If you need strict modification-time sorting, we can tweak it to `st_mtime`.
- If your data includes mixed encodings, stick to UTF‑8 when possible; otherwise use `--encoding` and the script will replace invalid bytes rather than crash.

---

## Exit codes

- `0` — success
- `1` — failed to combine (e.g., no files matched, write error)

---

## License

MIT‑ish. Use freely.
