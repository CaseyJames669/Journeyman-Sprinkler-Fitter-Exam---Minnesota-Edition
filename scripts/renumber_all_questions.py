import json
import os
import shutil

def renumber_questions(file_path, start_id):
    """
    Renumber the 'id' field of questions in a JSON file starting from a specified ID.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # Create a backup of the original file
    backup_path = file_path + ".bak"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Error: Expected a JSON array of questions.")
        return

    current_id = start_id
    updated_count = 0
    for question in data:
        if isinstance(question, dict) and 'id' in question:
            question['id'] = current_id
            current_id += 1
            updated_count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully renumbered {updated_count} questions in {file_path}, starting from ID {start_id}.")

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.join(script_dir, '..')
    all_questions_path = os.path.join(root_dir, 'all_questions.json')
    
    starting_id = 10001
    renumber_questions(all_questions_path, starting_id)
