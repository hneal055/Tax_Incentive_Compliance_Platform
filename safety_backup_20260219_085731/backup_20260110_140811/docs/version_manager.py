"""
PilotForge Version Management Automation
Automatically bumps version numbers across all files
"""
import re
import sys
from pathlib import Path
from datetime import datetime

VERSION_FILES = {
    'src/main.py': [
        (r'version="[^"]*"', 'version="{version}"'),
    ],
    'pyproject.toml': [
        (r'version = "[^"]*"', 'version = "{version}"'),
    ],
    'README.md': [
        (r'Version: [0-9.]+', 'Version: {version}'),
    ],
}

CHANGELOG_TEMPLATE = """# Changelog - PilotForge

All notable changes to PilotForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features go here

### Changed
- Changes go here

### Fixed
- Bug fixes go here

{existing_content}
"""


def get_current_version():
    """Extract current version from main.py"""
    main_py = Path('src/main.py')
    content = main_py.read_text()
    match = re.search(r'version="([^"]*)"', content)
    return match.group(1) if match else "0.1.0"


def parse_version(version_str):
    """Parse semantic version string"""
    match = re.match(r'(\d+)\.(\d+)\.(\d+)', version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    return tuple(map(int, match.groups()))


def bump_version(version_str, bump_type='patch'):
    """Bump version number"""
    major, minor, patch = parse_version(version_str)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


def update_version_in_files(new_version):
    """Update version in all relevant files"""
    updated_files = []
    
    for filepath, patterns in VERSION_FILES.items():
        file_path = Path(filepath)
        if not file_path.exists():
            print(f"⚠️  Skipping {filepath} (not found)")
            continue
        
        content = file_path.read_text()
        original_content = content
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement.format(version=new_version), content)
        
        if content != original_content:
            file_path.write_text(content)
            updated_files.append(filepath)
            print(f"✅ Updated {filepath}")
    
    return updated_files


def update_changelog(new_version):
    """Update CHANGELOG.md with new version"""
    changelog_path = Path('CHANGELOG.md')
    
    if not changelog_path.exists():
        # Create new changelog
        changelog_path.write_text(CHANGELOG_TEMPLATE.format(existing_content=''))
        print("📝 Created CHANGELOG.md")
        return
    
    content = changelog_path.read_text()
    
    # Check if this version already exists
    if f"## [{new_version}]" in content:
        print(f"ℹ️  Version {new_version} already in CHANGELOG")
        return
    
    # Add new version entry
    today = datetime.now().strftime('%Y-%m-%d')
    new_entry = f"""
## [{new_version}] - {today}

### Added
- Feature additions for this release

### Changed
- Changes in this release

### Fixed
- Bug fixes in this release

"""
    
    # Insert after [Unreleased]
    content = re.sub(
        r'(## \[Unreleased\].*?\n)',
        r'\1' + new_entry,
        content,
        flags=re.DOTALL
    )
    
    changelog_path.write_text(content)
    print(f"✅ Updated CHANGELOG.md with v{new_version}")


def create_git_tag(version):
    """Create git tag for version"""
    import subprocess
    
    try:
        # Create annotated tag
        subprocess.run([
            'git', 'tag', '-a', f'v{version}',
            '-m', f'PilotForge v{version}'
        ], check=True)
        
        print(f"✅ Created git tag v{version}")
        print("\n📤 To push tag: git push origin v{version}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create git tag: {e}")


def main():
    """Main version management script"""
    print("🎬 PilotForge Version Management")
    print("=" * 60)
    
    # Get current version
    current_version = get_current_version()
    print(f"📊 Current version: {current_version}")
    
    # Determine bump type
    if len(sys.argv) < 2:
        print("\nUsage: python version_manager.py [major|minor|patch]")
        print("\nExamples:")
        print("  python version_manager.py patch  # 1.0.0 → 1.0.1")
        print("  python version_manager.py minor  # 1.0.1 → 1.1.0")
        print("  python version_manager.py major  # 1.1.0 → 2.0.0")
        sys.exit(1)
    
    bump_type = sys.argv[1].lower()
    if bump_type not in ['major', 'minor', 'patch']:
        print(f"❌ Invalid bump type: {bump_type}")
        print("   Must be: major, minor, or patch")
        sys.exit(1)
    
    # Calculate new version
    new_version = bump_version(current_version, bump_type)
    print(f"🆕 New version: {new_version}")
    
    # Confirm
    response = input(f"\n⚠️  Bump version from {current_version} to {new_version}? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        sys.exit(0)
    
    # Update files
    print(f"\n📝 Updating version to {new_version}...")
    updated_files = update_version_in_files(new_version)
    
    # Update changelog
    update_changelog(new_version)
    
    # Create git tag
    create_tag = input("\n🏷️  Create git tag? (y/N): ")
    if create_tag.lower() == 'y':
        create_git_tag(new_version)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Version bump complete!")
    print(f"\n📊 Version: {current_version} → {new_version}")
    print(f"📝 Updated {len(updated_files)} files")
    print("\n📋 Next steps:")
    print("1. Review changes: git diff")
    print("2. Update CHANGELOG.md with details")
    print(f"3. Commit: git add . && git commit -m 'Bump version to {new_version}'")
    print("4. Push: git push origin main")
    if create_tag.lower() == 'y':
        print(f"5. Push tag: git push origin v{new_version}")
    print("\n🚀 PilotForge v{} ready!".format(new_version))


if __name__ == '__main__':
    main()