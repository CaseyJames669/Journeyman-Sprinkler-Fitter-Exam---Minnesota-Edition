import json
import os

# Read the questions
with open('all_questions.json', 'r', encoding='utf-8') as f:
    questions_json = f.read()

# Read the HTML file
with open('foreman.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Define the marker to replace
start_marker = "const questions = ["
end_marker = "];"

# Find the start and end of the questions block
start_index = html_content.find(start_marker)
# Find the first semicolon after the start marker to end the block
# We look for the closing bracket and semicolon of the array
# Since the placeholder ends with "];", we can search for that after the start
end_index = html_content.find(end_marker, start_index) + len(end_marker)

if start_index != -1 and end_index != -1:
    # Construct the new content
    new_content = html_content[:start_index] + "const questions = " + questions_json + ";" + html_content[end_index:]
    
    # Write back to file
    with open('foreman.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully injected questions.")
else:
    print("Could not find questions block in foreman.html")
