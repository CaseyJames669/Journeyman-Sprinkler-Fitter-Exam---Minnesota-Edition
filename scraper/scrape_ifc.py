import requests
from bs4 import BeautifulSoup
import os
import time
import re
import json

BASE_URL = "https://up.codes"
INDEX_URL = "https://up.codes/viewer/minnesota/ifc-2018"
OUTPUT_DIR = "scraper/output/upcodes_ifc_2018"

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_index():
    print(f"Fetching index: {INDEX_URL}")
    soup = get_soup(INDEX_URL)
    if not soup:
        return []

    chapters = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if "/viewer/minnesota/ifc-2018/chapter/" in href:
            full_url = BASE_URL + href if href.startswith('/') else href
            title = a.get_text(strip=True)
            if full_url not in [c['url'] for c in chapters]:
                chapters.append({'title': title, 'url': full_url})
    
    return chapters

def parse_html_content(html_content):
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    content = []
    
    # Extract text with some formatting
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'table', 'div']):
        # Skip if inside a table (handled separately)
        if element.find_parent('table'):
            continue
            
        if element.name.startswith('h'):
            level = int(element.name[1])
            content.append(f"{'#' * level} {element.get_text(strip=True)}\n\n")
        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                content.append(f"{text}\n\n")
        elif element.name == 'ul':
            for li in element.find_all('li'):
                content.append(f"- {li.get_text(strip=True)}\n")
            content.append("\n")
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li'), 1):
                # Check if the li has a value attribute (common in codes)
                val = li.get('value')
                num = val if val else i
                content.append(f"{num}. {li.get_text(strip=True)}\n")
            content.append("\n")
        elif element.name == 'table':
            rows = element.find_all('tr')
            for row in rows:
                cols = [ele.get_text(strip=True) for ele in row.find_all(['th', 'td'])]
                content.append("| " + " | ".join(cols) + " |\n")
            content.append("\n")
        elif element.name == 'div':
             # Some text might be in divs without p tags
             # But be careful not to duplicate content if div contains p tags
             if not element.find('p') and not element.find('table') and not element.name.startswith('h'):
                 text = element.get_text(strip=True)
                 if text and len(text) > 20: # Heuristic to avoid small UI elements
                     content.append(f"{text}\n\n")

    return "".join(content)

def process_node(node, level=1):
    content = []
    
    # Extract body HTML
    body_html = node.get('body')
    if body_html:
        text = parse_html_content(body_html)
        if text:
            content.append(text)
    
    # Process children
    children = node.get('children', [])
    for child in children:
        content.append(process_node(child, level + 1))
        
    return "".join(content)

def scrape_chapter(chapter):
    url = chapter['url']
    title = chapter['title']
    print(f"Scraping {title}...")
    
    soup = get_soup(url)
    if not soup:
        return None

    # Find the __NEXT_DATA__ script
    script = soup.find('script', string=lambda t: t and "__NEXT_DATA__" in t)
    if not script:
        # Fallback to searching for any script with the content if ID missing
        # But usually it has an ID or is the one with the big JSON
        scripts = soup.find_all('script')
        for s in scripts:
            if s.string and "leanChapterViewerData" in s.string:
                script = s
                break
    
    if not script:
        print(f"Could not find data script for {title}")
        return None

    try:
        data = json.loads(script.string)
        page_props = data.get('props', {}).get('pageProps', {})
        lean_data = page_props.get('leanChapterViewerData', {})
        tree = lean_data.get('leanCodeSectionsTree', [])
        
        content = []
        content.append(f"# {title}\n\n")
        
        for node in tree:
            content.append(process_node(node))
            
        return "".join(content)
        
    except Exception as e:
        print(f"Error parsing data for {title}: {e}")
        return None

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    chapters = scrape_index()
    print(f"Found {len(chapters)} chapters.")

    all_content = []

    for i, chapter in enumerate(chapters):
        chapter_content = scrape_chapter(chapter)
        if chapter_content:
            filename = f"{i:02d}_{re.sub(r'[^a-zA-Z0-9]', '_', chapter['title'])}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(chapter_content)
            
            all_content.append(chapter_content)
            all_content.append("\n---\n\n")
        else:
            print(f"Failed to scrape content for {chapter['title']}")
        
        time.sleep(1) # Be polite

    full_filepath = os.path.join(OUTPUT_DIR, "IFC_2018_Full.md")
    with open(full_filepath, 'w', encoding='utf-8') as f:
        f.write("".join(all_content))
    
    print(f"Done. Saved to {full_filepath}")

if __name__ == "__main__":
    main()
