import requests
from bs4 import BeautifulSoup
import json

URL = "https://up.codes/viewer/minnesota/ifc-2018/chapter/5/fire-service-features"

def debug_deeper():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    scripts = soup.find_all('script')
    
    for script in scripts:
        if script.string and "501.1 Scope" in script.string:
            try:
                data = json.loads(script.string)
                page_props = data.get('props', {}).get('pageProps', {})
                lean_data = page_props.get('leanChapterViewerData', {})
                tree = lean_data.get('leanCodeSectionsTree', [])
                
                if len(tree) > 0:
                    chapter = tree[0] # Chapter 5
                    if 'children' in chapter:
                        section_501 = chapter['children'][0] # Section 501
                        print(f"Section 501 Display Title: {section_501.get('displayTitle')}")
                        
                        if 'children' in section_501:
                            for child in section_501['children']:
                                print(f"  Subsection Display Title: {child.get('displayTitle')}")
                                print(f"  Subsection Title: {child.get('titleText')}")
                                # Check if number is separate
                                print(f"  Subsection Keys: {list(child.keys())}")
                                print("-" * 10)
                                
            except Exception as e:
                print(f"Error: {e}")
            break

if __name__ == "__main__":
    debug_deeper()
