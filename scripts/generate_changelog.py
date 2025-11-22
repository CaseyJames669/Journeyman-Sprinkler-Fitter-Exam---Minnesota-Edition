#!/usr/bin/env python3
"""Generate a markdown changelog from reports/renumber_applied.json
"""
import json
import os
from datetime import datetime


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    reports_dir = os.path.join(root, 'reports')
    src = os.path.join(reports_dir, 'renumber_applied.json')
    out = os.path.join(reports_dir, 'renumber_changelog.md')

    if not os.path.exists(src):
        print('renumber_applied.json not found')
        return 1

    data = json.load(open(src, 'r', encoding='utf-8'))

    total_files = len(data)
    total_changes = 0
    per_file = []

    for fname, info in data.items():
        changes = info.get('changes') or []
        cnt = len(changes)
        total_changes += cnt
        per_file.append((fname, cnt, info.get('offset')))

    per_file.sort(key=lambda x: (-x[1], x[0]))

    with open(out, 'w', encoding='utf-8') as f:
        f.write('# Renumbering Changelog\n\n')
        f.write(f'Generated: {datetime.utcnow().isoformat()}Z\n\n')
        f.write(f'- Files scanned: {total_files}\n')
        f.write(f'- Total ids changed: {total_changes}\n\n')
        f.write('## Per-file summary\n\n')
        f.write('| File | Changed ids | Offset |\n')
        f.write('|---|---:|---:|\n')
        for fname, cnt, offset in per_file:
            f.write(f'| `{fname}` | {cnt} | {offset or "-"} |\n')

        f.write('\n## Notes\n\n')
        f.write('- Backups for modified dataset files were created with the `.bak` suffix next to each file.\n')
        f.write('- New id scheme: `new_id = file_offset + original_numeric_id` where `file_offset = (file_index + 1) * 100000` for sorted file list.\n')
        f.write('- If you want a different scheme (sequential global ids or smaller offsets), run the preview and apply scripts with modifications.\n')

    print(f'Changelog written to {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
