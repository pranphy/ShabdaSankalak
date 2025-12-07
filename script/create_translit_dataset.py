import json
import subprocess
import os
import re
from tqdm import tqdm

def get_transliteration(text):
    """
    Transliterates the given Nepali text using the 'uasc' tool.
    """
    try:
        # Assuming utasc takes input from stdin and outputs to stdout
        # Adjust arguments if utasc works differently (e.g. -i input -o output)
        # uasc takes input as argument
        process = subprocess.Popen(
            ['uasc', text], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error transliterating: {stderr}")
            return None
            
        return stdout.strip()
    except FileNotFoundError:
        print("Error: 'utasc' tool not found in PATH.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def split_sentences(text):
    """
    Splits Nepali text into sentences based on punctuation ?, ।, and |.
    """
    # Regex to split by ?, ।, |, or \n
    sentences = re.split(r'[?।|\n]', text)
    return [s.strip() for s in sentences if s.strip()]

def main():
    input_file = 'articles_clean.json'
    output_file = 'transliterated_dataset.json'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    output_data = []
    
    print("Processing articles...")
    # Using a small subset for testing if needed, but processing all for now
    for article in tqdm(data):
        content = article.get('content', '')
        if not content:
            continue
            
        sentences = split_sentences(content)
        
        for sentence in sentences:
            translit = get_transliteration(sentence)
            if translit:
                output_data.append({
                    'translit': translit,
                    'devanagari': sentence
                })
    
    print(f"Saving {len(output_data)} sentences to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("Done.")

if __name__ == '__main__':
    main()
