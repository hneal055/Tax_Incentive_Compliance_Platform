"""
SceneIQ Rebranding Script
Automatically updates all project files with new SceneIQ branding
"""
import os
import re
from pathlib import Path
from datetime import datetime

# Branding configuration
BRAND_CONFIG = {
    'old_name': 'Tax-Incentive Compliance Platform',
    'new_name': 'SceneIQ',
    'tagline': 'Tax Incentive Intelligence for Film & TV',
    'tagline_alt': 'Forge Your Production\'s Future',
    'author': 'Howard Neal',
    'year': '2025-2026',
    'url': 'https://pilotforge.com',  # Update when you have domain
}

# Files to update
FILE_PATTERNS = [
    'src/**/*.py',
    'tests/**/*.py',
    '*.md',
    'LICENSE',
    'pyproject.toml',
    'docker-compose.yml',
    'render.yaml',
]

# Replacement rules
REPLACEMENTS = [
    # Main name replacements
    (r'Tax-Incentive Compliance Platform', 'SceneIQ'),
    (r'Tax_Incentive_Compliance_Platform', 'SceneIQ'),
    (r'tax-incentive-platform', 'pilotforge'),
    (r'tax_incentive_platform', 'pilotforge'),
    
    # Add taglines
    (r'(SceneIQ)(\s*\n)', r'\1\n> Tax Incentive Intelligence for Film & TV\n'),
    
    # Update API messages
    (r'"message": "Tax-Incentive Compliance Platform API"', 
     '"message": "Welcome to SceneIQ", "tagline": "Tax Incentive Intelligence for Film & TV"'),
    
    # Update descriptions
    (r'Professional tax incentive calculation', 
     'SceneIQ - Tax Incentive Intelligence for Film & TV Productions'),
]


def backup_project(project_root):
    """Create backup before making changes"""
    backup_dir = project_root / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"📦 Creating backup at: {backup_dir}")
    
    import shutil
    shutil.copytree(project_root, backup_dir, 
                   ignore=shutil.ignore_patterns('venv', 'node_modules', '.git', '__pycache__', '*.pyc'))
    
    print(f"✅ Backup created successfully!")
    return backup_dir


