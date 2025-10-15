# Educational WiFi Monitor - Installation Guide

This comprehensive guide will help you install and set up the Educational WiFi Monitor on various operating systems.

## 🎯 Prerequisites

### System Requirements

**Minimum Requirements:**
- **Operating System**: Linux (Ubuntu 18.04+), macOS (10.12+), or Windows 10+
- **Python**: 3.6 or higher (3.8+ recommended)
- **RAM**: 4GB (8GB recommended for better performance)
- **Storage**: 1GB free space for installation and data
- **Network**: WiFi adapter (external adapter recommended for Linux)
- **Permissions**: Administrative/root access for installation

**Recommended Setup:**
- **Operating System**: Kali Linux or Ubuntu 20.04+ LTS
- **Python**: 3.8 or higher
- **RAM**: 8GB or more
- **Storage**: 5GB+ free space
- **Network**: External WiFi adapter with monitor mode support
- **Environment**: Virtual machine for isolated testing

### Legal Requirements

⚖️ **Before installation, ensure you:**
1. Understand the legal requirements in your jurisdiction
2. Plan to use this tool only on networks you own or have permission to test
3. Have read and agreed to the legal disclaimer
4. Intend to use this for educational purposes only

## 🐧 Linux Installation

### Ubuntu/Debian Systems

**Step 1: Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

**Step 2: Install System Dependencies**
```bash
sudo apt install -y python3 python3-pip python3-venv git curl wget
sudo apt install -y wireless-tools net-tools iw aircrack-ng
```

**Step 3: Clone Repository**
```bash
git clone <repository-url>
cd EthicalWiFiMonitor
```

**Step 4: Run Installation Script**
```bash
sudo ./scripts/install_dependencies.sh
```

**Step 5: Setup Environment**
```bash
./scripts/setup_environment.sh
```

### CentOS/RHEL/Fedora Systems

**Step 1: Update System**
```bash
# CentOS/RHEL
sudo yum update -y

# Fedora
sudo dnf update -y
```

**Step 2: Install Dependencies**
```bash
# CentOS/RHEL
sudo yum install -y python3 python3-pip git wireless-tools net-tools iw

# Fedora
sudo dnf install -y python3 python3-pip git wireless-tools net-tools iw
```

**Step 3: Continue with Common Steps**
```bash
git clone <repository-url>
cd EthicalWiFiMonitor
sudo ./scripts/install_dependencies.sh
./scripts/setup_environment.sh
```

### Kali Linux (Recommended for Security Testing)

Kali Linux comes with most required tools pre-installed:

**Step 1: Update Kali**
```bash
sudo apt update && sudo apt upgrade -y
```

**Step 2: Install Python Virtual Environment**
```bash
sudo apt install -y python3-venv
```

**Step 3: Clone and Install**
```bash
git clone <repository-url>
cd EthicalWiFiMonitor
sudo ./scripts/install_dependencies.sh
```

### Arch Linux

**Step 1: Update System**
```bash
sudo pacman -Syu
```

**Step 2: Install Dependencies**
```bash
sudo pacman -S python python-pip git wireless_tools net-tools iw
```

**Step 3: Continue Installation**
```bash
git clone <repository-url>
cd EthicalWiFiMonitor
sudo ./scripts/install_dependencies.sh
```

## 🍎 macOS Installation

### Using Homebrew (Recommended)

