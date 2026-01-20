# 🕊️ Pig3on - P2P File Transfer System

A terminal-based peer-to-peer file transfer system that works over WiFi and Bluetooth for seamless file sharing between devices on the same network.

## Features

- **Easy Pairing**: Automatic device discovery and simple yes/no pairing
- **Bidirectional Transfer**: Both devices can send and receive files
- **Live Progress**: Real-time upload/download progress bars
- **Verified Transfers**: SHA256 checksums ensure file integrity
- **Error Handling**: Detects interruptions and connection losses
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Quick Setup

1. **Clone or download** this repository
2. **Navigate** to the pig3on directory
3. **Make executable** (Linux/macOS):
   ```bash
   chmod +x pig3on.py
   ```

### Create Command Alias

#### Windows (PowerShell)
```powershell
# Add to PowerShell profile
notepad $PROFILE

# Add this line:
function pig3on { python C:\path\to\pig3on\pig3on.py $args }
```

#### Linux/macOS (Bash/Zsh)
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'alias pig3on="python3 /path/to/pig3on/pig3on.py"' >> ~/.bashrc
source ~/.bashrc
```

Or create a symlink:
```bash
sudo ln -s /path/to/pig3on/pig3on.py /usr/local/bin/pig3on
```

## Usage

### 1. Start Receiving Mode (Device A)
```bash
pig3on receive
```
This starts listening for incoming connections.

### 2. Connect from Sender (Device B)
```bash
pig3on connect
```
- Scans for nearby devices
- Shows list of available devices
- Select device to connect
- Device A receives pairing request (yes/no)
- Once accepted, both devices are paired!

### 3. Send Files
```bash
pig3on send myfile.pdf
pig3on send image.png
pig3on send document.txt
```

### 4. Check Status
```bash
pig3on status
```

### 5. Disconnect
```bash
pig3on disconnect
```

## File Structure

```
pig3on/
├── pig3on.py              # Main entry point
├── requirements.txt       # Dependencies (none!)
├── README.md             # This file
└── src/
    ├── core/
    │   ├── cli.py        # Command-line interface
    │   ├── config.py     # Configuration manager
    │   ├── connection.py # Connection handling
    │   └── transfer.py   # File transfer logic
    └── utils/
        ├── logger.py     # Logging utility
        ├── progress.py   # Progress bar
        └── crypto.py     # Encryption helper
```

## How It Works

### Discovery
- Uses UDP broadcast on port 37777
- Devices announce their presence
- Scans for 5 seconds to find peers

### Connection
- TCP connection on port 37778
- Pairing confirmation required
- Maintains persistent connection

### File Transfer
- Files split into packets (default 8KB)
- Each packet acknowledged
- SHA256 checksum verification
- Real-time progress tracking

### Error Handling
- **Connection Lost**: "Connection lost during transfer"
- **Interrupted Transfer**: "Interference in data transfer"
- **Cancelled**: "Transfer cancelled by user"
- **Verification Failed**: "File verification failed"

## Example Session

**Device A (Receiver):**
```bash
$ pig3on receive
Listening for incoming files...
Press Ctrl+C to stop

Listening on port 37778
Incoming connection from 192.168.1.100
Accept connection? (yes/no): yes
Paired successfully!

Incoming file: presentation.pdf (2.5 MB)
Downloading presentation.pdf: |████████████████████████████████████████| 100.0% | Completed in 00:12
Saved to: /home/user/Downloads/Pig3on/presentation.pdf
```

**Device B (Sender):**
```bash
$ pig3on connect
Searching for nearby devices...

Found 1 device(s):
  1. Desktop-PC (192.168.1.50)

Connecting to Desktop-PC...
Successfully paired and connected!

$ pig3on send presentation.pdf
Sending: presentation.pdf
Uploading presentation.pdf: |████████████████████████████████████████| 100.0% | Completed in 00:12
File sent successfully!
```

## Network Requirements

- Both devices on same WiFi network
- Firewall allows UDP port 37777 and TCP port 37778
- For Bluetooth: Ensure Bluetooth is enabled (future feature)

## Troubleshooting

### "No devices found"
- Ensure both devices are on the same network
- Check firewall settings
- Make sure one device is in `receive` mode

### "Connection failed"
- Check if ports 37777/37778 are available
- Verify network connectivity
- Try restarting both applications

### "Transfer interrupted"
- Check network stability
- Don't close terminal during transfer
- Ensure sufficient disk space

## Security Notes

- Files are verified with SHA256 checksums
- Only works on local network
- Pairing confirmation required
- No internet connection needed


## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

---

**Made with ❤️ for easy file sharing**