def update_file(filepath, replacements):
    """Update a single file with all replacements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # Apply all replacements
        for pattern, replacement in replacements:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made = True
        
        # Write back if changes were made
        if changes_made:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False


def update_main_py(filepath):
    """Special handling for src/main.py"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update FastAPI app initialization
    content = re.sub(
        r'title="[^"]*"',
        f'title="SceneIQ API"',
        content
    )
    
    content = re.sub(
        r'description="[^"]*"',
        f'description="Tax Incentive Intelligence for Film & TV Productions"',
        content
    )
    
    # Update root endpoint
    content = re.sub(
        r'"message": "[^"]*Compliance Platform[^"]*"',
        '"message": "Welcome to SceneIQ", "tagline": "Tax Incentive Intelligence for Film & TV"',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {filepath}")


def update_readme(filepath):
    """Special handling for README.md"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace title
    content = re.sub(
        r'# 🎬 Tax-Incentive Compliance Platform',
        '# 🎬 SceneIQ',
        content
    )
    
    # Add tagline after title
    if '> **Tax Incentive Intelligence' not in content:
        content = re.sub(
            r'(# 🎬 SceneIQ\n)',
            r'\1\n> **Tax Incentive Intelligence for Film & TV Productions**\n',
            content
        )
    
    # Update project description
    content = re.sub(
        r'The Tax-Incentive Compliance Platform is',
        'SceneIQ is',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {filepath}")


def update_license(filepath):
    """Special handling for LICENSE"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update copyright holder
    content = re.sub(
        r'Copyright \(c\) \d{4}(-\d{4})? [^\n]+',
        f'Copyright (c) {BRAND_CONFIG["year"]} {BRAND_CONFIG["author"]} - SceneIQ',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {filepath}")


def create_brand_guidelines(project_root):
    """Create brand guidelines document"""
    brand_doc = f"""# 🎨 SceneIQ Brand Guidelines

## Brand Identity

### Name
**SceneIQ**

### Tagline
Primary: "Tax Incentive Intelligence for Film & TV"
Alternative: "Forge Your Production's Future"

### Mission Statement
SceneIQ empowers film and television productions to maximize their tax incentive 
savings through intelligent location comparison, compliance verification, and 
professional reporting across 32 global jurisdictions.

---

## Visual Identity

### Colors
- **Primary Blue**: #2c5aa0 (Professional, trustworthy)
- **Success Green**: #28a745 (Savings, positive outcomes)
- **Gold Accent**: #ffc107 (Value, money, optimization)
- **Dark Text**: #1a1a1a
- **Light Gray**: #f8f8f8

### Typography
- **Headings**: Helvetica Bold / Arial Bold
- **Body**: Helvetica / Arial
- **Code**: Consolas / Monaco

### Logo Concepts
1. Film slate + forge hammer combination
2. P+F monogram with clean, modern style
3. Location pin with film reel inside

---

## Voice & Tone

### Voice Characteristics
- **Professional**: Industry expertise, authoritative
- **Approachable**: Friendly, helpful, not stuffy
- **Data-Driven**: Facts, numbers, evidence-based
- **Results-Focused**: ROI, savings, concrete outcomes

### Writing Style
- Use active voice
- Lead with benefits, not features
- Include real dollar amounts when possible
- Speak to production decision-makers

### Example Phrases
✅ "Save $750K by filming in Louisiana"
✅ "Compare 32 jurisdictions in seconds"
✅ "From calculation to compliance verification"
✅ "Maximize your production's tax savings"

❌ "Our platform provides tax incentive calculation capabilities"
❌ "Utilize our system to determine optimal filming locations"

---

## Messaging

### Key Messages
1. **Efficiency**: "32 jurisdictions, one platform"
2. **Accuracy**: "100% tested calculation engine"
3. **Professionalism**: "Enterprise-grade reports (PDF & Excel)"
4. **Intelligence**: "Smart recommendations, real savings"

### Value Propositions
- **For Productions**: "Find the location that saves you the most"
- **For Accountants**: "Accurate calculations, professional reports"
- **For Executives**: "Data-driven location decisions"
- **For Film Commissions**: "Showcase your incentive programs effectively"

---

## Use Cases

### Primary Tagline Use
```
SceneIQ
Tax Incentive Intelligence for Film & TV
```

### Short Form
```
SceneIQ: Smart Tax Incentives
```

### Social Media Bio
```
SceneIQ helps film & TV productions maximize tax incentives 
across 32 global jurisdictions. 💰🎬
```

### Email Signature
```
[Name]
[Title], SceneIQ
Tax Incentive Intelligence for Film & TV
pilotforge.com
```

---

## API Branding

### API Title
```python
title="SceneIQ API"
description="Tax Incentive Intelligence for Film & TV Productions"
```

### Welcome Message
```json
{{
  "message": "Welcome to SceneIQ",
  "tagline": "Tax Incentive Intelligence for Film & TV",
  "version": "1.0.0"
}}
```

### Error Messages
Keep branded and professional:
```
"SceneIQ was unable to process your request..."
```

---

## Domain & Social

### Website
- Primary: pilotforge.com
- Alternatives: getpilotforge.com, usepilotforge.com

### Social Media
- Twitter/X: @pilotforge
- LinkedIn: linkedin.com/company/pilotforge
- Instagram: @pilotforge
- GitHub: github.com/[username]/pilotforge

---

## Legal

### Copyright Notice
```
Copyright (c) {BRAND_CONFIG['year']} {BRAND_CONFIG['author']} - SceneIQ
```

### Trademark Usage
```
SceneIQ™
```
(Use ™ until registered, then ®)

---

## Don'ts

❌ Don't call it "Pilot Forge" (two words)
❌ Don't use "The SceneIQ" (no article)
❌ Don't abbreviate to "PF" in user-facing content
❌ Don't change the capitalization (not "pilotForge" or "PILOTFORGE")

---

**Last Updated**: {datetime.now().strftime('%B %d, %Y')}
"""
    
    filepath = project_root / 'BRAND_GUIDELINES.md'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(brand_doc)
    
    print(f"✅ Created: {filepath}")


def main():
    """Main rebranding script"""
    print("🎬 SceneIQ Automated Rebranding Script")
    print("=" * 60)
    
    # Get project root
    project_root = Path(__file__).parent
    print(f"📁 Project root: {project_root}")
    
    # Create backup
    print("\n📦 Step 1: Creating backup...")
    backup_dir = backup_project(project_root)
    
    # Update main.py
    print("\n📝 Step 2: Updating main files...")
    main_py = project_root / 'src' / 'main.py'
    if main_py.exists():
        update_main_py(main_py)
    
    # Update README
    readme = project_root / 'README.md'
    if readme.exists():
        update_readme(readme)
    
    # Update LICENSE
    license_file = project_root / 'LICENSE'
    if license_file.exists():
        update_license(license_file)
    
    # Update all other files
    print("\n🔄 Step 3: Updating all project files...")
    updated_files = []
    
    for pattern in FILE_PATTERNS:
        for filepath in project_root.glob(pattern):
            if filepath.is_file() and filepath.name != 'rebrand.py':
                if update_file(filepath, REPLACEMENTS):
                    updated_files.append(filepath)
                    print(f"✅ Updated: {filepath.relative_to(project_root)}")
    
    # Create brand guidelines
    print("\n📚 Step 4: Creating brand guidelines...")
    create_brand_guidelines(project_root)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Rebranding Complete!")
    print(f"✅ Updated {len(updated_files)} files")
    print(f"📦 Backup saved to: {backup_dir.name}")
    print("\n📋 Next Steps:")
    print("1. Review changes: git diff")
    print("2. Test the application: python -m uvicorn src.main:app --reload")
    print("3. Run tests: pytest")
    print("4. Commit changes: git add . && git commit -m 'Rebrand to SceneIQ'")
    print("5. Register domain: pilotforge.com")
    print("\n🚀 Welcome to SceneIQ!")


if __name__ == '__main__':
    main()