#!/usr/bin/env python3
"""
Educational Dashboard Module
Interactive learning interface for network security concepts.
"""

import time
import os
from datetime import datetime
import json

class EducationalDashboard:
    def __init__(self):
        self.learning_progress = {}

    def show_educational_info(self):
        """Display educational information about WiFi scanning"""
        print("\n" + "="*60)
        print("              EDUCATIONAL INFORMATION")
        print("="*60)

        print("""
📚 WHAT YOU'RE LEARNING:

🔍 Network Discovery:
   • How devices find and connect to WiFi networks
   • Understanding beacon frames and network advertisements
   • Learning about SSIDs, BSSIDs, and network identifiers

🛡️  Security Analysis:
   • Different WiFi security protocols (WEP, WPA, WPA2, WPA3)
   • How encryption protects network traffic
   • Common security vulnerabilities and misconfigurations

📊 Network Monitoring:
   • How to analyze network traffic patterns
   • Understanding signal strength and coverage
   • Identifying different types of network devices

⚖️  Ethical Considerations:
   • Legal requirements for network testing
   • Responsible disclosure practices
   • Professional ethics in cybersecurity
""")

    def display_networks(self, networks):
        """Display discovered networks with educational context"""
        print("\n" + "="*80)
        print("                    EDUCATIONAL NETWORK ANALYSIS")
        print("="*80)

        if not networks:
            print("\n❌ No networks discovered.")
            print("💡 Educational Tip: Try moving to a different location or checking your interface.")
            return

        print(f"\n📊 DISCOVERED NETWORKS: {len(networks)} found")
        print("\n📋 Network Details:")
        print("-" * 80)

        for i, network in enumerate(networks, 1):
            ssid = network.get('ssid', 'Unknown')
            bssid = network.get('bssid', 'Unknown')
            encryption = network.get('encryption', 'Unknown')
            signal = network.get('signal', 'Unknown')

            # Color coding for educational purposes
            security_indicator = self._get_security_indicator(encryption)

            print(f"{i:2d}. SSID: {ssid}")
            print(f"    BSSID: {bssid}")
            print(f"    Security: {encryption} {security_indicator}")
            print(f"    Signal: {signal}")

            # Educational commentary
            self._provide_network_education(network)
            print("-" * 80)

    def _get_security_indicator(self, encryption):
        """Get security level indicator"""
        encryption_upper = encryption.upper()

        if any(sec in encryption_upper for sec in ['WPA3']):
            return "🟢 (Most Secure)"
        elif any(sec in encryption_upper for sec in ['WPA2']):
            return "🟡 (Good Security)"
        elif 'WPA' in encryption_upper:
            return "🟠 (Basic Security)"
        elif 'WEP' in encryption_upper:
            return "🔴 (Weak - Avoid)"
        elif 'OPEN' in encryption_upper or encryption == 'None':
            return "⚪ (No Security)"
        else:
            return "❓ (Unknown)"

    def _provide_network_education(self, network):
        """Provide educational context for each network"""
        encryption = network.get('encryption', 'Unknown').upper()

        if 'WPA3' in encryption:
            print("    📚 Learning: WPA3 is the latest WiFi security standard with enhanced protection")
        elif 'WPA2' in encryption:
            print("    📚 Learning: WPA2 provides strong security when properly configured")
        elif 'WEP' in encryption:
            print("    📚 Learning: WEP is outdated and easily cracked - avoid for security")
        elif 'OPEN' in encryption:
            print("    📚 Learning: Open networks have no encryption - traffic is visible")

        # Signal strength education
        signal_str = network.get('signal', '')
        if 'dBm' in signal_str:
            try:
                signal_value = int(''.join(filter(str.lstrip('-').isdigit(), signal_str)))
                if signal_value > -50:
                    print("    📶 Signal: Excellent (very close to access point)")
                elif signal_value > -70:
                    print("    📶 Signal: Good (reasonable connection quality)")
                elif signal_value > -85:
                    print("    📶 Signal: Fair (may experience slow speeds)")
                else:
                    print("    📶 Signal: Poor (connection issues likely)")
            except:
                pass

    def explain_wifi_security(self):
        """Explain WiFi security concepts"""
        print("\n" + "="*60)
        print("           WIFI SECURITY FUNDAMENTALS")
        print("="*60)

        print("""
🔒 WIFI SECURITY EVOLUTION:

1️⃣  WEP (Wired Equivalent Privacy) - DEPRECATED
   • Introduced: 1999
   • Key Length: 64-bit or 128-bit
   • Status: ❌ BROKEN - Can be cracked in minutes
   • Educational Note: Important historical lesson in cryptographic failures

2️⃣  WPA (WiFi Protected Access) - LEGACY
   • Introduced: 2003
   • Improvements: TKIP encryption, better key management
   • Status: 🟠 Weak - Vulnerable to attacks
   • Educational Note: Temporary solution while WPA2 was developed

3️⃣  WPA2 (WiFi Protected Access 2) - CURRENT STANDARD
   • Introduced: 2004
   • Features: AES encryption, strong authentication
   • Status: 🟡 Good when properly configured
   • Educational Note: Most widely deployed security standard

4️⃣  WPA3 (WiFi Protected Access 3) - LATEST
   • Introduced: 2018
   • Features: Enhanced encryption, protection against brute force
   • Status: 🟢 Most Secure
   • Educational Note: Addresses known WPA2 vulnerabilities

🛡️  KEY SECURITY CONCEPTS:

• Authentication: Verifying device identity
• Encryption: Protecting data in transit  
• Key Management: Secure distribution of encryption keys
• Forward Secrecy: Past sessions remain secure if keys compromised
""")

        input("\nPress Enter to continue...")

    def explain_network_scanning(self):
        """Explain network scanning concepts"""
        print("\n" + "="*60)
        print("          NETWORK SCANNING FUNDAMENTALS")
        print("="*60)

        print("""
🔍 HOW NETWORK SCANNING WORKS:

1️⃣  Passive Scanning:
   • Listens for beacon frames broadcast by access points
   • Doesn't transmit - purely observational
   • Lower detection risk
   • Slower discovery process

2️⃣  Active Scanning:  
   • Sends probe requests to discover networks
   • Faster discovery
   • May be logged by access points
   • Higher detection probability

📡 INFORMATION GATHERED:

• SSID (Network Name): Human-readable identifier
• BSSID (MAC Address): Unique hardware identifier  
• Channel: Radio frequency used
• Signal Strength: Distance/quality indicator
• Encryption Type: Security protocol in use
• Vendor Information: Device manufacturer

🎯 LEGITIMATE USE CASES:

• Network troubleshooting and optimization
• Security assessments (authorized)
• Site surveys for network deployment
• Interference analysis
• Educational learning and research

⚖️  LEGAL CONSIDERATIONS:

• Passive scanning is generally legal
• Active scanning may require permission
• Accessing networks requires authorization
• Laws vary by jurisdiction
""")

        input("\nPress Enter to continue...")

    def explain_security_analysis(self):
        """Explain security analysis concepts"""
        print("\n" + "="*60)
        print("            SECURITY ANALYSIS CONCEPTS")
        print("="*60)

        print("""
🔒 SECURITY ASSESSMENT METHODOLOGY:

1️⃣  Information Gathering:
   • Identify target networks and devices
   • Catalog security configurations
   • Map network topology
   • Document potential entry points

2️⃣  Vulnerability Identification:
   • Weak encryption protocols (WEP)
   • Default credentials
   • Outdated firmware
   • Misconfigured settings

3️⃣  Risk Assessment:
   • Evaluate impact of vulnerabilities
   • Consider attack probability  
   • Assess business/personal risk
   • Prioritize remediation efforts

4️⃣  Reporting & Remediation:
   • Document findings clearly
   • Provide actionable recommendations
   • Assist with security improvements
   • Verify fixes are effective

🚨 COMMON VULNERABILITIES:

• Weak Passwords: Easy to guess or crack
• Open Networks: No encryption protection
• WPS Enabled: Vulnerable to brute force
• Default Settings: Unchanged from factory
• Outdated Firmware: Missing security patches

🛡️  DEFENSIVE MEASURES:

• Use WPA3 or WPA2 with strong passwords
• Disable WPS if not needed
• Change default administrator credentials  
• Keep firmware updated
• Monitor for unauthorized access
• Implement network segmentation
""")

        input("\nPress Enter to continue...")

    def explain_defensive_measures(self):
        """Explain defensive cybersecurity measures"""
        print("\n" + "="*60)
        print("           DEFENSIVE CYBERSECURITY MEASURES")
        print("="*60)

        print("""
🛡️  NETWORK DEFENSE STRATEGIES:

1️⃣  Perimeter Security:
   • Strong WiFi encryption (WPA3/WPA2)
   • Complex passwords/passphrases
   • MAC address filtering (where appropriate)
   • Network access control (NAC)

2️⃣  Network Segmentation:
   • Separate guest and internal networks
   • Isolate IoT devices
   • Use VLANs for different device types
   • Implement micro-segmentation

3️⃣  Monitoring & Detection:
   • Intrusion Detection Systems (IDS)
   • Security Information Event Management (SIEM)
   • Network behavior analysis
   • Automated threat detection

4️⃣  Incident Response:
   • Preparation and planning
   • Detection and analysis
   • Containment and eradication
   • Recovery and lessons learned

🔍 CONTINUOUS IMPROVEMENT:

• Regular security assessments
• Penetration testing (authorized)
• Security awareness training
• Threat intelligence integration
• Security policy updates

💡 BEST PRACTICES:

• Defense in depth approach
• Principle of least privilege
• Regular security updates
• Employee security training
• Incident response planning
• Business continuity planning

🎓 CAREER PATHS:

• Security Analyst
• Penetration Tester
• Security Engineer
• Incident Response Specialist
• Security Architect
• Chief Information Security Officer (CISO)
""")

        input("\nPress Enter to continue...")

    def generate_learning_report(self, scan_data):
        """Generate educational learning report"""
        print("\n" + "="*60)
        print("              LEARNING REPORT")
        print("="*60)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_networks = len(scan_data)

        # Analyze security distribution
        security_analysis = self._analyze_security_distribution(scan_data)

        print(f"\n📊 Scan Summary ({timestamp}):")
        print(f"   • Total Networks Discovered: {total_networks}")
        print(f"   • Scan Duration: Educational demonstration")
        print(f"   • Learning Objectives: Network security awareness")

        print(f"\n🔒 Security Analysis:")
        for security_type, count in security_analysis.items():
            percentage = (count / total_networks * 100) if total_networks > 0 else 0
            print(f"   • {security_type}: {count} networks ({percentage:.1f}%)")

        print(f"\n📚 Key Learning Points:")
        self._generate_learning_points(security_analysis, total_networks)

        print(f"\n✅ Educational Objectives Achieved:")
        print("   ✓ Understanding of WiFi security protocols")
        print("   ✓ Network discovery methodology")
        print("   ✓ Security assessment techniques")
        print("   ✓ Ethical hacking principles")

        return {
            "timestamp": timestamp,
            "total_networks": total_networks,
            "security_analysis": security_analysis
        }

    def _analyze_security_distribution(self, networks):
        """Analyze distribution of security types"""
        security_count = {
            "WPA3 (Most Secure)": 0,
            "WPA2 (Good Security)": 0, 
            "WPA (Basic Security)": 0,
            "WEP (Weak Security)": 0,
            "Open (No Security)": 0,
            "Unknown": 0
        }

        for network in networks:
            encryption = network.get('encryption', 'Unknown').upper()

            if 'WPA3' in encryption:
                security_count["WPA3 (Most Secure)"] += 1
            elif 'WPA2' in encryption:
                security_count["WPA2 (Good Security)"] += 1
            elif 'WPA' in encryption:
                security_count["WPA (Basic Security)"] += 1
            elif 'WEP' in encryption:
                security_count["WEP (Weak Security)"] += 1
            elif any(term in encryption for term in ['OPEN', 'NONE']):
                security_count["Open (No Security)"] += 1
            else:
                security_count["Unknown"] += 1

        return security_count

    def _generate_learning_points(self, security_analysis, total_networks):
        """Generate educational learning points"""
        if security_analysis.get("WEP (Weak Security)", 0) > 0:
            print("   • WEP networks detected - demonstrate vulnerability to attacks")

        if security_analysis.get("Open (No Security)", 0) > 0:
            print("   • Open networks found - highlight privacy and security risks")

        if security_analysis.get("WPA3 (Most Secure)", 0) > 0:
            print("   • WPA3 networks show adoption of latest security standards")

        secure_percentage = (security_analysis.get("WPA2 (Good Security)", 0) + 
                           security_analysis.get("WPA3 (Most Secure)", 0)) / total_networks * 100

        if secure_percentage > 75:
            print("   • High adoption of secure protocols in this area")
        elif secure_percentage < 50:
            print("   • Opportunity for security awareness and education")

        print("   • Network diversity provides comprehensive learning opportunity")
