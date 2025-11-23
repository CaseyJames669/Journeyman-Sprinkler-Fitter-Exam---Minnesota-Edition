import json
import os

def save_chapters(chapters):
    output_file = "scraper/output/full_text.md"
    
    # Check if file exists to determine if we need to add a header
    file_exists = os.path.exists(output_file)
    
    with open(output_file, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("# Minnesota Fire Code 2020\n\n")
            
        for chapter in chapters:
            f.write(f"## [{chapter['url']}]({chapter['url']})\n\n")
            f.write(chapter['content'])
            f.write("\n\n---\n\n")
            
    print(f"Saved {len(chapters)} chapters to {output_file}")

if __name__ == "__main__":
    # This is just a placeholder. I will call this script with data or import it.
    pass
