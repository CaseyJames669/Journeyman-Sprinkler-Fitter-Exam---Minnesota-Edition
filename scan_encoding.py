
import re

file_path = 'js/questions.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of Ã followed by any character
matches = re.findall(r'(Ã.)', content)
unique_matches = set(matches)

print(f"Found {len(matches)} artifacts.")
print("Unique patterns found:")
for m in unique_matches:
    # Try to decode it as UTF-8 bytes interpreted as Latin-1
    try:
        # This is a bit of a guess, but often works for this type of corruption
        # The characters are likely UTF-8 bytes that were read as Latin-1/Windows-1252
        # So we encode to Latin-1 to get the bytes back, then decode as UTF-8
        corrected = m.encode('latin1').decode('utf-8')
        print(f"'{m}' -> '{corrected}'")
    except:
        print(f"'{m}' -> ???")

# Also print context for each
for i, line in enumerate(content.splitlines()):
    if 'Ã' in line:
        print(f"Line {i+1}: {line.strip()}")
