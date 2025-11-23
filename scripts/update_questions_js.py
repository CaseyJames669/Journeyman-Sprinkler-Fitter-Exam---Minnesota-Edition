import json
import os

def update_questions_js():
    # Paths
    json_path = 'all_questions.json'
    js_path = os.path.join('js', 'questions.js')

    # Check if source exists
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    # Read JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} questions from {json_path}")

        # Write JS
        # We write it as a global variable "questions"
        js_content = f"const questions = {json.dumps(data, indent=4)};"
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"Successfully wrote {len(data)} questions to {js_path}")
        print("You can now open index.html locally without a server.")

    except Exception as e:
        print(f"Failed to update questions.js: {e}")

if __name__ == "__main__":
    update_questions_js()
