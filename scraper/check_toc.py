import requests
from bs4 import BeautifulSoup

url = "https://codes.iccsafe.org/content/MNFC2020P1"
try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try to find links that look like chapters
    links = soup.find_all('a')
    chapter_links = []
    for link in links:
        href = link.get('href')
        if href and 'MNFC2020P1/chapter' in href:
            chapter_links.append(href)
            
    print(f"Found {len(chapter_links)} chapter links.")
    for link in chapter_links[:5]:
        print(link)
        
except Exception as e:
    print(f"Error: {e}")
