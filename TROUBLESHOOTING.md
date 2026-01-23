# 🔧 Troubleshooting Guide

This guide covers common issues when setting up and running the Tax Incentive Compliance Platform on Windows.

---

## Python Issues

### Issue: "Python not found in PATH"

**Symptom:**
```
❌ Python 3.12 not found!
```
The start.ps1 script cannot locate Python 3.12 on your system.

**Cause:**
Python 3.12 is either not installed, or it wasn't added to your system PATH during installation.

**Fix:**
1. **Verify Python is installed:**
   ```powershell
   py --list
   ```
   Look for a line like `-V:3.12` in the output.

2. **If Python 3.12 is listed but not in PATH:**
   - Find your Python installation (usually `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312`)
   - Add it to PATH:
     ```powershell
     # Run as Administrator
     [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312;C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\Scripts", "Machine")
     ```
   - Restart PowerShell and try again

3. **If Python 3.12 is NOT installed:**
   - Download from https://www.python.org/downloads/
   - During installation, **CHECK ✓ "Add Python to PATH"**
   - Complete installation and run `.\start.ps1` again

4. **Use Python Launcher (recommended):**
   ```powershell
   py -3.12 --version
   ```
   If this works, the start.ps1 script should find it automatically.

---

### Issue: "Wrong Python version"

**Symptom:**
```
⚠ Virtual environment has wrong version: Python 3.10.x
Recreating with Python 3.12...
```

**Cause:**
Your `.venv` directory was created with a different Python version (e.g., 3.10, 3.11) instead of 3.12.

**Fix:**
The `start.ps1` script will **automatically fix this** by:
1. Detecting the version mismatch
2. Removing the old `.venv`
3. Creating a new one with Python 3.12

If you want to manually fix it:
```powershell
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
```

---

### Issue: "Script execution policy errors"

**Symptom:**
```
.\start.ps1 : File cannot be loaded because running scripts is disabled on this system.
```

**Cause:**
PowerShell's execution policy prevents running scripts for security reasons.

**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try running `.\start.ps1` again.

**Note:** This only affects the current user and allows locally-created scripts to run.

---

## Virtual Environment Issues

### Issue: ".venv contains wrong Python version"

**Symptom:**
Virtual environment was created with Python 3.10 or 3.11 instead of 3.12.

**Cause:**
The `py -3.12` command wasn't available when `.venv` was first created, so it used the default Python version.

**Fix:**
The `start.ps1` script **auto-fixes this**. Just run:
```powershell
.\start.ps1
```

The script will:
1. Check the Python version in `.venv`
2. Delete the old `.venv` if version is wrong
3. Create a new one with Python 3.12

---

### Issue: "Unable to activate venv"

**Symptom:**
```
.\.venv\Scripts\Activate.ps1 : File cannot be loaded
```

**Cause:**
PowerShell execution policy blocks the activation script.

**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alternative:** Use the start.ps1 script which handles activation automatically.

---

## Docker Issues

### Issue: "Docker Desktop not running"

**Symptom:**
```
❌ Docker Desktop is not running
```

**Cause:**
Docker Desktop application is not started or not installed.

**Fix:**
1. **Check if Docker Desktop is installed:**
   - Look for Docker Desktop in your Start Menu
   - If not installed, download from: https://www.docker.com/products/docker-desktop/

2. **Start Docker Desktop:**
   - Open Docker Desktop from Start Menu
   - Wait for the whale icon in system tray to become steady (not animating)
   - This can take 30-60 seconds on first start

3. **Verify Docker is running:**
   ```powershell
   docker version
   ```
   You should see both Client and Server version information.

4. **Run start.ps1 again:**
   ```powershell
   .\start.ps1
   ```

---

### Issue: "PostgreSQL container won't start"

**Symptom:**
```
❌ Failed to create container
```
or
```
Error response from daemon: Conflict. The container name "/tax-incentive-db" is already in use
```

**Cause:**
- Container exists but is corrupted
- Port 5432 is already in use by another process
- Docker volume is corrupted

**Fix:**

1. **View container logs:**
   ```powershell
   docker logs tax-incentive-db
   ```
   Look for error messages.

2. **Remove and recreate container:**
   ```powershell
   docker-compose down
   docker rm tax-incentive-db
   docker-compose up -d
   ```

3. **If problems persist, reset everything:**
   ```powershell
   # Stop and remove container + volumes
   docker-compose down -v
   
   # Recreate from scratch
   docker-compose up -d
   ```

4. **Check if container is running:**
   ```powershell
   docker ps
   ```
   You should see `tax-incentive-db` in the list.

---

### Issue: "Port 5432 already in use"

**Symptom:**
```
Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address already in use
```

**Cause:**
Another PostgreSQL instance or application is using port 5432.

**Fix:**

1. **Find what's using port 5432:**
   ```powershell
   netstat -ano | findstr :5432
   ```
   Note the PID (last column).

2. **Stop the conflicting process:**
   ```powershell
   # Find process name
   tasklist | findstr <PID>
   
   # Stop it (if it's postgres.exe or another db)
   Stop-Process -Id <PID>
   ```

