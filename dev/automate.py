"""
PilotForge Master Automation Runner
One command to automate everything!
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime


AUTOMATIONS = {
    'rebrand': {
        'name': 'Rebrand to PilotForge',
        'script': 'rebrand.py',
        'description': 'Update all files with PilotForge branding',
        'requires_api': False
    },
    'version': {
        'name': 'Version Management',
        'script': 'version_manager.py',
        'description': 'Bump version numbers across project',
        'requires_api': False,
        'args': True
    },
    'docs': {
        'name': 'Generate Documentation',
        'script': 'generate_docs.py',
        'description': 'Auto-generate API docs from OpenAPI spec',
        'requires_api': True
    },
    'test': {
        'name': 'Run Test Suite',
        'command': 'pytest --cov=src --cov-report=html',
        'description': 'Run all tests with coverage',
        'requires_api': False
    },
    'lint': {
        'name': 'Code Quality Check',
        'command': 'flake8 src/ tests/ --max-line-length=120',
        'description': 'Check code quality and style',
        'requires_api': False
    },
    'format': {
        'name': 'Auto-Format Code',
        'command': 'black src/ tests/ && isort src/ tests/',
        'description': 'Format code with Black and isort',
        'requires_api': False
    },
    'all': {
        'name': 'Full Quality Check',
        'description': 'Run tests, linting, and documentation',
        'requires_api': True
    }
}


def print_banner():
    """Print PilotForge banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎬 PilotForge Automation Suite                         ║
║   Tax Incentive Intelligence for Film & TV               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def run_command(command, description):
    """Run a shell command"""
    print(f"\n▶️  {description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed!")
        if e.stderr:
            print(e.stderr)
        return False


def run_script(script_name, description, args=None):
    """Run a Python script"""
    print(f"\n▶️  {description}")
    print(f"   Script: {script_name}")
    
    command = [sys.executable, script_name]
    if args:
        command.extend(args)
    
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed!")
        if e.stderr:
            print(e.stderr)
        return False


def check_api_running():
    """Check if API is running"""
    import httpx
    try:
        response = httpx.get('http://localhost:8000/', timeout=2)
        return response.status_code == 200
    except:
        return False


def list_automations():
    """List all available automations"""
    print("\n📋 Available Automations:\n")
    
    for key, automation in AUTOMATIONS.items():
        print(f"  {key:12} - {automation['name']}")
        print(f"               {automation['description']}")
        if automation.get('requires_api'):
            print(f"               ⚠️  Requires API running")
        print()


def run_automation(automation_key, args=None):
    """Run a specific automation"""
    if automation_key not in AUTOMATIONS:
        print(f"❌ Unknown automation: {automation_key}")
        return False
    
    automation = AUTOMATIONS[automation_key]
    
    # Check if API is required and running
    if automation.get('requires_api') and not check_api_running():
        print(f"\n⚠️  {automation['name']} requires the API to be running")
        print("   Start it with: python -m uvicorn src.main:app --reload")
        return False
    
    # Special handling for 'all'
    if automation_key == 'all':
        print(f"\n🚀 Running Full Quality Check...")
        success = True
        success &= run_automation('test')
        success &= run_automation('lint')
        if check_api_running():
            success &= run_automation('docs')
        else:
            print("\n⚠️  Skipping docs generation (API not running)")
        return success
    
    # Run script or command
    if 'script' in automation:
        return run_script(
            automation['script'],
            automation['name'],
            args=args
        )
    elif 'command' in automation:
        return run_command(
            automation['command'],
            automation['name']
        )
    
    return False


def interactive_mode():
    """Interactive automation selection"""
    print_banner()
    list_automations()
    
    print("📝 Select automation (or 'exit' to quit):")
    choice = input("   > ").strip().lower()
    
    if choice == 'exit':
        print("👋 Goodbye!")
        return
    
    if choice not in AUTOMATIONS:
        print(f"❌ Unknown automation: {choice}")
        return interactive_mode()
    
    # Get args if needed
    args = None
    if AUTOMATIONS[choice].get('args'):
        print("\n📝 Additional arguments (press Enter for none):")
        arg_input = input("   > ").strip()
        if arg_input:
            args = arg_input.split()
    
    # Run automation
    success = run_automation(choice, args)
    
    # Show summary
    print("\n" + "=" * 60)
    if success:
        print("✅ Automation completed successfully!")
    else:
        print("❌ Automation failed!")
    
    # Ask to run another
    print("\n📝 Run another automation? (y/N):")
    again = input("   > ").strip().lower()
    if again == 'y':
        return interactive_mode()


def main():
    """Main automation runner"""
    if len(sys.argv) == 1:
        # No arguments - interactive mode
        interactive_mode()
    elif sys.argv[1] == 'list':
        # List automations
        print_banner()
        list_automations()
    else:
        # Run specific automation
        automation_key = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else None
        
        print_banner()
        success = run_automation(automation_key, args)
        
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()