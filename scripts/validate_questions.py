"""
Data Validation Script for all_questions.json
Validates JSON structure, required fields, and data integrity.
"""
import json
import sys

def validate_questions(filepath):
    """Validate the questions JSON file."""
    print(f"Validating: {filepath}\n")
    
    issues = []
    warnings = []
    
    # Step 1: Load JSON with UTF-8 encoding
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ JSON syntax valid")
        print(f"✓ Total questions loaded: {len(data)}\n")
    except json.JSONDecodeError as e:
        print(f"✗ JSON SYNTAX ERROR: {e}")
        return False
    except UnicodeDecodeError as e:
        print(f"✗ ENCODING ERROR: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    # Step 2: Validate structure
    if not isinstance(data, list):
        issues.append("Root element must be an array")
        print(f"✗ {issues[-1]}")
        return False
    
    # Step 3: Validate each question
    required_fields = ['id', 'category', 'topic', 'question', 'answer', 'distractors', 'citation', 'code_text']
    ids_seen = set()
    
    for idx, q in enumerate(data):
        q_id = q.get('id', f'MISSING_{idx}')
        
        # Check if it's a dict
        if not isinstance(q, dict):
            issues.append(f"Question at index {idx}: Not a dictionary object")
            continue
        
        # Check required fields
        missing = [field for field in required_fields if field not in q]
        if missing:
            issues.append(f"Q{q_id}: Missing fields: {', '.join(missing)}")
        
        # Check ID uniqueness
        if 'id' in q:
            if q['id'] in ids_seen:
                issues.append(f"Q{q_id}: Duplicate ID")
            ids_seen.add(q['id'])
        
        # Check distractors is array with 3 items
        if 'distractors' in q:
            if not isinstance(q['distractors'], list):
                issues.append(f"Q{q_id}: 'distractors' must be an array")
            elif len(q['distractors']) != 3:
                warnings.append(f"Q{q_id}: Expected 3 distractors, got {len(q['distractors'])}")
        
        # Check for empty strings
        for field in ['question', 'answer', 'citation', 'code_text']:
            if field in q and not q[field]:
                warnings.append(f"Q{q_id}: '{field}' is empty")
        
        # Check for MN amendments flag
        if q.get('is_mn_amendment'):
            if 'MN' not in q.get('citation', ''):
                warnings.append(f"Q{q_id}: Marked as MN amendment but citation doesn't contain 'MN'")
    
    # Report results
    print(f"\n{'='*60}")
    print("VALIDATION RESULTS")
    print(f"{'='*60}")
    
    if issues:
        print(f"\n✗ CRITICAL ISSUES FOUND: {len(issues)}")
        for issue in issues[:20]:  # Show first 20
            print(f"  - {issue}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more")
    else:
        print(f"\n✓ No critical issues found")
    
    if warnings:
        print(f"\n⚠ WARNINGS: {len(warnings)}")
        for warning in warnings[:20]:  # Show first 20
            print(f"  - {warning}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")
    else:
        print(f"\n✓ No warnings")
    
    print(f"\n{'='*60}")
    print(f"Questions validated: {len(data)}")
    print(f"Unique IDs: {len(ids_seen)}")
    print(f"{'='*60}\n")
    
    return len(issues) == 0

if __name__ == "__main__":
    filepath = "android/app/src/main/assets/public/all_questions.json"
    
    # Redirect output to file
    import io
    output = io.StringIO()
    
    # Capture print output
    old_stdout = sys.stdout
    sys.stdout = output
    
    success = validate_questions(filepath)
    
    # Restore stdout
    sys.stdout = old_stdout
    
    # Get results
    results = output.getvalue()
    
    # Print to console
    print(results)
    
    # Save to file
    with open('validation_report.txt', 'w', encoding='utf-8') as f:
        f.write(results)
    
    print(f"\n✓ Full report saved to: validation_report.txt")
    
    sys.exit(0 if success else 1)