3. **Or change the port in docker-compose.yml:**
   ```yaml
   ports:
     - "5433:5432"  # Use 5433 externally instead
   ```
   Then update your `.env` file:
   ```
   DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/tax_incentive_db
   ```

---

## Dependencies Issues

### Issue: "Packages not installing"

**Symptom:**
```
ERROR: Could not find a version that satisfies the requirement...
```
or
```
⚠ Some dependencies may have failed to install
```

**Cause:**
- Not in activated virtual environment
- pip is outdated
- Network connectivity issues
- Package version conflicts

**Fix:**

1. **Verify you're in the virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   python --version  # Should show Python 3.12.x
   ```

2. **Upgrade pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

3. **Install requirements again:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Install specific failing package manually:**
   ```powershell
   pip install <package-name>
   ```

5. **Check for version conflicts:**
   ```powershell
   pip check
   ```

**Note:** The `start.ps1` script automatically handles most dependency installation.

---

### Issue: "Prisma errors"

**Symptom:**
```
Error: Prisma Client is not generated
```
or
```
ImportError: cannot import name 'Prisma' from 'prisma'
```

**Cause:**
Prisma client needs to be generated after installation or schema changes.

**Fix:**

1. **Generate Prisma client:**
   ```powershell
   .\.venv\Scripts\python.exe -m prisma generate
   ```

2. **If schema.prisma changed, regenerate:**
   ```powershell
   cd prisma
   .\..\venv\Scripts\python.exe -m prisma generate
   ```

3. **Database migrations (if needed):**
   ```powershell
   .\.venv\Scripts\python.exe -m prisma migrate dev
   ```

**Note:** The `start.ps1` script automatically runs `prisma generate` if the prisma directory exists.

---

## Network/Port Issues

### Issue: "Port 8000 already in use"

**Symptom:**
```
ERROR:    [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```

**Cause:**
Another instance of the application or a different program is using port 8000.

**Fix:**

1. **Find what's using port 8000:**
   ```powershell
   netstat -ano | findstr :8000
   ```

2. **Stop the process:**
   ```powershell
   # Get PID from previous command
   Stop-Process -Id <PID>
   ```

3. **Or use a different port:**
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn src.main:app --reload --port 8001
   ```
   Then access at: http://localhost:8001

---

### Issue: "Can't access http://localhost:8000"

**Symptom:**
Browser shows "This site can't be reached" or "Connection refused"

**Cause:**
- Server didn't start successfully
- Firewall blocking the connection
- Server bound to wrong interface

**Fix:**

1. **Check if server is running:**
   ```powershell
   netstat -ano | findstr :8000
   ```
   If nothing appears, the server isn't running.

2. **Look for error messages in the terminal where you ran start.ps1**

3. **Check Windows Firewall:**
   - Go to Windows Security → Firewall & network protection
   - Click "Allow an app through firewall"
   - Make sure Python is allowed for Private networks

4. **Try accessing via 127.0.0.1:**
   ```
   http://127.0.0.1:8000
   ```

5. **Check server logs for errors:**
   The terminal running `start.ps1` will show all server logs and errors.

---

## General Tips

### Best Practices

1. **Always run PowerShell from project root directory**
   ```powershell
   cd C:\Users\<YourUsername>\Tax_Incentive_Compliance_Platform
   ```

2. **Use `.\start.ps1` not `start.ps1`**
   PowerShell security requires the `.\` prefix for local scripts.

3. **Check Docker Desktop is running before starting**
   Look for the whale icon in your system tray (bottom-right of screen).

4. **Keep Python 3.12 and Docker Desktop up to date**
   ```powershell
   # Check Python version
   py -3.12 --version
   
   # Update pip
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   ```

---

### Nuclear Option: Complete Reset

If nothing else works, perform a complete reset:

```powershell
# 1. Stop and remove all Docker containers and volumes
docker-compose down -v

# 2. Remove virtual environment
Remove-Item -Recurse -Force .venv

# 3. Remove .env (will be recreated)
Remove-Item .env

# 4. Run start.ps1 to rebuild everything
.\start.ps1
```

This will:
- ✅ Recreate the virtual environment with Python 3.12
- ✅ Reinstall all dependencies
- ✅ Create a fresh PostgreSQL container
- ✅ Generate a new .env file

---

## Still Having Issues?

If you've tried all the above and still have problems:

1. **Check the GitHub Issues page** for similar problems
2. **Collect diagnostic information:**
   ```powershell
   # Python version
   py --list
   python --version
   
   # Docker status
   docker version
   docker ps -a
   
   # Port usage
   netstat -ano | findstr :8000
   netstat -ano | findstr :5432
   ```

3. **Create a new issue** with:
   - Error messages (full text)
   - Output from diagnostic commands above
   - Steps you've already tried
   - Your Windows version

---

## Quick Checklist

Before asking for help, verify:

- [ ] Python 3.12 is installed (`py -3.12 --version`)
- [ ] Docker Desktop is running (whale icon in system tray)
- [ ] You're in the project directory
- [ ] Execution policy allows scripts (`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)
- [ ] Ports 8000 and 5432 are not in use by other applications
- [ ] You've tried the "Nuclear Option" reset above
