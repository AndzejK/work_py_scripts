#!/usr/bin/env python3
"""
Combine multiple text files from a directory into one master file.
"""

import argparse
from pathlib import Path
from datetime import datetime


def combine_files(source_dir, output_file, file_pattern="*", 
                  sort_by_date=True, encoding='utf-8', recursive=False):
    """
    Combine all matching files from a directory into one output file.
    
    Args:
        source_dir: Directory containing files to combine
        output_file: Path to the output file
        file_pattern: Pattern to match files (e.g., '*.txt', '*.log', '*')
        sort_by_date: If True, sort by creation date; if False, sort alphabetically
        encoding: Text encoding to use (default: utf-8)
        recursive: If True, search subdirectories as well
    
    Returns:
        Tuple of (files_processed, total_lines, success)
    """
    source_path = Path(source_dir)
    output_path = Path(output_file)
    
    # Validate source directory
    if not source_path.exists():
        print(f"Error: Directory '{source_dir}' does not exist.")
        return 0, 0, False
    
    if not source_path.is_dir():
        print(f"Error: '{source_dir}' is not a directory.")
        return 0, 0, False
    
    # Get list of files to process
    if recursive:
        files = list(source_path.rglob(file_pattern))
    else:
        files = list(source_path.glob(file_pattern))
    
    # Filter out directories and the output file itself
    files = [f for f in files if f.is_file() and f.resolve() != output_path.resolve()]
    
    # Sort files by creation date (oldest first) or alphabetically
    if sort_by_date:
        files.sort(key=lambda f: f.stat().st_ctime)
        sort_method = "creation date"
    else:
        files.sort()
        sort_method = "name"
    
    if not files:
        print(f"No files matching '{file_pattern}' found in {source_dir}")
        return 0, 0, False
    
    print(f"Found {len(files)} file(s) to combine (sorted by {sort_method})")
    print(f"Output file: {output_path}")
    print("-" * 60)
    
    files_processed = 0
    total_lines = 0
    
    try:
        with open(output_path, 'w', encoding=encoding) as outfile:
            # Write header
            outfile.write(f"Combined file created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write(f"Source directory: {source_path.absolute()}\n")
            outfile.write(f"Total files: {len(files)}\n")
            outfile.write(f"Sorted by: {sort_method}\n")
            outfile.write(f"Encoding: {encoding}\n")
            outfile.write("=" * 80 + "\n\n")
            
            for file_path in files:
                try:
                    # Read the file
                    with open(file_path, 'r', encoding=encoding, errors='replace') as infile:
                        content = infile.read()
                        lines = content.count('\n')
                    
                    # Get file metadata
                    file_stat = file_path.stat()
                    creation_time = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Write separator with file information
                    separator = f"\n{'=' * 80}\n"
                    separator += f"FILE: {file_path.name}\n"
                    separator += f"Path: {file_path.relative_to(source_path)}\n"
                    separator += f"Size: {file_stat.st_size:,} bytes\n"
                    separator += f"Lines: {lines:,}\n"
                    separator += f"Created: {creation_time}\n"
                    separator += f"{'=' * 80}\n\n"
                    outfile.write(separator)
                    
                    # Write the file content
                    outfile.write(content)
                    
                    # Ensure there's a newline at the end
                    if content and not content.endswith('\n'):
                        outfile.write('\n')
                    
                    files_processed += 1
                    total_lines += lines
                    
                    print(f"✓ Processed: {file_path.name} ({lines} lines)")
                    
                except UnicodeDecodeError:
                    print(f"✗ Skipped: {file_path.name} (encoding error - might be binary)")
                except Exception as e:
                    print(f"✗ Error reading {file_path.name}: {e}")
            
            # Write footer
            outfile.write(f"\n{'=' * 80}\n")
            outfile.write(f"End of combined file\n")
            outfile.write(f"Files processed: {files_processed}\n")
            outfile.write(f"Total lines: {total_lines}\n")
            outfile.write(f"={'=' * 80}\n")
    
    except Exception as e:
        print(f"Error writing output file: {e}")
        return files_processed, total_lines, False
    
    return files_processed, total_lines, True


def main():
    """Main function to parse arguments and execute file combining."""
    parser = argparse.ArgumentParser(
        description='Combine multiple text files into one master file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Combine all files in a directory (sorted by creation date)
  python combine_files.py /path/to/files combined.txt
  
  # Combine only .txt files
  python combine_files.py /path/to/files combined.txt --pattern "*.txt"
  
  # Combine files sorted alphabetically instead of by date
  python combine_files.py /path/to/files combined.txt --sort-by-name
  
  # Combine files from subdirectories too
  python combine_files.py /path/to/files combined.txt --recursive
  
  # Specify encoding for special characters
  python combine_files.py /path/to/files combined.txt --encoding "utf-16"
        """
    )
    
    parser.add_argument(
        'source_dir',
        help='Directory containing files to combine'
    )
    
    parser.add_argument(
        'output_file',
        help='Path to the output combined file'
    )
    
    parser.add_argument(
        '--pattern',
        default='*',
        help='File pattern to match (e.g., "*.txt", "*.log"). Default: * (all files)'
    )
    
    parser.add_argument(
        '--sort-by-name',
        action='store_true',
        help='Sort files alphabetically by name instead of by creation date'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='Text encoding to use (default: utf-8)'
    )
    
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Include files from subdirectories'
    )
    
    args = parser.parse_args()
    
    # Execute the combining
    files_count, lines_count, success = combine_files(
        source_dir=args.source_dir,
        output_file=args.output_file,
        file_pattern=args.pattern,
        sort_by_date=not args.sort_by_name,
        encoding=args.encoding,
        recursive=args.recursive
    )
    
    # Print summary
    print("-" * 60)
    if success:
        print(f"✓ Success! Combined {files_count} file(s) with {lines_count} total lines")
        print(f"  Output saved to: {args.output_file}")
    else:
        print("✗ Failed to combine files")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())