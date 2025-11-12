#!/usr/bin/env python3
"""
Universal file renaming script that changes file extensions with optional numbering.
Examples:
  # Rename .log/.log2/.log.2 -> .txt (keeping the number before the new ext)
  python rename_files.py /path/to/folder log txt

  # Preview changes
  python rename_files.py /path/to/folder log txt --dry-run
"""

import argparse
import re
from pathlib import Path


def rename_files(folder_path, old_ext, new_ext, dry_run=False):
    """
    Rename files in the specified folder from old extension to new extension.

    Args:
        folder_path: Path to the folder containing files to rename
        old_ext: Original extension to match (e.g., 'log')
        new_ext: New extension to apply (e.g., 'txt')
        dry_run: If True, only show what would be renamed without actually renaming

    Returns:
        Number of files renamed (or would be renamed in dry-run mode)
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return 0
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return 0

    old_ext = old_ext.lstrip('.')
    new_ext = new_ext.lstrip('.')

    # Matches:
    #   name.log
    #   name.log2
    #   name.log.2
    # Captures base name and optional number
    pattern = re.compile(
        rf'^(.+)\.{re.escape(old_ext)}(?:\.?(\d+))?$', re.IGNORECASE
    )

    renamed_count = 0

    for file_path in sorted(folder.iterdir()):
        if not file_path.is_file():
            continue

        m = pattern.match(file_path.name)
        if not m:
            continue

        base_name, number = m.group(1), m.group(2)

        if number:
            new_name = f"{base_name}.{number}.{new_ext}"
        else:
            new_name = f"{base_name}.{new_ext}"

        target = folder / new_name

        # Avoid overwrite: add a numeric suffix if needed
        if target.exists():
            stem = target.stem
            suffix = target.suffix  # includes the dot
            i = 1
            while True:
                candidate = folder / f"{stem}_{i}{suffix}"
                if not candidate.exists():
                    target = candidate
                    break
                i += 1

        prefix = "[DRY RUN] " if dry_run else ""
        print(f"{prefix}Renaming: {file_path.name} -> {target.name}")

        if not dry_run:
            try:
                file_path.rename(target)
                renamed_count += 1
            except Exception as e:
                print(f"  Error renaming {file_path.name}: {e}")
        else:
            renamed_count += 1

    return renamed_count


def main():
    parser = argparse.ArgumentParser(
        description='Rename files with specific extensions in a folder.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('folder', help='Path to the folder containing files to rename')
    parser.add_argument('old_ext', help='Current file extension to match (e.g., log, bak)')
    parser.add_argument('new_ext', help='New file extension to apply (e.g., txt, backup)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be renamed without actually renaming files')
    args = parser.parse_args()

    count = rename_files(args.folder, args.old_ext, args.new_ext, args.dry_run)

    action = "would be renamed" if args.dry_run else "renamed"
    if count:
        print(f"\nTotal: {count} file(s) {action}")
    else:
        print(f"\nNo files matching '*.{args.old_ext}*' found in {args.folder}")


if __name__ == "__main__":
    main()
