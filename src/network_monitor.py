#!/usr/bin/env python3
"""
Network Monitor Module
Educational network monitoring and traffic analysis.
"""

import subprocess
import time
import json
import threading
from datetime import datetime
import platform
import re

class NetworkMonitor:
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.traffic_stats = {}

    def monitor_network_activity(self, duration=60, interface=None):
        """Monitor network activity for educational purposes"""
        print(f"\n📊 Starting network monitoring for {duration} seconds...")
        print("📚 Educational Purpose: Understanding network traffic patterns")

        if platform.system() == "Linux":
            self._monitor_linux(duration, interface)
        elif platform.system() == "Darwin":
            self._monitor_macos(duration, interface)  
        elif platform.system() == "Windows":
            self._monitor_windows(duration)
        else:
            print(f"❌ Network monitoring not supported on {platform.system()}")
            return False

        return True

    def _monitor_linux(self, duration, interface):
        """Monitor network on Linux using various tools"""
        try:
            # Get network statistics
            self._get_interface_stats_linux(interface)

            # Monitor for specified duration
            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(5)
                current_stats = self._get_interface_stats_linux(interface)
                self._display_traffic_update(current_stats)

        except Exception as e:
            print(f"❌ Linux monitoring error: {e}")

    def _monitor_macos(self, duration, interface):
        """Monitor network on macOS"""
        try:
            # Use netstat and other macOS tools
            self._get_interface_stats_macos(interface)

            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(5)
                current_stats = self._get_interface_stats_macos(interface)
                self._display_traffic_update(current_stats)

        except Exception as e:
            print(f"❌ macOS monitoring error: {e}")

    def _monitor_windows(self, duration):
        """Monitor network on Windows"""
        try:
            # Use Windows networking commands
            start_time = time.time()
            while time.time() - start_time < duration:
                stats = self._get_interface_stats_windows()
                self._display_traffic_update(stats)
                time.sleep(5)

        except Exception as e:
            print(f"❌ Windows monitoring error: {e}")

    def _get_interface_stats_linux(self, interface):
        """Get interface statistics on Linux"""
        stats = {}

        try:
            # Read from /proc/net/dev
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()

            for line in lines:
                if ':' in line:
                    parts = line.split(':')
                    iface = parts[0].strip()

                    if not interface or iface == interface:
                        data = parts[1].split()
                        stats[iface] = {
                            'rx_bytes': int(data[0]),
                            'rx_packets': int(data[1]),
                            'tx_bytes': int(data[8]),
                            'tx_packets': int(data[9])
                        }

        except Exception as e:
            print(f"⚠️  Error reading interface stats: {e}")

        return stats

    def _get_interface_stats_macos(self, interface):
        """Get interface statistics on macOS"""
        stats = {}

        try:
            result = subprocess.run(['netstat', '-ibn'], 
                                  capture_output=True, text=True, timeout=10)

            for line in result.stdout.split('\n'):
                parts = line.split()
                if len(parts) >= 10 and (not interface or parts[0] == interface):
                    iface = parts[0]
                    if iface.startswith(('en', 'wi')):  # Network interfaces
                        stats[iface] = {
                            'rx_bytes': int(parts[6]) if parts[6].isdigit() else 0,
                            'rx_packets': int(parts[4]) if parts[4].isdigit() else 0,
                            'tx_bytes': int(parts[9]) if parts[9].isdigit() else 0,
                            'tx_packets': int(parts[7]) if parts[7].isdigit() else 0
                        }

        except Exception as e:
            print(f"⚠️  Error reading macOS interface stats: {e}")

        return stats

    def _get_interface_stats_windows(self):
        """Get interface statistics on Windows"""
        stats = {}

        try:
            result = subprocess.run(['netstat', '-e'], 
                                  capture_output=True, text=True, timeout=10)

            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if 'Bytes' in line and i+1 < len(lines):
                    data = lines[i+1].split()
                    if len(data) >= 2:
                        stats['total'] = {
                            'rx_bytes': int(data[0]) if data[0].isdigit() else 0,
                            'tx_bytes': int(data[1]) if data[1].isdigit() else 0
                        }
                        break

        except Exception as e:
            print(f"⚠️  Error reading Windows interface stats: {e}")

        return stats

    def _display_traffic_update(self, current_stats):
        """Display traffic statistics update"""
        print(f"\n📈 Network Traffic Update - {datetime.now().strftime('%H:%M:%S')}")

        for interface, stats in current_stats.items():
            rx_mb = stats.get('rx_bytes', 0) / (1024 * 1024)
            tx_mb = stats.get('tx_bytes', 0) / (1024 * 1024)

            print(f"   {interface}:")
            print(f"     📥 Received: {rx_mb:.2f} MB ({stats.get('rx_packets', 0)} packets)")
            print(f"     📤 Transmitted: {tx_mb:.2f} MB ({stats.get('tx_packets', 0)} packets)")

    def analyze_network_devices(self, networks):
        """Analyze detected network devices for educational purposes"""
        print("\n🔍 EDUCATIONAL NETWORK DEVICE ANALYSIS")
        print("="*50)

        device_types = self._categorize_devices(networks)
        security_levels = self._analyze_security_levels(networks)

        print(f"\n📊 Device Categories Found:")
        for category, count in device_types.items():
            print(f"   {category}: {count} devices")

        print(f"\n🔒 Security Analysis:")
        for level, networks_list in security_levels.items():
            print(f"   {level}: {len(networks_list)} networks")

        return {
            'device_types': device_types,
            'security_levels': security_levels
        }

    def _categorize_devices(self, networks):
        """Categorize devices based on network characteristics"""
        categories = {
            'Home Routers': 0,
            'Enterprise APs': 0,
            'Mobile Hotspots': 0,
            'IoT Devices': 0,
            'Unknown': 0
        }

        for network in networks:
            ssid = network.get('ssid', '').lower()

            # Simple heuristic categorization for educational purposes
            if any(term in ssid for term in ['home', 'wifi', 'router', 'netgear', 'linksys']):
                categories['Home Routers'] += 1
            elif any(term in ssid for term in ['corp', 'office', 'enterprise', 'company']):
                categories['Enterprise APs'] += 1
            elif any(term in ssid for term in ['mobile', 'hotspot', 'phone', 'android', 'iphone']):
                categories['Mobile Hotspots'] += 1
            elif any(term in ssid for term in ['cam', 'printer', 'tv', 'smart']):
                categories['IoT Devices'] += 1
            else:
                categories['Unknown'] += 1

        return categories

    def _analyze_security_levels(self, networks):
        """Analyze security levels of detected networks"""
        security_levels = {
            'Secure (WPA2/WPA3)': [],
            'Weak Security (WEP)': [],
            'Open Networks': [],
            'Unknown Security': []
        }

        for network in networks:
            encryption = network.get('encryption', 'Unknown').upper()

            if any(sec in encryption for sec in ['WPA2', 'WPA3']):
                security_levels['Secure (WPA2/WPA3)'].append(network)
            elif 'WEP' in encryption:
                security_levels['Weak Security (WEP)'].append(network)
            elif 'OPEN' in encryption or encryption == 'NONE':
                security_levels['Open Networks'].append(network)
            else:
                security_levels['Unknown Security'].append(network)

        return security_levels

    def detect_suspicious_activity(self, networks):
        """Educational demonstration of suspicious network activity detection"""
        print("\n🚨 EDUCATIONAL: Suspicious Activity Detection")
        print("="*50)

        suspicious_indicators = []

        # Check for hidden networks
        hidden_networks = [n for n in networks if n.get('ssid') in ['', '[Hidden]']]
        if hidden_networks:
            suspicious_indicators.append(f"Found {len(hidden_networks)} hidden networks")

        # Check for duplicate SSIDs (possible rogue APs)
        ssid_count = {}
        for network in networks:
            ssid = network.get('ssid', '')
            if ssid and ssid != '[Hidden]':
                ssid_count[ssid] = ssid_count.get(ssid, 0) + 1

        duplicates = {ssid: count for ssid, count in ssid_count.items() if count > 1}
        if duplicates:
            suspicious_indicators.append(f"Duplicate SSIDs detected: {list(duplicates.keys())}")

        # Check for weak security
        weak_networks = [n for n in networks if 'WEP' in n.get('encryption', '').upper()]
        if weak_networks:
            suspicious_indicators.append(f"Found {len(weak_networks)} networks using weak WEP encryption")

        if suspicious_indicators:
            print("⚠️  Educational Alert - Potential Issues Detected:")
            for indicator in suspicious_indicators:
                print(f"   • {indicator}")

            print("\n📚 Educational Note:")
            print("   These indicators don't necessarily mean malicious activity,")
            print("   but they represent patterns that security professionals monitor.")
        else:
            print("✅ No obvious suspicious patterns detected in this educational scan.")

        return suspicious_indicators
