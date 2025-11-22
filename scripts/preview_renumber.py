#!/usr/bin/env python3
"""Preview deterministic renumbering using a file-based offset.

This script DOES NOT modify dataset files. It computes a mapping:
  new_id = file_offset + original_numeric_id
where file_offset = (file_index + 1) * 100000

Writes `reports/renumber_preview.json` and `reports/renumber_preview.csv`.
"""
import json
import os
import csv
from collections import OrderedDict


def load_json_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_id(entry):
    if not isinstance(entry, dict):
        return None
    for k in ('id', 'Id', 'ID', 'questionId', 'qid', 'qId'):
        if k in entry:
            return entry[k]
    return None


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    datasets_dir = os.path.join(root, 'datasets')
    reports_dir = os.path.join(root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(datasets_dir) if f.lower().endswith('.json')])

    mapping = OrderedDict()
    file_index = 0
    for file_index, fname in enumerate(files):
        path = os.path.join(datasets_dir, fname)
        try:
            data = load_json_file(path)
        except Exception as e:
            mapping[fname] = {'error': f'load_error: {e}'}
            continue

        # Try to extract list of entries
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            if 'questions' in data and isinstance(data['questions'], list):
                items = data['questions']
            elif 'items' in data and isinstance(data['items'], list):
                items = data['items']
            else:
                # best-effort flatten
                items = []
                for v in data.values():
                    if isinstance(v, list):
                        items.extend(v)
        else:
            items = []

        offset = (file_index + 1) * 100000
        file_map = []
        for idx, entry in enumerate(items):
            orig_id = find_id(entry)
            if orig_id is None:
                new_id = None
            else:
                # Attempt numeric conversion
                try:
                    numeric = int(orig_id)
                    new_id = offset + numeric
                except Exception:
                    # Non-numeric ids: leave unchanged and mark
                    new_id = f'NONNUM:{orig_id}'

            file_map.append({'index': idx, 'orig_id': orig_id, 'new_id': new_id, 'question_preview': (entry.get('question') if isinstance(entry, dict) else None)})

        mapping[fname] = {'offset': offset, 'mappings': file_map}

    out_json = os.path.join(reports_dir, 'renumber_preview.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    out_csv = os.path.join(reports_dir, 'renumber_preview.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as csvf:
        w = csv.writer(csvf)
        w.writerow(['file', 'index', 'orig_id', 'new_id', 'question_preview'])
        for fname, info in mapping.items():
            if isinstance(info, dict) and 'mappings' in info:
                for m in info['mappings']:
                    w.writerow([fname, m['index'], m['orig_id'], m['new_id'], (m.get('question_preview') or '')[:200]])

    print(f'Preview written to {out_json} and {out_csv}')
    # Print first 20 remaps for quick review
    printed = 0
    for fname, info in mapping.items():
        if isinstance(info, dict) and 'mappings' in info:
            for m in info['mappings']:
                if m['orig_id'] is None:
                    continue
                print(f"{fname} [{m['index']}]: {m['orig_id']} -> {m['new_id']}")
                printed += 1
                if printed >= 20:
                    return 0

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
