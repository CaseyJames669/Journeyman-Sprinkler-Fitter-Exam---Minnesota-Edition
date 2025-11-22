#!/usr/bin/env python3
"""Apply deterministic renumbering to dataset JSON files.

This script will:
 - create a `.bak` backup for each modified dataset file (if not already present)
 - update numeric `id` fields using the per-file offset scheme:
       new_id = (file_index + 1) * 100000 + int(orig_id)
 - write a report to `reports/renumber_applied.json` and CSV

Run only after previewing with `scripts/preview_renumber.py`.
"""
import json
import os
import csv
import shutil
from collections import OrderedDict


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_id_key(entry):
    # Return the key name for the id if present
    for k in ('id', 'Id', 'ID', 'questionId', 'qid', 'qId'):
        if k in entry:
            return k
    return None


def apply_to_entry(entry, offset):
    if not isinstance(entry, dict):
        return None
    key = find_id_key(entry)
    if not key:
        return None
    orig = entry[key]
    try:
        numeric = int(orig)
    except Exception:
        return None
    new_id = offset + numeric
    entry[key] = new_id
    return (orig, new_id)


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    datasets_dir = os.path.join(root, 'datasets')
    reports_dir = os.path.join(root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(datasets_dir) if f.lower().endswith('.json')])

    applied_summary = OrderedDict()

    for idx, fname in enumerate(files):
        path = os.path.join(datasets_dir, fname)
        try:
            data = load_json(path)
        except Exception as e:
            applied_summary[fname] = {'error': f'load_error: {e}'}
            continue

        # locate items list
        if isinstance(data, list):
            items = data
            container_type = 'list'
        elif isinstance(data, dict):
            if 'questions' in data and isinstance(data['questions'], list):
                items = data['questions']
                container_type = 'questions'
            elif 'items' in data and isinstance(data['items'], list):
                items = data['items']
                container_type = 'items'
            else:
                # flatten and attempt to map back - in this repo most files are top-level lists
                # fallback: treat top-level dict as single entry
                items = None
                container_type = 'dict'
        else:
            items = None
            container_type = 'unknown'

        offset = (idx + 1) * 100000
        file_changes = []

        if items is None:
            applied_summary[fname] = {'error': 'no_items_to_process'}
            continue

        # backup
        bak_path = path + '.bak'
        if not os.path.exists(bak_path):
            shutil.copy2(path, bak_path)

        # apply
        for i, entry in enumerate(items):
            res = apply_to_entry(entry, offset)
            if res:
                orig, new = res
                file_changes.append({'index': i, 'orig_id': orig, 'new_id': new})

        # write file only if there are changes
        if file_changes:
            try:
                write_json(path, data)
                applied_summary[fname] = {'offset': offset, 'changes': file_changes}
            except Exception as e:
                applied_summary[fname] = {'error': f'write_error: {e}'}
        else:
            applied_summary[fname] = {'offset': offset, 'changes': []}

    # write report
    out_json = os.path.join(reports_dir, 'renumber_applied.json')
    write_json(out_json, applied_summary)

    out_csv = os.path.join(reports_dir, 'renumber_applied.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as csvf:
        w = csv.writer(csvf)
        w.writerow(['file', 'index', 'orig_id', 'new_id'])
        for fname, info in applied_summary.items():
            if isinstance(info, dict) and 'changes' in info:
                for c in info['changes']:
                    w.writerow([fname, c['index'], c['orig_id'], c['new_id']])

    print(f"Applied renumbering. Report: {out_json}, {out_csv}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
