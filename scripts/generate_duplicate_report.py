#!/usr/bin/env python3
"""Generate a duplicate-id report for JSON datasets.

Writes `reports/duplicate_ids.json` and `reports/duplicate_ids.csv`.
"""
import json
import os
import csv
from collections import defaultdict


def load_items(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return None, f"LOAD_ERROR: {e}"

    # Common shapes: top-level list, or dict with 'questions'/'items' keys
    if isinstance(data, list):
        return data, None
    if isinstance(data, dict):
        for key in ('questions', 'items', 'data'):
            if key in data and isinstance(data[key], list):
                return data[key], None
        # If dict maps numeric keys to entries, try to coerce
        values = [v for k, v in data.items() if isinstance(v, dict) or isinstance(v, list)]
        if values:
            # best-effort: flatten one level
            flat = []
            for v in values:
                if isinstance(v, list):
                    flat.extend(v)
                else:
                    flat.append(v)
            return flat, None

    return None, 'UNEXPECTED_JSON_SHAPE'


def find_id(entry):
    if not isinstance(entry, dict):
        return None
    # Common id key names
    for k in ('id', 'Id', 'ID', 'questionId', 'qid', 'qId'):
        if k in entry:
            return entry[k]
    return None


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    datasets_dir = os.path.join(root, 'datasets')
    reports_dir = os.path.join(root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    ids_map = defaultdict(list)
    missing_id = []
    load_errors = []

    if not os.path.isdir(datasets_dir):
        print(f"Datasets directory not found: {datasets_dir}")
        return 2

    files = sorted([f for f in os.listdir(datasets_dir) if f.lower().endswith('.json')])

    for fname in files:
        path = os.path.join(datasets_dir, fname)
        items, err = load_items(path)
        if err:
            load_errors.append({'file': fname, 'error': err})
            continue
        if items is None:
            load_errors.append({'file': fname, 'error': 'no_items'})
            continue

        for idx, entry in enumerate(items):
            idv = find_id(entry)
            if idv is None:
                missing_id.append({'file': fname, 'index': idx, 'entry_preview': str(entry)[:200]})
            else:
                ids_map[str(idv)].append({'file': fname, 'index': idx, 'question_preview': (entry.get('question') if isinstance(entry, dict) else None)})

    duplicates = {k: v for k, v in ids_map.items() if len(v) > 1}

    # Write JSON report
    out_json = os.path.join(reports_dir, 'duplicate_ids.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump({'duplicates': duplicates, 'missing_id': missing_id, 'load_errors': load_errors}, f, indent=2, ensure_ascii=False)

    # Write CSV report (one row per occurrence)
    out_csv = os.path.join(reports_dir, 'duplicate_ids.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as csvf:
        w = csv.writer(csvf)
        w.writerow(['id', 'file', 'index', 'question_preview'])
        for idv, occ in ids_map.items():
            if len(occ) > 1:
                for o in occ:
                    w.writerow([idv, o.get('file'), o.get('index'), (o.get('question_preview') or '')[:200]])

    # Summary output
    total_ids = len(ids_map)
    total_duplicates = len(duplicates)
    print(f"Scanned {len(files)} files. Found {total_ids} unique ids; {total_duplicates} ids duplicated.")
    print(f"Reports written:")
    print(f"  {out_json}")
    print(f"  {out_csv}")

    if load_errors:
        print(f"Load errors: {len(load_errors)} (see {out_json})")
    if missing_id:
        print(f"Entries missing id: {len(missing_id)} (see {out_json})")

    # Exit code 0 even if duplicates found; report produced.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
