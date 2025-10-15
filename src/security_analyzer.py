#!/usr/bin/env python3
"""
Security Analyzer Module
Educational security analysis and vulnerability assessment.
"""

import re
import json
from datetime import datetime
from collections import Counter

class SecurityAnalyzer:
    def __init__(self):
        self.vulnerability_database = self._load_vulnerability_patterns()
        self.security_recommendations = {}

    def _load_vulnerability_patterns(self):
        """Load patterns for educational vulnerability identification"""
        return {
            'weak_encryption': {
                'patterns': ['WEP', 'OPEN', 'NONE'],
                'severity': 'HIGH',
                'description': 'Network uses weak or no encryption'
            },
            'default_ssids': {
                'patterns': ['linksys', 'netgear', 'dlink', 'tplink', 'belkin', 
                           'asus', 'default', 'admin', 'router'],
                'severity': 'MEDIUM',
                'description': 'Network uses default or common SSID'
            },
            'hidden_networks': {
                'patterns': ['[Hidden]', '', 'hidden'],
                'severity': 'INFO',
                'description': 'Hidden network detected (security through obscurity)'
            },
            'weak_passwords': {
                'patterns': ['password', '123456', 'admin', 'default'],
                'severity': 'HIGH',
                'description': 'Potentially weak password based on SSID'
            }
        }

    def analyze_network_security(self, networks):
        """Perform comprehensive educational security analysis"""
        print("\n" + "="*70)
        print("              EDUCATIONAL SECURITY ANALYSIS")
        print("="*70)

        if not networks:
            print("\n❌ No networks to analyze.")
            return {}

        analysis_results = {
            'total_networks': len(networks),
            'vulnerabilities': [],
            'security_summary': {},
            'recommendations': []
        }

        # Analyze each network
        for network in networks:
            vulnerabilities = self._analyze_single_network(network)
            analysis_results['vulnerabilities'].extend(vulnerabilities)

        # Generate security summary
        analysis_results['security_summary'] = self._generate_security_summary(networks)

        # Generate recommendations
        analysis_results['recommendations'] = self._generate_recommendations(analysis_results)

        # Display results
        self._display_analysis_results(analysis_results)

        return analysis_results

    def _analyze_single_network(self, network):
        """Analyze security of a single network"""
        vulnerabilities = []
        ssid = network.get('ssid', '').lower()
        encryption = network.get('encryption', 'Unknown').upper()

        # Check encryption strength
        if any(weak in encryption for weak in ['WEP', 'OPEN', 'NONE']):
            vulnerabilities.append({
                'network': network.get('ssid', 'Unknown'),
                'bssid': network.get('bssid', 'Unknown'),
                'type': 'Weak Encryption',
                'severity': 'HIGH',
                'description': f'Uses {encryption} which is vulnerable',
                'education': self._get_encryption_education(encryption)
            })

        # Check for default SSIDs
        if any(pattern in ssid for pattern in self.vulnerability_database['default_ssids']['patterns']):
            vulnerabilities.append({
                'network': network.get('ssid', 'Unknown'),
                'bssid': network.get('bssid', 'Unknown'),
                'type': 'Default SSID',
                'severity': 'MEDIUM',
                'description': 'Uses default or common SSID',
                'education': 'Default SSIDs can reveal device type and may indicate default passwords'
            })

        # Check for hidden networks
        if ssid in ['', '[hidden]', 'hidden']:
            vulnerabilities.append({
                'network': '[Hidden Network]',
                'bssid': network.get('bssid', 'Unknown'),
                'type': 'Hidden Network',
                'severity': 'INFO',
                'description': 'Network SSID is hidden',
                'education': 'Hidden SSIDs provide minimal security benefit and can still be discovered'
            })

        return vulnerabilities

    def _get_encryption_education(self, encryption):
        """Get educational information about encryption types"""
        encryption = encryption.upper()

        if 'WEP' in encryption:
            return ("WEP uses RC4 encryption with static keys. It can be cracked in minutes "
                   "using tools like Aircrack-ng. Always upgrade to WPA2 or WPA3.")
        elif 'OPEN' in encryption or 'NONE' in encryption:
            return ("Open networks provide no encryption. All traffic is transmitted in "
                   "plain text and can be intercepted by anyone within range.")
        elif 'WPA3' in encryption:
            return ("WPA3 is the latest standard providing strong security with "
                   "Simultaneous Authentication of Equals (SAE) and enhanced encryption.")
        elif 'WPA2' in encryption:
            return ("WPA2 uses AES encryption and is currently secure when properly "
                   "configured with strong passwords.")
        elif 'WPA' in encryption:
            return ("Original WPA uses TKIP which has known vulnerabilities. "
                   "Upgrade to WPA2 or WPA3 for better security.")
        else:
            return "Unknown encryption type - investigate further for security assessment."

    def _generate_security_summary(self, networks):
        """Generate overall security summary"""
        summary = {
            'encryption_distribution': Counter(),
            'signal_strength_analysis': {},
            'security_score': 0,
            'risk_level': 'Unknown'
        }

        # Analyze encryption distribution
        for network in networks:
            encryption = network.get('encryption', 'Unknown').upper()

            if 'WPA3' in encryption:
                summary['encryption_distribution']['WPA3'] += 1
            elif 'WPA2' in encryption:
                summary['encryption_distribution']['WPA2'] += 1
            elif 'WPA' in encryption:
                summary['encryption_distribution']['WPA'] += 1
            elif 'WEP' in encryption:
                summary['encryption_distribution']['WEP'] += 1
            elif 'OPEN' in encryption or 'NONE' in encryption:
                summary['encryption_distribution']['Open'] += 1
            else:
                summary['encryption_distribution']['Unknown'] += 1

        # Calculate security score (0-100)
        total = len(networks)
        if total > 0:
            wpa3_score = summary['encryption_distribution'].get('WPA3', 0) * 100
            wpa2_score = summary['encryption_distribution'].get('WPA2', 0) * 80
            wpa_score = summary['encryption_distribution'].get('WPA', 0) * 40
            wep_score = summary['encryption_distribution'].get('WEP', 0) * 10
            open_score = summary['encryption_distribution'].get('Open', 0) * 0

            summary['security_score'] = (wpa3_score + wpa2_score + wpa_score + wep_score + open_score) // total

        # Determine risk level
        if summary['security_score'] >= 80:
            summary['risk_level'] = 'Low'
        elif summary['security_score'] >= 60:
            summary['risk_level'] = 'Medium'
        elif summary['security_score'] >= 40:
            summary['risk_level'] = 'High'
        else:
            summary['risk_level'] = 'Critical'

        return summary

    def _generate_recommendations(self, analysis_results):
        """Generate security recommendations based on analysis"""
        recommendations = []

        vulnerabilities = analysis_results['vulnerabilities']
        security_summary = analysis_results['security_summary']

        # Encryption recommendations
        wep_count = security_summary['encryption_distribution'].get('WEP', 0)
        open_count = security_summary['encryption_distribution'].get('Open', 0)

        if wep_count > 0:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Encryption',
                'title': 'Upgrade WEP Networks',
                'description': f'{wep_count} network(s) using vulnerable WEP encryption',
                'action': 'Upgrade to WPA2 or WPA3 immediately',
                'education': 'WEP can be cracked in minutes with freely available tools'
            })

        if open_count > 0:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Encryption',
                'title': 'Secure Open Networks',
                'description': f'{open_count} network(s) with no encryption',
                'action': 'Enable WPA2 or WPA3 encryption with strong passwords',
                'education': 'Open networks expose all traffic to eavesdropping'
            })

        # Default SSID recommendations
        default_ssids = [v for v in vulnerabilities if v['type'] == 'Default SSID']
        if default_ssids:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Configuration',
                'title': 'Change Default SSIDs',
                'description': f'{len(default_ssids)} network(s) using default SSIDs',
                'action': 'Change to unique, non-identifying network names',
                'education': 'Default SSIDs can reveal device information to attackers'
            })

        # General security recommendations
        total_networks = analysis_results['total_networks']
        if total_networks > 0:
            secure_networks = (security_summary['encryption_distribution'].get('WPA2', 0) + 
                             security_summary['encryption_distribution'].get('WPA3', 0))
            secure_percentage = (secure_networks / total_networks) * 100

            if secure_percentage < 50:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'General',
                    'title': 'Improve Overall Security',
                    'description': f'Only {secure_percentage:.1f}% of networks use modern security',
                    'action': 'Promote security awareness and best practices',
                    'education': 'Strong WiFi security protects against various attack vectors'
                })

        return recommendations

    def _display_analysis_results(self, analysis_results):
        """Display comprehensive analysis results"""
        print(f"\n📊 ANALYSIS OVERVIEW:")
        print(f"   • Total Networks Analyzed: {analysis_results['total_networks']}")
        print(f"   • Vulnerabilities Found: {len(analysis_results['vulnerabilities'])}")
        print(f"   • Security Score: {analysis_results['security_summary']['security_score']}/100")
        print(f"   • Risk Level: {analysis_results['security_summary']['risk_level']}")

        # Display encryption distribution
        print(f"\n🔒 ENCRYPTION ANALYSIS:")
        for enc_type, count in analysis_results['security_summary']['encryption_distribution'].items():
            percentage = (count / analysis_results['total_networks']) * 100
            indicator = self._get_security_indicator(enc_type)
            print(f"   • {enc_type}: {count} networks ({percentage:.1f}%) {indicator}")

        # Display vulnerabilities
        if analysis_results['vulnerabilities']:
            print(f"\n🚨 VULNERABILITIES DETECTED:")
            for vuln in analysis_results['vulnerabilities']:
                print(f"\n   {vuln['type']} - {vuln['severity']} Risk")
                print(f"   Network: {vuln['network']}")
                print(f"   Issue: {vuln['description']}")
                print(f"   📚 Education: {vuln['education']}")
                print("   " + "-" * 50)

        # Display recommendations
        if analysis_results['recommendations']:
            print(f"\n💡 SECURITY RECOMMENDATIONS:")
            for rec in analysis_results['recommendations']:
                priority_indicator = self._get_priority_indicator(rec['priority'])
                print(f"\n   {priority_indicator} {rec['title']}")
                print(f"   Issue: {rec['description']}")
                print(f"   Action: {rec['action']}")
                print(f"   📚 Why: {rec['education']}")
                print("   " + "-" * 50)

    def _get_security_indicator(self, encryption_type):
        """Get visual indicator for security level"""
        if encryption_type == 'WPA3':
            return "🟢"
        elif encryption_type == 'WPA2':
            return "🟡"
        elif encryption_type == 'WPA':
            return "🟠"
        elif encryption_type == 'WEP':
            return "🔴"
        elif encryption_type == 'Open':
            return "⚪"
        else:
            return "❓"

    def _get_priority_indicator(self, priority):
        """Get visual indicator for priority level"""
        if priority == 'HIGH':
            return "🔴 HIGH:"
        elif priority == 'MEDIUM':
            return "🟠 MEDIUM:"
        elif priority == 'LOW':
            return "🟡 LOW:"
        else:
            return "ℹ️  INFO:"

    def generate_security_report(self, analysis_results, filename=None):
        """Generate detailed security report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.json"

        # Create reports directory
        import os
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)

        report_data = {
            "report_info": {
                "timestamp": datetime.now().isoformat(),
                "report_type": "Educational WiFi Security Analysis",
                "version": "1.0"
            },
            "executive_summary": {
                "total_networks": analysis_results['total_networks'],
                "vulnerabilities_count": len(analysis_results['vulnerabilities']),
                "security_score": analysis_results['security_summary']['security_score'],
                "risk_level": analysis_results['security_summary']['risk_level']
            },
            "detailed_analysis": analysis_results
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"\n📋 Security report saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None

    def educational_vulnerability_demo(self):
        """Educational demonstration of common vulnerabilities"""
        print("\n" + "="*70)
        print("          EDUCATIONAL VULNERABILITY DEMONSTRATION")
        print("="*70)

        vulnerabilities = [
            {
                'name': 'WEP Encryption',
                'description': 'Uses weak RC4 encryption with static keys',
                'impact': 'Network traffic can be decrypted in minutes',
                'tools': 'Aircrack-ng, Wireshark',
                'mitigation': 'Upgrade to WPA2 or WPA3'
            },
            {
                'name': 'Open Networks',
                'description': 'No encryption protection for network traffic',
                'impact': 'All communications visible to anyone in range',
                'tools': 'Any wireless adapter and packet capture software',
                'mitigation': 'Enable WPA2/WPA3 with strong passwords'
            },
            {
                'name': 'Default Credentials',
                'description': 'Router using factory default login credentials',
                'impact': 'Complete network compromise and configuration changes',
                'tools': 'Web browser, credential dictionaries',
                'mitigation': 'Change default usernames and passwords immediately'
            },
            {
                'name': 'WPS PIN Attack',
                'description': 'WiFi Protected Setup with vulnerable PIN authentication',
                'impact': 'Network password can be brute-forced',
                'tools': 'Reaver, Bully',
                'mitigation': 'Disable WPS or use push-button method only'
            }
        ]

        for i, vuln in enumerate(vulnerabilities, 1):
            print(f"\n{i}. {vuln['name']}")
            print(f"   📝 Description: {vuln['description']}")
            print(f"   💥 Impact: {vuln['impact']}")
            print(f"   🛠️  Tools: {vuln['tools']}")
            print(f"   ✅ Mitigation: {vuln['mitigation']}")

        print(f"\n📚 Educational Note:")
        print("   Understanding these vulnerabilities helps in:")
        print("   • Identifying security weaknesses")
        print("   • Implementing proper defenses")
        print("   • Educating others about WiFi security")
        print("   • Building a security-conscious mindset")
