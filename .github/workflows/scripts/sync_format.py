#!/usr/bin/env python3
"""Normalize HTML attribute escaping in .properties files.

The project writes the equals sign inside HTML attributes with a leading
backslash (the escaped form) so that downstream key=value parsing does not
split on it. This script rewrites any attribute written without that escaping
across every language file. It is idempotent and preserves line endings.
"""
import re
import sys
from pathlib import Path

# Matches a word directly followed by =". The escaped form (a backslash
# before the equals sign) is not matched because the word is followed by a
# backslash rather than by "=".
_UNESCAPED_ATTR_EQ = re.compile(r'(\w+)="')


def normalize_properties_format(content):
    lines = []
    for line in content.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            lines.append(line)
            continue
        if '=' not in line:
            lines.append(line)
            continue

        key, value = line.split('=', 1)
        value = _UNESCAPED_ATTR_EQ.sub(r'\1\\="', value)
        lines.append('%s=%s' % (key, value))

    return '\n'.join(lines)


def normalize_files(base_dir):
    lang_dir = Path(base_dir) / 'lang'
    for filepath in sorted(lang_dir.glob('*.properties')):
        content = filepath.read_text(encoding='utf-8')
        normalized = normalize_properties_format(content)
        filepath.write_text(normalized, encoding='utf-8')
        print('Normalized: %s' % filepath)


if __name__ == '__main__':
    normalize_files(sys.argv[1] if len(sys.argv) > 1 else '.')
