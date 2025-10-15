#!/usr/bin/env python3
"""
Educational WiFi Network Monitor
A tool for learning about network security and WiFi technologies in an ethical manner.

IMPORTANT LEGAL NOTICE:
This tool is for educational purposes only. Only use on networks you own or have 
explicit written permission to test. Unauthorized network scanning may be illegal 
in your jurisdiction.

Author: Educational Project
License: MIT (Educational Use Only)
"""

import argparse
import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ethical_framework import EthicalFramework
from wifi_scanner import WiFiScanner
from network_monitor import NetworkMonitor
from educational_dashboard import EducationalDashboard
from security_analyzer import SecurityAnalyzer

class EthicalWiFiMonitor:
    def __init__(self, config_path="config/settings.json"):
        """Initialize the Educational WiFi Monitor"""
        self.config = self._load_config(config_path)
        self.ethics = EthicalFramework()
        self.scanner = WiFiScanner()
        self.monitor = NetworkMonitor()
        self.dashboard = EducationalDashboard()
        self.analyzer = SecurityAnalyzer()

    def _load_config(self, path):
        """Load configuration settings"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {path} not found. Using defaults.")
            return self._default_config()

    def _default_config(self):
        """Return default configuration"""
        return {
            "educational_mode": True,
            "scan_timeout": 30,
            "display_warnings": True,
            "log_activities": True,
            "interface": "wlan0"
        }

    def run_educational_scan(self):
        """Run educational WiFi scanning with proper warnings"""
        print("\n" + "="*60)
        print("    EDUCATIONAL WIFI NETWORK MONITOR")
        print("="*60)

        # Check ethical compliance
        if not self.ethics.verify_ethical_usage():
            print("\n❌ Ethical verification failed. Exiting.")
            return False

        print("\n✅ Ethical verification passed. Starting educational scan...")

        # Display educational information
        self.dashboard.show_educational_info()

        # Perform network scan
        networks = self.scanner.scan_networks()

        if networks:
            # Display results educationally
            self.dashboard.display_networks(networks)

            # Analyze security (educational)
            self.analyzer.analyze_network_security(networks)

            # Monitor network behavior (educational)
            self.monitor.monitor_network_activity()

        return True

    def run_interactive_mode(self):
        """Run in interactive learning mode"""
        print("\n🎓 Interactive Learning Mode")
        print("This mode will guide you through network security concepts.")

        while True:
            print("\nSelect learning module:")
            print("1. WiFi Security Basics")
            print("2. Network Scanning Concepts")
            print("3. Security Analysis")
            print("4. Defensive Measures")
            print("5. Exit")

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                self.dashboard.explain_wifi_security()
            elif choice == "2":
                self.dashboard.explain_network_scanning()
            elif choice == "3":
                self.dashboard.explain_security_analysis()
            elif choice == "4":
                self.dashboard.explain_defensive_measures()
            elif choice == "5":
                print("\n👋 Thank you for learning responsibly!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Educational WiFi Network Monitor for Learning Cybersecurity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py --scan          # Run educational network scan
  python3 main.py --interactive   # Run in interactive learning mode
  python3 main.py --help          # Show this help message

LEGAL WARNING: Only use on networks you own or have explicit permission to test.
"""
    )

    parser.add_argument('--scan', action='store_true', 
                       help='Run educational network scan')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive learning mode')
    parser.add_argument('--config', type=str, default='config/settings.json',
                       help='Path to configuration file')

    args = parser.parse_args()

    # Check if running as root (required for some operations)
    if os.geteuid() != 0 and (args.scan):
        print("⚠️  Root privileges required for network scanning.")
        print("Please run with: sudo python3 main.py --scan")
        sys.exit(1)

    # Initialize monitor
    monitor = EthicalWiFiMonitor(args.config)

    # Run based on arguments
    if args.scan:
        monitor.run_educational_scan()
    elif args.interactive:
        monitor.run_interactive_mode()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
