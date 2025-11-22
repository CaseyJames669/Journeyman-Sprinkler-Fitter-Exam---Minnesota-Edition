
import os

file_path = 'js/questions.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replacements
replacements = {
    'Ã—': '×',
    'âˆš': '√'
}

original_content = content
for bad, good in replacements.items():
    content = content.replace(bad, good)

if content != original_content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed encoding issues in {file_path}")
else:
    print(f"No encoding issues found in {file_path}")
