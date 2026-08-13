#!/usr/bin/env python3
"""Check HTML integrity in .properties files.

Reports two kinds of problems per value:

1. An unescaped equals sign in an HTML attribute. The project writes the
   equals sign inside HTML attributes with a leading backslash (the escaped
   form) so that downstream key=value parsing does not split on it. Any
   attribute written without that escaping is flagged.
2. Unbalanced HTML tags (void elements such as br and img are ignored).
"""
import re
import sys

VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr',
}

# Matches a word directly followed by =". The escaped form (a backslash
# before the equals sign) is not matched because the word is followed by a
# backslash rather than by "=".
_UNESCAPED_ATTR_EQ = re.compile(r'\w+="')


def check_html(filepath):
    issues = []
    with open(filepath, encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or '=' not in stripped:
                continue

            key, value = stripped.split('=', 1)

            for match in _UNESCAPED_ATTR_EQ.finditer(value):
                issues.append(
                    'Line %d: unescaped HTML attribute "%s" '
                    '(expected a backslash before the equals sign)'
                    % (line_num, match.group(0))
                )

            open_tags = re.findall(r'<(\w+)[^>]*>', value)
            close_tags = {t.lower() for t in re.findall(r'</(\w+)>', value)}
            for tag in open_tags:
                if tag.lower() not in VOID_ELEMENTS and tag.lower() not in close_tags:
                    issues.append('Line %d: possibly unclosed <%s> tag' % (line_num, tag))

    return issues


def main():
    files = sys.argv[1:]
    if not files:
        print('Usage: check_html.py <properties-file> [...]', file=sys.stderr)
        sys.exit(2)

    exit_code = 0
    for filepath in files:
        issues = check_html(filepath)
        if issues:
            exit_code = 1
            print('\n%s:' % filepath)
            for issue in issues:
                print('  - %s' % issue)
        else:
            print('%s: OK' % filepath)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
