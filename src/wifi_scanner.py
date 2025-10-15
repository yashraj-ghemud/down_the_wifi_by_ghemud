#!/usr/bin/env python3
"""
WiFi Scanner Module
Educational WiFi network scanning with ethical considerations.
"""

import subprocess
import re
import time
import json
from datetime import datetime
import platform

class WiFiScanner:
    def __init__(self):
        self.interface = None
        self.networks = []
        self.scan_results = {}

    def check_dependencies(self):
        """Check if required tools are installed"""
        required_tools = []

        # Check OS-specific tools
        if platform.system() == "Linux":
            required_tools = ["iwlist", "iwconfig", "ip"]
        elif platform.system() == "Darwin":  # macOS
            required_tools = ["airport"]
        elif platform.system() == "Windows":
            required_tools = ["netsh"]

        missing_tools = []
        for tool in required_tools:
            if not self._command_exists(tool):
                missing_tools.append(tool)

        if missing_tools:
            print(f"❌ Missing required tools: {', '.join(missing_tools)}")
            return False
        return True

    def _command_exists(self, command):
        """Check if a command exists in the system"""
        try:
            subprocess.run([command], stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, timeout=5)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            return False

    def get_available_interfaces(self):
        """Get available wireless interfaces"""
        interfaces = []

        try:
            if platform.system() == "Linux":
                # Use iwconfig to find wireless interfaces
                result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=10)
                for line in result.stdout.split('\n'):
                    if 'IEEE 802.11' in line:
                        interface = line.split()[0]
                        interfaces.append(interface)

            elif platform.system() == "Darwin":  # macOS
                # Use networksetup to find wifi interfaces
                result = subprocess.run(['networksetup', '-listallhardwareports'], 
                                      capture_output=True, text=True, timeout=10)
                lines = result.stdout.split('\n')
                for i, line in enumerate(lines):
                    if 'Wi-Fi' in line and i+1 < len(lines):
                        device_line = lines[i+1]
                        if 'Device:' in device_line:
                            interface = device_line.split('Device: ')[1].strip()
                            interfaces.append(interface)

            elif platform.system() == "Windows":
                # Use netsh to find wireless interfaces
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                      capture_output=True, text=True, timeout=10)
                for line in result.stdout.split('\n'):
                    if 'Name' in line and 'Wi-Fi' in line:
                        interface = line.split(':')[1].strip()
                        interfaces.append(interface)

        except Exception as e:
            print(f"⚠️  Error finding interfaces: {e}")

        return interfaces

    def scan_networks(self, interface=None, timeout=30):
        """Perform educational network scan"""
        print("\n🔍 Starting educational WiFi network scan...")

        if not self.check_dependencies():
            print("❌ Required dependencies not found. Please install networking tools.")
            return []

        # Auto-detect interface if not provided
        if not interface:
            interfaces = self.get_available_interfaces()
            if interfaces:
                interface = interfaces[0]
                print(f"📡 Using interface: {interface}")
            else:
                print("❌ No wireless interfaces found.")
                return []

        networks = []

        try:
            if platform.system() == "Linux":
                networks = self._scan_linux(interface, timeout)
            elif platform.system() == "Darwin":
                networks = self._scan_macos(interface, timeout)
            elif platform.system() == "Windows":
                networks = self._scan_windows(timeout)
            else:
                print(f"❌ Unsupported operating system: {platform.system()}")
                return []

        except Exception as e:
            print(f"❌ Scan error: {e}")
            return []

        print(f"\n✅ Scan completed. Found {len(networks)} networks.")
        return networks

    def _scan_linux(self, interface, timeout):
        """Scan networks on Linux"""
        networks = []

        try:
            # Use iwlist to scan for networks
            print(f"📡 Scanning with iwlist on {interface}...")
            result = subprocess.run(['iwlist', interface, 'scan'], 
                                  capture_output=True, text=True, timeout=timeout)

            if result.returncode != 0:
                print(f"⚠️  iwlist scan failed: {result.stderr}")
                return networks

            # Parse iwlist output
            networks = self._parse_iwlist_output(result.stdout)

        except subprocess.TimeoutExpired:
            print("⚠️  Scan timeout. Try increasing timeout value.")
        except Exception as e:
            print(f"⚠️  Linux scan error: {e}")

        return networks

    def _scan_macos(self, interface, timeout):
        """Scan networks on macOS"""
        networks = []

        try:
            # Use airport utility for scanning
            airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

            if not os.path.exists(airport_path):
                print("⚠️  airport utility not found. Using system_profiler instead.")
                return self._scan_macos_fallback()

            result = subprocess.run([airport_path, '-s'], 
                                  capture_output=True, text=True, timeout=timeout)

            networks = self._parse_airport_output(result.stdout)

        except Exception as e:
            print(f"⚠️  macOS scan error: {e}")

        return networks

    def _scan_windows(self, timeout):
        """Scan networks on Windows"""
        networks = []

        try:
            # Use netsh to scan for networks
            result = subprocess.run(['netsh', 'wlan', 'show', 'network'], 
                                  capture_output=True, text=True, timeout=timeout)

            networks = self._parse_netsh_output(result.stdout)

        except Exception as e:
            print(f"⚠️  Windows scan error: {e}")

        return networks

    def _parse_iwlist_output(self, output):
        """Parse iwlist scan output"""
        networks = []
        current_network = {}

        for line in output.split('\n'):
            line = line.strip()

            if 'Cell' in line and 'Address:' in line:
                if current_network:
                    networks.append(current_network)
                current_network = {'bssid': line.split('Address: ')[1]}

            elif 'ESSID:' in line:
                essid = line.split('ESSID:')[1].strip('"')
                current_network['ssid'] = essid if essid else '[Hidden]'

            elif 'Quality=' in line:
                quality_match = re.search(r'Quality=([\d/]+)', line)
                signal_match = re.search(r'Signal level=(-?\d+)', line)
                if quality_match:
                    current_network['quality'] = quality_match.group(1)
                if signal_match:
                    current_network['signal'] = f"{signal_match.group(1)} dBm"

            elif 'Encryption key:' in line:
                current_network['encryption'] = 'WEP' if 'on' in line else 'Open'

            elif 'IEEE 802.11' in line:
                protocol_match = re.search(r'IEEE 802.11([a-z]+)', line)
                if protocol_match:
                    current_network['protocol'] = f"802.11{protocol_match.group(1)}"

        if current_network:
            networks.append(current_network)

        return networks

    def _parse_airport_output(self, output):
        """Parse airport scan output (macOS)"""
        networks = []
        lines = output.split('\n')[1:]  # Skip header

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    network = {
                        'ssid': parts[0] if parts[0] != '[Hidden]' else '[Hidden]',
                        'bssid': parts[1],
                        'rssi': f"{parts[2]} dBm",
                        'channel': parts[3],
                        'encryption': parts[6] if len(parts) > 6 else 'Unknown'
                    }
                    networks.append(network)

        return networks

    def _parse_netsh_output(self, output):
        """Parse netsh scan output (Windows)"""
        networks = []
        current_network = {}

        for line in output.split('\n'):
            line = line.strip()

            if line.startswith('SSID'):
                if current_network:
                    networks.append(current_network)
                ssid = line.split(':', 1)[1].strip()
                current_network = {'ssid': ssid if ssid else '[Hidden]'}

            elif 'Authentication' in line:
                auth = line.split(':', 1)[1].strip()
                current_network['encryption'] = auth

            elif 'Signal' in line:
                signal = line.split(':', 1)[1].strip()
                current_network['signal'] = signal

        if current_network:
            networks.append(current_network)

        return networks

    def save_scan_results(self, networks, filename=None):
        """Save scan results to file for educational analysis"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_results_{timestamp}.json"

        # Create results directory
        os.makedirs("results", exist_ok=True)
        filepath = os.path.join("results", filename)

        scan_data = {
            "timestamp": datetime.now().isoformat(),
            "scan_type": "educational_wifi_scan",
            "total_networks": len(networks),
            "networks": networks
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(scan_data, f, indent=2)
            print(f"📁 Scan results saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return None
