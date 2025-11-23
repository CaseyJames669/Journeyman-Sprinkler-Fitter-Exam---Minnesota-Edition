import json
import os
import shutil

def add_default_fields(file_path):
    """
    Adds 'difficulty' and 'sprinklerType' fields to questions in a JSON file
    if they are missing, with default values.
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

    updated_count = 0
    for question in data:
        if isinstance(question, dict):
            if 'difficulty' not in question:
                question['difficulty'] = "unlisted"
                updated_count += 1
            if 'sprinklerType' not in question:
                question['sprinklerType'] = "N/A"
                updated_count += 1
    
    # Only write if changes were made
    if updated_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully added default fields to {updated_count} fields in {file_path}.")
    else:
        print(f"No new fields to add. All questions in {file_path} already have 'difficulty' and 'sprinklerType'.")


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.join(script_dir, '..')
    all_questions_path = os.path.join(root_dir, 'all_questions.json')
    
    add_default_fields(all_questions_path)