**Step 1: Install Homebrew** (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2: Install Python and Git**
```bash
brew install python3 git
```

**Step 3: Clone Repository**
```bash
git clone <repository-url>
cd EthicalWiFiMonitor
```

**Step 4: Run Installation**
```bash
./scripts/install_dependencies.sh
```

**Note**: macOS has limited WiFi monitoring capabilities compared to Linux. Some features may require additional tools or have reduced functionality.

### macOS-Specific Considerations

- **Airport Utility**: Required for advanced WiFi scanning
- **System Permissions**: May require additional security permissions
- **Limited Monitor Mode**: Most built-in adapters don't support monitor mode
- **External Adapters**: Consider USB WiFi adapters for enhanced functionality

## 🪟 Windows Installation

### Windows Subsystem for Linux (WSL2) - Recommended

**Step 1: Enable WSL2**
```powershell
# Run in PowerShell as Administrator
wsl --install
```

**Step 2: Install Ubuntu from Microsoft Store**
- Open Microsoft Store
- Search for "Ubuntu" and install latest LTS version
- Launch Ubuntu and complete setup

**Step 3: Follow Ubuntu Installation Steps**
```bash
sudo apt update && sudo apt upgrade -y
cd /mnt/c/Users/<YourUsername>/Documents
git clone <repository-url>
cd EthicalWiFiMonitor
sudo ./scripts/install_dependencies.sh
```

### Native Windows Installation

**Prerequisites:**
- Python 3.8+ installed from python.org
- Git for Windows installed
- Administrative privileges

**Step 1: Install Python and Git**
1. Download Python from https://python.org
2. Download Git from https://git-scm.com
3. Ensure "Add to PATH" is selected during installation

**Step 2: Clone Repository**
```cmd
git clone <repository-url>
cd EthicalWiFiMonitor
```

**Step 3: Install Python Dependencies**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Windows Limitations:**
- Limited WiFi scanning capabilities
- No monitor mode support for most adapters
- Reduced functionality compared to Linux
- Consider using WSL2 or a Linux VM for full features

## 📦 Manual Installation

If the automated scripts don't work for your system:

### Step 1: Python Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Python Dependencies

```bash
pip install scapy>=2.4.5
pip install psutil>=5.8.0
pip install netifaces>=0.11.0
pip install pandas>=1.3.0
pip install tabulate>=0.9.0
pip install colorama>=0.4.4
pip install jsonschema>=3.2.0
pip install python-dotenv>=0.19.0
```

### Step 3: System Tools Installation

**Linux:**
```bash
sudo apt install wireless-tools net-tools iw  # Ubuntu/Debian
sudo yum install wireless-tools net-tools iw  # CentOS/RHEL
```

**macOS:**
```bash
# Most tools are built-in, but you may need:
brew install wireless-tools  # If available
```

**Windows:**
```cmd
# Built-in tools are used (netsh, netstat)
# No additional installation needed
```

## 🔧 Post-Installation Configuration

### Verify Installation

**Step 1: Activate Environment**
```bash
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
```

**Step 2: Test Installation**
```bash
python3 main.py --help
```

**Step 3: Run Basic Test**
```bash
python3 -c "
import scapy
import psutil
import pandas
print('✅ All core dependencies imported successfully')
"
```

### Configuration Files

**Step 1: Review Settings**
```bash
cat config/settings.json
```

**Step 2: Read Legal Disclaimer**
```bash
cat config/legal_disclaimer.txt
```

**Step 3: Create Log Directories**
```bash
mkdir -p logs results reports backups
```

## 🌐 Network Interface Configuration

### Linux WiFi Interface Setup

**Step 1: Check Available Interfaces**
```bash
iwconfig
# or
ip link show
```

**Step 2: Enable Monitor Mode (if supported)**
```bash
# Replace wlan0 with your interface
sudo ip link set wlan0 down
sudo iw wlan0 set monitor control
sudo ip link set wlan0 up
```

**Step 3: Test Interface**
```bash
iwconfig  # Should show monitor mode
```

### External WiFi Adapter Recommendations

**For Enhanced Functionality (Linux):**
- **Alfa AWUS036NHA** - Popular for security testing
- **Panda PAU09** - Good budget option
- **TP-Link AC600 T2U Plus** - Modern dual-band option
- **Alfa AWUS036ACS** - 802.11ac support

**Key Features to Look For:**
- Monitor mode support
- Packet injection capability
- Good Linux driver support
- Adequate transmission power

## 🚀 Quick Start Verification

### Test Basic Functionality

**Step 1: Start Interactive Mode**
```bash
./scripts/run_monitor.sh
# Select option 1 (Interactive Learning Mode)
```

**Step 2: Test Network Scanning (Authorized Only)**
```bash
python3 main.py --scan
# Ensure you have proper authorization first
```

**Step 3: View Educational Content**
```bash
python3 main.py --interactive
# Explore the learning modules
```

## 🐛 Troubleshooting

### Common Issues and Solutions

**1. "No wireless interfaces found"**
```bash
# Check if wireless adapter is connected
lsusb  # Look for wireless adapters
iwconfig  # Check interface status
sudo modprobe <driver_name>  # Load driver if needed
```

**2. "Permission denied" errors**
```bash
# Ensure user has proper permissions
sudo usermod -a -G netdev $USER
# Log out and back in
```

**3. "Python module not found"**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

**4. "Monitor mode not supported"**
- Use external WiFi adapter with monitor mode support
- Check adapter chipset compatibility
- Consider using USB WiFi adapter designed for security testing

**5. "Scapy import errors"**
```bash
# Install scapy with specific version
pip install scapy==2.4.5
# Or install from source
pip install https://github.com/secdev/scapy/archive/master.zip
```

### Platform-Specific Issues

**Linux:**
- Driver issues with certain WiFi chipsets
- Permission problems with wireless interfaces
- Conflicts with NetworkManager

**macOS:**
- Limited monitor mode support
- System Integrity Protection restrictions
- Airport utility access issues

**Windows:**
- Limited WiFi scanning capabilities
- No monitor mode support
- Antivirus interference with network tools

## 🔄 Updating the Tool

### Update Installation

```bash
# Pull latest changes
git pull origin main

# Update Python dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Run setup again if needed
./scripts/setup_environment.sh
```

## 📞 Support

### Getting Help

**Documentation:**
- Read all files in the `docs/` directory
- Check configuration files in `config/`
- Review error logs in `logs/` directory

**Community Resources:**
- Cybersecurity forums and communities
- Educational institutions and programs
- Professional training organizations

**Professional Development:**
- Consider formal cybersecurity training
- Pursue relevant certifications
- Join professional organizations

---

**Remember**: This tool is for educational purposes only. Always ensure you have proper authorization before testing any networks, and use your new skills to make the digital world more secure! 🛡️
