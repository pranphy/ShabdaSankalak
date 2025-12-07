import os
import json
import re
from pathlib import Path
from collections import defaultdict

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
    # The pattern looks like: googletag.cmd.push(function() { ... });
    # We can use regex to remove these blocks.
    # Note: The sample showed these scripts inline.
    
    # Remove googletag blocks
    body_content = re.sub(r'googletag\.cmd\.push\(function\(\)\s*\{[\s\S]*?\}\);', '', body_content)
    
    # Remove other potential ad scripts or artifacts if any (based on sample)
    # The sample had: googletag.defineSlot...
    # The regex above should catch the push(function() {...}) blocks.
    # Let's also be safe and remove lines that look like code if they remain.
    
    # Replace non-breaking spaces with regular spaces
    body_content = body_content.replace('\u00a0', ' ')
    
    # Normalize whitespace
    body_content = body_content.strip()
    
    place = ''
    # Check for place delimiter (em dash '—') in the first few characters
    # Some articles might use hyphen or en dash, but user specified em dash.
    # Let's look for it in the first 100 characters to be safe.
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
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)
    
    articles_by_month = defaultdict(list)
    
    print(f"Scanning {source_dir}...")
    
    for file_path in source_dir.rglob('*.txt'):
        if file_path.is_file():
            try:
                article = parse_legacy_file(file_path)
                if article['url']: # Basic check if it's a valid article
                    # Extract year and month from file path or date
                    # Path format: .../year/month/day/category/file.txt
                    # We can use the path parts.
                    # source_dir is .../kantipur
                    # file_path relative to source_dir: year/month/day/category/file.txt
                    
                    rel_path = file_path.relative_to(source_dir)
                    parts = rel_path.parts
                    
                    if len(parts) >= 2:
                        year = parts[0]
                        month = parts[1]
                        
                        # Validate year and month are digits
                        if year.isdigit() and month.isdigit():
                            key = f"kantipur_{year}_{month}.json"
                            articles_by_month[key].append(article)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    print(f"Found {sum(len(v) for v in articles_by_month.values())} articles.")
    
    for filename, articles in articles_by_month.items():
        output_path = output_dir / filename
        print(f"Saving {len(articles)} articles to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
