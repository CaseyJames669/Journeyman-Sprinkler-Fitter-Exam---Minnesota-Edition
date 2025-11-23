import requests
from bs4 import BeautifulSoup

url = "https://codes.iccsafe.org/content/MNFC2020P1/chapter-1-scope-and-administration"
try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check for some content that should be there
    # "SECTION 101 SCOPE AND GENERAL REQUIREMENTS"
    if "SECTION 101" in soup.text:
        print("Found 'SECTION 101' in content.")
    else:
        print("Did not find 'SECTION 101' in content.")
        
    # Print a snippet of the text
    print(soup.text[:500])
        
except Exception as e:
    print(f"Error: {e}")
