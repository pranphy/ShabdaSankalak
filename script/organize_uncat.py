import os
import json
import re
import shutil
from pathlib import Path

def organize_uncat_files():
    uncat_dir = Path("data/uncat")
    skipped_file_path = uncat_dir / "skipped.txt"
    
    # Ensure uncat directory exists
    if not uncat_dir.exists():
        print(f"Directory {uncat_dir} does not exist.")
        return

    # Regex to extract date from URL: .../YYYY/MM/DD/...
    # Example: https://ekantipur.com/pradesh-4/2025/10/15/14-prisoners-arrested-after-escaping-from-gorkha-prison-13-33.html
    date_pattern = re.compile(r'/(\d{4})/(\d{2})/\d{2}/')

    files_processed = 0
    files_moved = 0
    files_skipped = 0

    skipped_files = []

    for file_path in uncat_dir.glob("*.json"):
        files_processed += 1
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            url = data.get('url')
            if not url:
                print(f"No URL found in {file_path.name}, skipping.")
                continue

            match = date_pattern.search(url)
            if match:
                year = match.group(1)
                month = match.group(2)
                
                target_dir = Path(f"data/{year}-{month}")
                target_dir.mkdir(parents=True, exist_ok=True)
                
                target_file_path = target_dir / file_path.name
                
                if target_file_path.exists():
                    skipped_files.append(file_path.name)
                    files_skipped += 1
                    # print(f"File {file_path.name} already exists in {target_dir}, skipping.")
                else:
                    shutil.move(str(file_path), str(target_file_path))
                    files_moved += 1
                    # print(f"Moved {file_path.name} to {target_dir}")
            else:
                # print(f"Could not extract date from URL in {file_path.name}: {url}")
                pass

        except json.JSONDecodeError:
            print(f"Error decoding JSON in {file_path.name}, skipping.")
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    if skipped_files:
        with open(skipped_file_path, 'a', encoding='utf-8') as f:
            for filename in skipped_files:
                f.write(filename + '\n')
        print(f"Logged {len(skipped_files)} skipped files to {skipped_file_path}")

    print(f"Processing complete.")
    print(f"Total files processed: {files_processed}")
    print(f"Files moved: {files_moved}")
    print(f"Files skipped (duplicates): {files_skipped}")

if __name__ == "__main__":
    organize_uncat_files()
