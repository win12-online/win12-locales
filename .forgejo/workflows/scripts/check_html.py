#!/usr/bin/env python3
"""Check HTML integrity in properties files."""
import re
import sys

def check_html(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if '=' not in line or line.startswith('#'):
                continue
            
            key, value = line.split('=', 1)
            
            # Check for unescaped quotes in HTML attributes
            if '<' in value and '>' in value:
                # Find HTML tags
                tags = re.findall(r'<[^>]+>', value)
                for tag in tags:
                    # Check for unescaped quotes in attributes
                    if '="' in tag and '\\"' not in tag:
                        # This might be okay in some contexts, but worth checking
                        pass
            
            # Check for common issues
            if 'onclick' in value and 'window.open' in value:
                if "'" in value and "\\'" not in value:
                    # Check for unescaped single quotes in onclick
                    if "window.open('" in value and "\\'" not in value:
                        issues.append(f"Line {line_num}: Possible unescaped single quote in onclick")
            
            # Check for mismatched tags
            open_tags = re.findall(r'<(\w+)[^>]*>', value)
            close_tags = re.findall(r'</(\w+)>', value)
            
            # Simple check - not perfect but catches obvious issues
            for tag in open_tags:
                if tag.lower() not in ['br', 'hr', 'img', 'input', 'meta', 'link']:
                    if tag.lower() not in [t.lower() for t in close_tags]:
                        issues.append(f"Line {line_num}: Possibly unclosed <{tag}> tag")
    
    return issues

if __name__ == '__main__':
    for filepath in sys.argv[1:]:
        issues = check_html(filepath)
        if issues:
            print(f"\n{filepath}:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"{filepath}: No obvious issues found")
