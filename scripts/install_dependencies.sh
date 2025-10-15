#!/bin/bash
# Educational WiFi Monitor - Dependency Installation Script

set -e  # Exit on any error

echo "=================================================="
echo "    Educational WiFi Monitor - Setup Script"
echo "=================================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root for system package installation
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. This is required for system package installation."
    else
        print_warning "Not running as root. You may need to run with sudo for system packages."
    fi
}

# Detect operating system
detect_os() {
    print_status "Detecting operating system..."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if command -v apt-get &> /dev/null; then
            DISTRO="debian"
            PACKAGE_MANAGER="apt-get"
        elif command -v yum &> /dev/null; then
            DISTRO="redhat"
            PACKAGE_MANAGER="yum"
        elif command -v dnf &> /dev/null; then
            DISTRO="fedora"
            PACKAGE_MANAGER="dnf"
        elif command -v pacman &> /dev/null; then
            DISTRO="arch"
            PACKAGE_MANAGER="pacman"
        else
            print_error "Unsupported Linux distribution"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        PACKAGE_MANAGER="brew"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi

    print_success "Detected $OS ($DISTRO) with $PACKAGE_MANAGER"
}

# Install system dependencies
install_system_packages() {
    print_status "Installing system dependencies..."

    case $OS in
        "linux")
            case $DISTRO in
                "debian")
                    print_status "Installing packages for Debian/Ubuntu..."
                    $PACKAGE_MANAGER update
                    $PACKAGE_MANAGER install -y python3 python3-pip python3-venv wireless-tools net-tools iw
                    ;;
                "redhat"|"fedora")
                    print_status "Installing packages for RedHat/CentOS/Fedora..."
                    $PACKAGE_MANAGER install -y python3 python3-pip wireless-tools net-tools iw
                    ;;
                "arch")
                    print_status "Installing packages for Arch Linux..."
                    $PACKAGE_MANAGER -S python python-pip wireless_tools net-tools iw --noconfirm
                    ;;
            esac
            ;;
        "macos")
            if ! command -v brew &> /dev/null; then
                print_error "Homebrew not found. Please install Homebrew first:"
                print_error "https://brew.sh/"
                exit 1
            fi
            print_status "Installing packages for macOS..."
            brew install python3
            ;;
    esac

    print_success "System packages installed successfully"
}

# Check Python installation
check_python() {
    print_status "Checking Python installation..."

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"

        # Check if version is 3.6 or higher
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 6 ]; then
            print_success "Python version is compatible"
        else
            print_error "Python 3.6 or higher required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.6 or higher."
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating Python virtual environment..."

    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf venv
    fi

    python3 -m venv venv
    print_success "Virtual environment created"
}

# Install Python dependencies
install_python_packages() {
    print_status "Installing Python dependencies..."

    # Activate virtual environment
    source venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip

    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Python packages installed from requirements.txt"
    else
        # Install basic packages manually
        pip install scapy psutil netifaces pandas tabulate colorama jsonschema python-dotenv
        print_success "Basic Python packages installed"
    fi

    deactivate
}

# Create necessary directories
create_directories() {
    print_status "Creating project directories..."

    mkdir -p logs
    mkdir -p results
    mkdir -p reports
    mkdir -p backups

    print_success "Project directories created"
}

# Set permissions
set_permissions() {
    print_status "Setting appropriate permissions..."

    # Make shell scripts executable
    chmod +x scripts/*.sh 2>/dev/null || true
    chmod +x *.py 2>/dev/null || true

    print_success "Permissions set"
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."

    # Activate virtual environment
    source venv/bin/activate

    # Test Python imports
    python3 -c "
import sys
try:
    import scapy
    import psutil
    import pandas
    import json
    print('✅ All required Python packages imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

    deactivate

    print_success "Installation verification completed"
}

# Main installation process
main() {
    echo "🚀 Starting Educational WiFi Monitor installation..."
    echo

    # Check prerequisites
    detect_os
    check_root

    # Install dependencies
    install_system_packages
    check_python
    create_venv
    install_python_packages

    # Setup project
    create_directories
    set_permissions

    # Verify everything works
    verify_installation

    echo
    echo "=================================================="
    print_success "Installation completed successfully!"
    echo "=================================================="
    echo
    echo "📋 Next steps:"
    echo "1. Review the legal disclaimer: cat config/legal_disclaimer.txt"
    echo "2. Read the documentation: cat docs/README.md"
    echo "3. Activate virtual environment: source venv/bin/activate"
    echo "4. Run the tool: python3 main.py --help"
    echo
    echo "⚠️  IMPORTANT: Only use on networks you own or have permission to test!"
    echo
}

# Run main function
main "$@"
