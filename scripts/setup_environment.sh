#!/bin/bash
# Educational WiFi Monitor - Environment Setup Script

set -e

echo "=================================================="
echo "    Educational WiFi Monitor - Environment Setup"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        print_error "Virtual environment not found. Run install_dependencies.sh first."
        exit 1
    fi
    print_success "Virtual environment found"
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Check wireless interface
check_wireless_interface() {
    print_info "Checking for wireless interfaces..."

    if command -v iwconfig &> /dev/null; then
        INTERFACES=$(iwconfig 2>/dev/null | grep "IEEE 802.11" | cut -d' ' -f1)
        if [ -n "$INTERFACES" ]; then
            print_success "Wireless interfaces found: $INTERFACES"
            echo "export WIFI_INTERFACE=$(echo $INTERFACES | head -n1)" >> ~/.bashrc
        else
            print_error "No wireless interfaces found"
        fi
    elif command -v ip &> /dev/null; then
        print_info "Using ip command to check interfaces..."
        ip link show | grep -E "(wlan|wlp)"
    else
        print_error "Cannot check wireless interfaces (no iwconfig or ip command)"
    fi
}

# Check permissions
check_permissions() {
    print_info "Checking permissions..."

    if [ "$EUID" -eq 0 ]; then
        print_success "Running as root - full network access available"
    else
        print_info "Not running as root - some features may require sudo"
        print_info "For full functionality, consider running: sudo ./scripts/setup_environment.sh"
    fi
}

# Create desktop shortcut (Linux only)
create_desktop_shortcut() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Creating desktop shortcut..."

        CURRENT_DIR=$(pwd)
        DESKTOP_FILE="$HOME/Desktop/EthicalWiFiMonitor.desktop"

        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Educational WiFi Monitor
Comment=Ethical WiFi Network Scanner for Learning
Exec=gnome-terminal -- bash -c "cd $CURRENT_DIR && source venv/bin/activate && python3 main.py --interactive; read -p 'Press Enter to close...'"
Icon=network-wireless
Terminal=false
Categories=Network;Security;Education;
EOF

        chmod +x "$DESKTOP_FILE"
        print_success "Desktop shortcut created"
    fi
}

# Set up shell aliases
setup_aliases() {
    print_info "Setting up convenient aliases..."

    ALIAS_FILE="$HOME/.ethical_wifi_aliases"

    cat > "$ALIAS_FILE" << 'EOF'
# Educational WiFi Monitor Aliases
alias ewm-scan='cd $(pwd) && source venv/bin/activate && python3 main.py --scan'
alias ewm-interactive='cd $(pwd) && source venv/bin/activate && python3 main.py --interactive'
alias ewm-help='cd $(pwd) && source venv/bin/activate && python3 main.py --help'
alias ewm-activate='cd $(pwd) && source venv/bin/activate'
EOF

    # Add to bashrc if not already present
    if ! grep -q "source.*ethical_wifi_aliases" ~/.bashrc 2>/dev/null; then
        echo "source $ALIAS_FILE" >> ~/.bashrc
        print_success "Aliases added to ~/.bashrc"
    fi

    print_info "Available aliases:"
    echo "  ewm-scan        - Run network scan"
    echo "  ewm-interactive - Run interactive mode"
    echo "  ewm-help        - Show help"
    echo "  ewm-activate    - Activate environment"
}

# Display system information
show_system_info() {
    print_info "System Information:"
    echo "  OS: $(uname -s)"
    echo "  Architecture: $(uname -m)"
    echo "  Python: $(python3 --version 2>/dev/null || echo 'Not found')"
    echo "  Working Directory: $(pwd)"

    if command -v iwconfig &> /dev/null; then
        echo "  Wireless Tools: Available"
    else
        echo "  Wireless Tools: Not available"
    fi
}

# Main setup process
main() {
    echo "🔧 Setting up educational WiFi monitor environment..."
    echo

    check_venv
    activate_venv
    check_wireless_interface
    check_permissions
    create_desktop_shortcut
    setup_aliases
    show_system_info

    echo
    print_success "Environment setup completed!"
    echo
    echo "📋 Usage:"
    echo "1. Run: source venv/bin/activate"
    echo "2. Then: python3 main.py --interactive"
    echo "3. Or use aliases after restarting terminal"
    echo
    echo "⚠️  Remember: Only use on authorized networks!"
}

main "$@"
