#!/usr/bin/env python3
"""
Simple validator for question JSON files in `datasets/`.
Checks that each file is valid JSON, contains an array or objects with required keys,
and verifies that `id` values are unique across all files.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'datasets'

required_keys = {'id', 'category', 'question', 'answer'}

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse {path}: {e}")
        return None

def main():
    if not DATA_DIR.exists():
        print(f"datasets directory not found at {DATA_DIR}")
        sys.exit(1)

    ids = set()
    errors = 0

    for p in sorted(DATA_DIR.glob('*.json')):
        data = load_json(p)
        if data is None:
            errors += 1
            continue

        # Accept either a list of question objects or a single object wrapper
        items = data if isinstance(data, list) else data.get('questions') if isinstance(data, dict) else None
        if items is None:
            print(f"WARN: {p} does not contain an array of questions or a 'questions' field")
            continue

        for i, q in enumerate(items):
            if not isinstance(q, dict):
                print(f"ERROR: {p}[{i}] is not an object")
                errors += 1
                continue
            missing = required_keys - q.keys()
            if missing:
                print(f"ERROR: {p}[{i}] missing keys: {missing}")
                errors += 1
                continue
            if q['id'] in ids:
                print(f"ERROR: Duplicate id {q['id']} in {p}[{i}]")
                errors += 1
            ids.add(q['id'])

    print(f"Validation complete. {len(ids)} unique ids checked. {errors} errors/warnings.")
    if errors:
        sys.exit(2)

if __name__ == '__main__':
    main()
