#!/bin/bash
# Educational WiFi Monitor - Quick Start Script

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "       Educational WiFi Monitor - Quick Start"
    echo "=================================================="
    echo -e "${NC}"
}

print_legal_warning() {
    echo -e "${RED}"
    echo "⚖️  LEGAL WARNING:"
    echo "   Only use on networks you own or have explicit"
    echo "   written permission to test. Unauthorized network"
    echo "   scanning may be illegal in your jurisdiction."
    echo -e "${NC}"
    echo
}

print_menu() {
    echo "Select an option:"
    echo "1. 🎓 Interactive Learning Mode (Recommended for beginners)"
    echo "2. 🔍 Network Scan (Requires authorization)"
    echo "3. 📚 View Documentation"
    echo "4. ⚖️  Legal Disclaimer"
    echo "5. ❌ Exit"
    echo
}

check_environment() {
    if [ ! -d "venv" ]; then
        echo -e "${RED}❌ Virtual environment not found.${NC}"
        echo "Please run: ./scripts/install_dependencies.sh"
        exit 1
    fi

    if [ ! -f "main.py" ]; then
        echo -e "${RED}❌ Main application not found.${NC}"
        echo "Please ensure you're in the project directory."
        exit 1
    fi
}

activate_environment() {
    echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
    source venv/bin/activate
}

run_interactive() {
    echo -e "${GREEN}🎓 Starting Interactive Learning Mode...${NC}"
    python3 main.py --interactive
}

run_scan() {
    echo -e "${YELLOW}⚠️  Network Scan Mode${NC}"
    echo "This will perform an authorized network scan."
    read -p "Do you have permission to scan this network? (yes/no): " permission

    if [ "$permission" = "yes" ]; then
        echo -e "${GREEN}🔍 Starting authorized network scan...${NC}"
        python3 main.py --scan
    else
        echo -e "${RED}❌ Cannot proceed without proper authorization.${NC}"
    fi
}

view_docs() {
    echo -e "${BLUE}📚 Available Documentation:${NC}"
    echo

    if [ -f "docs/README.md" ]; then
        echo "1. README.md - Main documentation"
        echo "2. ETHICS_GUIDE.md - Ethical guidelines"
        echo "3. USAGE_GUIDE.md - Usage instructions"
        echo
        read -p "Which document would you like to view? (1-3): " doc_choice

        case $doc_choice in
            1) less docs/README.md ;;
            2) less docs/ETHICS_GUIDE.md ;;
            3) less docs/USAGE_GUIDE.md ;;
            *) echo "Invalid choice" ;;
        esac
    else
        echo "❌ Documentation files not found."
    fi
}

view_legal() {
    echo -e "${YELLOW}⚖️  Legal Disclaimer:${NC}"
    if [ -f "config/legal_disclaimer.txt" ]; then
        less config/legal_disclaimer.txt
    else
        echo "❌ Legal disclaimer file not found."
    fi
}

main() {
    print_header
    print_legal_warning

    check_environment
    activate_environment

    while true; do
        print_menu
        read -p "Enter your choice (1-5): " choice
        echo

        case $choice in
            1)
                run_interactive
                ;;
            2)
                run_scan
                ;;
            3)
                view_docs
                ;;
            4)
                view_legal
                ;;
            5)
                echo -e "${GREEN}👋 Thank you for using Educational WiFi Monitor responsibly!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Invalid choice. Please select 1-5.${NC}"
                ;;
        esac

        echo
        read -p "Press Enter to return to main menu..."
        echo
    done
}

main "$@"
