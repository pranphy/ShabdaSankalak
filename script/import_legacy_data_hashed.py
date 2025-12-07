import os
import json
import re
import hashlib
from pathlib import Path

def parse_legacy_file(file_path):
    """
    Parses a legacy text file to extract metadata and content.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from headers
    metadata = {}
    lines = content.split('\n')
    body_start_index = 0
    
    for i, line in enumerate(lines):
        if line.startswith('# url:'):
            metadata['url'] = line.replace('# url:', '').strip()
        elif line.startswith('# title :'):
            metadata['title'] = line.replace('# title :', '').strip()
        elif line.startswith('# date:'):
            metadata['date'] = line.replace('# date:', '').strip()
        elif line.startswith('# category:'):
            metadata['category'] = line.replace('# category:', '').strip()
        elif line.startswith('# author:'):
            metadata['author'] = line.replace('# author:', '').strip()
        elif not line.startswith('#'):
            body_start_index = i
            break
            
    # Extract body content
    body_content = '\n'.join(lines[body_start_index:])
    
    # Clean body content (remove googletag scripts)
    body_content = re.sub(r'googletag\.cmd\.push\(function\(\)\s*\{[\s\S]*?\}\);', '', body_content)
    
    # Replace non-breaking spaces with regular spaces
    body_content = body_content.replace('\u00a0', ' ')
    
    # Normalize whitespace
    body_content = body_content.strip()
    
    place = ''
    # Check for place delimiter (em dash '—') in the first few characters
    if '—' in body_content[:100]:
        parts = body_content.split('—', 1)
        place = parts[0].strip()
        body_content = parts[1].strip()
    
    return {
        'url': metadata.get('url', ''),
        'title': metadata.get('title', ''),
        'date': metadata.get('date', ''),
        'author': metadata.get('author', ''),
        'category': metadata.get('category', ''),
        'place': place,
        'content': body_content
    }

def main():
    source_dir = Path.home() / 'repos/ShabdaSankalak/scrapped/ag/kantipur'
    output_base_dir = Path('data')
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Scanning {source_dir}...")
    
    count = 0
    for file_path in source_dir.rglob('*.txt'):
        if file_path.is_file():
            try:
                article = parse_legacy_file(file_path)
                url = article['url']
                if url:
                    url = url.strip()
                    # Generate MD5 hash of the trimmed URL
                    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
                    
                    # Extract year and month from URL
                    # Expected format: .../YYYY/MM/DD/...
                    match = re.search(r'/(\d{4})/(\d{2})/\d{2}/', url)
                    if match:
                        year, month = match.groups()
                        month_dir = output_base_dir / f"{year}-{month}"
                        month_dir.mkdir(parents=True, exist_ok=True)
                        output_path = month_dir / f"{url_hash}.json"
                        
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(article, f, ensure_ascii=False, indent=2)
                        count += 1
                    else:
                        # Fallback if date not found in URL, maybe use date field or put in 'unknown'
                        # For now, let's log it and skip or put in 'misc'
                        # print(f"Could not extract date from URL: {url}")
                        pass
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    print(f"Saved {count} articles to {output_base_dir}.")

if __name__ == '__main__':
    main()
