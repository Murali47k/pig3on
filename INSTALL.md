# Pig3on Installation Guide

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation Methods

### Method 1: Direct Use (No Installation)

1. Download or clone the repository
2. Navigate to the pig3on directory
3. Run directly:
   ```bash
   python pig3on.py connect
   ```

### Method 2: Install as Package (Recommended)

#### Windows

```powershell
# Navigate to pig3on directory
cd path\to\pig3on

# Install
pip install -e .

# Now you can use from anywhere:
pig3on connect
```

#### Linux/macOS

```bash
# Navigate to pig3on directory
cd /path/to/pig3on

# Install
pip3 install -e .

# Now you can use from anywhere:
pig3on connect
```

### Method 3: Create Alias/Shortcut

#### Windows PowerShell

1. Find your PowerShell profile location:
   ```powershell
   $PROFILE
   ```

2. Edit the profile (create if doesn't exist):
   ```powershell
   notepad $PROFILE
   ```

3. Add this line (replace with your actual path):
   ```powershell
   function pig3on { python C:\path\to\pig3on\pig3on.py $args }
   ```

4. Reload profile:
   ```powershell
   . $PROFILE
   ```

#### Windows Command Prompt

1. Create `pig3on.bat` in a folder that's in your PATH (like `C:\Windows\System32`)
2. Add this content:
   ```batch
   @echo off
   python C:\path\to\pig3on\pig3on.py %*
   ```

#### Linux/macOS

**Option A: Alias (Current user only)**

```bash
# For Bash
echo 'alias pig3on="python3 /path/to/pig3on/pig3on.py"' >> ~/.bashrc
source ~/.bashrc

# For Zsh
echo 'alias pig3on="python3 /path/to/pig3on/pig3on.py"' >> ~/.zshrc
source ~/.zshrc
```

**Option B: Symlink (System-wide)**

```bash
# Make script executable
chmod +x /path/to/pig3on/pig3on.py

# Create symlink
sudo ln -s /path/to/pig3on/pig3on.py /usr/local/bin/pig3on
```

## Verify Installation

```bash
pig3on help
```

You should see the help message.

## First Run

On first run, Pig3on will:
- Create config directory at `~/.pig3on/`
- Create download directory at `~/Downloads/Pig3on/`
- Generate device name from hostname

## Firewall Configuration

### Windows Firewall

```powershell
# Allow inbound connections
New-NetFirewallRule -DisplayName "Pig3on Discovery" -Direction Inbound -Protocol UDP -LocalPort 37777 -Action Allow
New-NetFirewallRule -DisplayName "Pig3on Transfer" -Direction Inbound -Protocol TCP -LocalPort 37778 -Action Allow
```

### Linux (UFW)

```bash
sudo ufw allow 37777/udp
sudo ufw allow 37778/tcp
```

### macOS

System Preferences > Security & Privacy > Firewall > Firewall Options
- Allow incoming connections for Python

## Uninstall

### If installed via pip:
```bash
pip uninstall pig3on
```

### If using alias:
Remove the alias line from your shell config file

### If using symlink:
```bash
sudo rm /usr/local/bin/pig3on
```

### Clean up config:
```bash
rm -rf ~/.pig3on
```

## Troubleshooting

### "python: command not found"
- Install Python from python.org
- On Windows, use `py` instead of `python`

### Permission denied (Linux/macOS)
```bash
chmod +x pig3on.py
```

### Module not found errors
- Ensure you're in the correct directory
- Check Python version: `python --version`

### Firewall blocking connections
- See firewall configuration above
- Temporarily disable firewall to test

## Testing

1. Open two terminals
2. Terminal 1: `pig3on receive`
3. Terminal 2: `pig3on connect`
4. Accept pairing
5. Terminal 2: `pig3on send test.txt`

## Support

For issues and questions:
- Check README.md
- Open an issue on GitHub
- Check firewall and network settings