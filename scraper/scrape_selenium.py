import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_chapters():
    # Load chapters
    with open("scraper/chapters.json", "r") as f:
        chapters = json.load(f)

    # Setup Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    output_file = "scraper/output/full_text.md"
    
    # Check what we've already scraped to resume if needed
    # (Simple check: if file exists, we might be appending, but for now let's just start after the ones we know we did if we want, 
    # or just overwrite/append. The user wants the whole book. 
    # I already did 8 chapters manually/via subagent. 
    # But to be safe and consistent, I'll just scrape everything or check if I should skip.)
    
    # Let's just append to the file. 
    # If the file exists, we might want to clear it if we are starting fresh, 
    # but I already have some content there.
    # Actually, the user wants the *entire* book. 
    # I have batch 1 (3 chapters) in full_text.md.
    # I have batch 2 (5 chapters) in batch_2.json (truncated).
    # I should probably just re-scrape everything to be sure I get it all clean and consistent.
    # It's 89 chapters. It won't take too long with selenium.
    
    # Let's overwrite the file to start fresh and ensure consistency.
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Minnesota Fire Code 2020\n\n")

    print(f"Starting scrape of {len(chapters)} chapters...")
    
    try:
        for i, chapter in enumerate(chapters):
            url = chapter['url']
            title = chapter['title']
            print(f"[{i+1}/{len(chapters)}] Scraping: {title}")
            
            try:
                driver.get(url)
                
                # Wait for main content
                # The content is usually in 'main' tag
                wait = WebDriverWait(driver, 10)
                main_elem = wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
                
                # Give it a little extra time for dynamic content to settle
                time.sleep(2)
                
                # Extract text
                # We want to remove the sidebar text if it's included in main's innerText
                # The sidebar has id 'chapter-wrapper'
                
                content = driver.execute_script("""
                    const main = document.querySelector('main');
                    const sidebar = document.getElementById('chapter-wrapper');
                    const breadcrumbs = document.querySelector('.v-toolbar__content');
                    
                    if (!main) return "Error: No main element";
                    
                    // Clone the node to modify it without affecting the page (though we are scraping so it doesn't matter)
                    // Actually, innerText is computed.
                    // Let's just get the text and do string replacement if needed, 
                    // or better, hide the sidebar and then get text.
                    
                    if (sidebar) sidebar.style.display = 'none';
                    if (breadcrumbs) breadcrumbs.style.display = 'none';
                    
                    return main.innerText;
                """)
                
                # Clean up whitespace
                content = content.strip()
                
                # Append to file
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"## [{title}]({url})\n\n")
                    f.write(content)
                    f.write("\n\n---\n\n")
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"## [{title}]({url})\n\n")
                    f.write(f"Error scraping content: {e}")
                    f.write("\n\n---\n\n")
            
            # Sleep to be polite
            time.sleep(1)
            
    finally:
        driver.quit()
        print("Scraping complete.")

if __name__ == "__main__":
    scrape_chapters()
