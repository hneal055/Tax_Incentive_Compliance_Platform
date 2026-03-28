"""
PilotForge Brand Consistency Checker
Ensures all references use correct branding
"""
import re
from pathlib import Path
from collections import defaultdict


# Brand consistency rules
BRAND_RULES = {
    'correct_name': {
        'pattern': r'\bPilotForge\b',
        'incorrect': ['Pilot Forge', 'pilot forge', 'pilotforge', 'PILOTFORGE'],
        'message': 'Use "PilotForge" (one word, capital P and F)'
    },
    'tagline': {
        'expected': 'Tax Incentive Intelligence for Film & TV',
        'alternatives': [
            'Forge Your Production\'s Future',
            'Tax Incentive Intelligence'
        ],
        'message': 'Use approved tagline'
    },
    'copyright': {
        'pattern': r'Copyright \(c\) \d{4}(-\d{4})? Howard Neal - PilotForge',
        'message': 'Use: Copyright (c) 2025-2026 Howard Neal - PilotForge'
    },
    'api_title': {
        'pattern': r'title="PilotForge API"',
        'message': 'API title should be "PilotForge API"'
    }
}

# File patterns to check
CHECK_PATTERNS = [
    '**/*.py',
    '**/*.md',
    'LICENSE',
    '*.toml',
    '*.yml',
    '*.yaml',
]

# Exclude patterns
EXCLUDE_PATTERNS = [
    'venv',
    'node_modules',
    '__pycache__',
    '.git',
    '*.pyc',
    'backup_*',
]


def should_check_file(filepath):
    """Determine if file should be checked"""
    path_str = str(filepath)
    
    # Exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return False
    
    return True


def check_file_branding(filepath):
    """Check a single file for brand consistency"""
    issues = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except:
        return issues
    
    # Check for incorrect name variations
    for incorrect in BRAND_RULES['correct_name']['incorrect']:
        if incorrect in content:
            issues.append({
                'file': filepath,
                'type': 'incorrect_name',
                'found': incorrect,
                'message': BRAND_RULES['correct_name']['message'],
                'line_numbers': [
                    i + 1 for i, line in enumerate(content.split('\n'))
                    if incorrect in line
                ]
            })
    
    # Check copyright format (for Python files and LICENSE)
    if filepath.suffix in ['.py', ''] or filepath.name == 'LICENSE':
        if 'Copyright' in content and 'PilotForge' in content:
            if not re.search(BRAND_RULES['copyright']['pattern'], content):
                issues.append({
                    'file': filepath,
                    'type': 'copyright_format',
                    'message': BRAND_RULES['copyright']['message']
                })
    
    # Check API title (for main.py)
    if filepath.name == 'main.py':
        if 'title=' in content:
            if not re.search(BRAND_RULES['api_title']['pattern'], content):
                issues.append({
                    'file': filepath,
                    'type': 'api_title',
                    'message': BRAND_RULES['api_title']['message']
                })
    
    return issues


def check_all_files(project_root):
    """Check all project files"""
    all_issues = []
    files_checked = 0
    
    for pattern in CHECK_PATTERNS:
        for filepath in project_root.glob(pattern):
            if not filepath.is_file():
                continue
            
            if not should_check_file(filepath):
                continue
            
            files_checked += 1
            issues = check_file_branding(filepath)
            all_issues.extend(issues)
    
    return all_issues, files_checked


def print_issues_report(issues, files_checked):
    """Print formatted issues report"""
    print("\n📊 Brand Consistency Report")
    print("=" * 60)
    print(f"Files checked: {files_checked}")
    print(f"Issues found: {len(issues)}")
    
    if not issues:
        print("\n✅ All files follow PilotForge brand guidelines!")
        return
    
    # Group issues by type
    issues_by_type = defaultdict(list)
    for issue in issues:
        issues_by_type[issue['type']].append(issue)
    
    # Print grouped issues
    for issue_type, type_issues in issues_by_type.items():
        print(f"\n❌ {issue_type.replace('_', ' ').title()} ({len(type_issues)} files)")
        print("-" * 60)
        
        for issue in type_issues[:10]:  # Show first 10
            print(f"\n  File: {issue['file']}")
            if 'found' in issue:
                print(f"  Found: '{issue['found']}'")
            if 'line_numbers' in issue:
                print(f"  Lines: {', '.join(map(str, issue['line_numbers']))}")
            print(f"  Fix: {issue['message']}")
        
        if len(type_issues) > 10:
            print(f"\n  ... and {len(type_issues) - 10} more files")


def generate_fix_script(issues):
    """Generate script to auto-fix issues"""
    script = """#!/usr/bin/env python3
\"\"\"
Auto-generated brand consistency fixes
Run this to automatically fix brand issues
\"\"\"
import re
from pathlib import Path

fixes = [
"""
    
    for issue in issues:
        if issue['type'] == 'incorrect_name' and 'found' in issue:
            script += f"""
    {{
        'file': Path('{issue['file']}'),
        'find': '{issue['found']}',
        'replace': 'PilotForge'
    }},
"""
    
    script += """
]

for fix in fixes:
    try:
        content = fix['file'].read_text()
        content = content.replace(fix['find'], fix['replace'])
        fix['file'].write_text(content)
        print(f"✅ Fixed: {fix['file']}")
    except Exception as e:
        print(f"❌ Error fixing {fix['file']}: {e}")

print("\\n🎉 Auto-fix complete!")
"""
    
    fix_script_path = Path('fix_branding.py')
    fix_script_path.write_text(script)
    
    return fix_script_path


def main():
    """Main brand consistency checker"""
    print("🎨 PilotForge Brand Consistency Checker")
    print("=" * 60)
    
    # Get project root
    project_root = Path.cwd()
    print(f"📁 Checking: {project_root}")
    
    # Check all files
    print("\n🔍 Scanning files...")
    issues, files_checked = check_all_files(project_root)
    
    # Print report
    print_issues_report(issues, files_checked)
    
    # Offer to generate fix script
    if issues:
        print("\n" + "=" * 60)
        print("💡 Auto-fix available!")
        
        response = input("\n📝 Generate auto-fix script? (y/N): ")
        if response.lower() == 'y':
            fix_script = generate_fix_script(issues)
            print(f"\n✅ Created: {fix_script}")
            print(f"   Run: python {fix_script}")
    
    # Exit code
    return 0 if not issues else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())