# 🚀 Quick Start: Clone to Visual Studio Code

This is a quick reference guide for cloning the PilotForge repository and opening it in Visual Studio Code.

## Method 1: Using VS Code's Built-in Git (Easiest)

1. **Open VS Code**

2. **Open Command Palette**: 
   - Windows/Linux: `Ctrl+Shift+P`
   - macOS: `Cmd+Shift+P`

3. **Clone Repository**:
   - Type: `Git: Clone`
   - Paste URL: `https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git`
   - Choose a folder to clone into
   - Click "Open" when prompted

4. **Open the Workspace**:
   - Go to `File` → `Open Workspace from File...`
   - Select `PilotForge.code-workspace`

5. **Install Extensions**:
   - Click "Install All" when prompted for recommended extensions

## Method 2: Using Command Line

```bash
# Clone the repository
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform

# Open in VS Code with workspace
code PilotForge.code-workspace

# Or just open the folder
code .
```

## Method 3: GitHub Desktop + VS Code

1. **Open GitHub Desktop**
2. Click `File` → `Clone Repository`
3. Enter: `hneal055/Tax_Incentive_Compliance_Platform`
4. Choose a location and clone
5. Click `Repository` → `Open in Visual Studio Code`
6. In VS Code, open `PilotForge.code-workspace`

## What Happens Next?

After opening the workspace, VS Code will:

1. ✅ **Prompt to install recommended extensions** - Click "Install All"
2. ✅ **Configure Python interpreter** - Select `.venv/bin/python` if prompted
3. ✅ **Load workspace settings** - Automatic formatting, linting, etc.
4. ✅ **Enable debugging configurations** - Press F5 to debug
5. ✅ **Show build tasks** - Press Ctrl+Shift+B to run

## Next Steps

1. **Set up your environment** - Follow the [VS Code Setup Guide](./VSCODE_SETUP.md)
2. **Install dependencies**:
   ```bash
   # Python dependencies
   pip install -r requirements.txt
   
   # Frontend dependencies
   cd frontend && npm install
   ```
3. **Run the application**:
   - Press `Ctrl+Shift+B` (or `Cmd+Shift+B`)
   - Select "Full Stack: Start All"

## Need Help?

- 📖 Full guide: [VSCODE_SETUP.md](./VSCODE_SETUP.md)
- 📚 Project README: [README.md](./README.md)
- 🐛 Issues: [GitHub Issues](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/issues)

---

**You're all set! Happy coding! 🎉**
