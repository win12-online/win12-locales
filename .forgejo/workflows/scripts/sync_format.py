#!/usr/bin/env python3
"""Sync HTML format across all language files."""
import re
import sys
from pathlib import Path

def normalize_properties_format(content):
    """Normalize .properties file format."""
    lines = []
    for line in content.split('\n'):
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            lines.append(line)
            continue
        
        # Skip if not a key=value line
        if '=' not in line:
            lines.append(line)
            continue
        
        key, value = line.split('=', 1)
        
        # Fix double single quotes
        value = value.replace("''", "'")
        
        # Fix escaped single quotes (should not be escaped in .properties)
        value = value.replace("\\'", "'")
        
        # Ensure onclick attributes are properly escaped
        value = re.sub(r'onclick="', 'onclick\\="', value)
        
        # Ensure other HTML attributes are properly escaped
        # class=" should be class\="
        value = re.sub(r'(\w+)="', r'\1\\="', value)
        
        # Fix semicolon position in onclick handlers
        # Pattern: '_blank'\); should be '_blank');
        value = value.replace("'\\);", "');")
        
        lines.append(f"{key}={value}")
    
    return '\n'.join(lines)

def sync_files(base_dir):
    base_dir = Path(base_dir)
    lang_dir = base_dir / 'lang'
    
    # Read source file
    source_file = lang_dir / 'lang_zh_CN.properties'
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    # Normalize source file
    normalized_source = normalize_properties_format(source_content)
    
    # Write normalized source file
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(normalized_source)
    print(f"Normalized: {source_file}")
    
    # Process translation files
    for lang_file in ['lang_en.properties', 'lang_zh_TW.properties']:
        filepath = lang_dir / lang_file
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            normalized = normalize_properties_format(content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(normalized)
            print(f"Normalized: {filepath}")

if __name__ == '__main__':
    sync_files(sys.argv[1] if len(sys.argv) > 1 else '.')
