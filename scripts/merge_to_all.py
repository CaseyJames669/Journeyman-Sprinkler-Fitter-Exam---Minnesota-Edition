#!/usr/bin/env python3
"""Merge all dataset JSON files into a single `all_questions.json`.

Creates a backup of existing `all_questions.json` as `all_questions.json.bak`.
Writes `reports/merge_summary.json` with counts and any skipped files.
"""
import json
import os
import shutil
from collections import OrderedDict


def load_items(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return None, f'LOAD_ERROR: {e}'

    if isinstance(data, list):
        return data, None
    if isinstance(data, dict):
        for key in ('questions', 'items', 'data'):
            if key in data and isinstance(data[key], list):
                return data[key], None
        # flatten best-effort
        values = []
        for v in data.values():
            if isinstance(v, list):
                values.extend(v)
        if values:
            return values, None

    return None, 'UNEXPECTED_JSON_SHAPE'


def find_id_key(entry):
    if not isinstance(entry, dict):
        return None
    for k in ('id', 'Id', 'ID', 'questionId', 'qid', 'qId'):
        if k in entry:
            return k
    return None


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    datasets_dir = os.path.join(root, 'datasets')
    out_file = os.path.join(root, 'all_questions.json')
    reports_dir = os.path.join(root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(datasets_dir) if f.lower().endswith('.json') and not f.endswith('.bak')])

    merged = []
    summary = {'files': [], 'total_entries': 0, 'skipped': []}

    for fname in files:
        path = os.path.join(datasets_dir, fname)
        items, err = load_items(path)
        if err:
            summary['skipped'].append({'file': fname, 'error': err})
            continue
        if items is None:
            summary['skipped'].append({'file': fname, 'error': 'no_items'})
            continue

        count = 0
        for entry in items:
            # ensure id key exists
            idk = find_id_key(entry)
            if idk is None:
                # skip entries without id
                summary['skipped'].append({'file': fname, 'index': count, 'reason': 'missing_id'})
                count += 1
                continue
            merged.append(entry)
            count += 1

        summary['files'].append({'file': fname, 'entries': count})
        summary['total_entries'] += count

    # backup existing all_questions.json
    if os.path.exists(out_file):
        bak = out_file + '.bak'
        if not os.path.exists(bak):
            shutil.copy2(out_file, bak)

    # Optional: sort merged by numeric id if possible
    def id_key(e):
        k = find_id_key(e)
        if not k:
            return 10**18
        try:
            return int(e[k])
        except Exception:
            return 10**18

    merged_sorted = sorted(merged, key=id_key)

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(merged_sorted, f, indent=2, ensure_ascii=False)

    out_report = os.path.join(reports_dir, 'merge_summary.json')
    with open(out_report, 'w', encoding='utf-8') as rf:
        json.dump(summary, rf, indent=2, ensure_ascii=False)

    print(f'Merged {summary["total_entries"]} entries from {len(summary["files"])} files into {out_file}')
    print(f'Report written to {out_report}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
