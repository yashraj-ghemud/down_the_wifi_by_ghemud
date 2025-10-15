#!/usr/bin/env python3
"""
Ethical Framework Module
Ensures all operations comply with ethical hacking principles and legal requirements.
"""

import os
import json
from datetime import datetime

class EthicalFramework:
    def __init__(self):
        self.consent_verified = False
        self.legal_warnings_shown = False

    def verify_ethical_usage(self):
        """Verify user understands ethical and legal implications"""
        print("\n" + "="*60)
        print("           ETHICAL HACKING VERIFICATION")
        print("="*60)

        print("""
⚖️  LEGAL AND ETHICAL REQUIREMENTS:

1. AUTHORIZATION: You must have explicit written permission to test any network
   that is not your own personal network.

2. SCOPE LIMITATION: Testing must be limited to authorized systems only.

3. NO MALICIOUS INTENT: This tool is for educational and defensive purposes only.

4. RESPONSIBLE DISCLOSURE: Any vulnerabilities found must be reported responsibly.

5. COMPLIANCE: You must comply with all applicable laws in your jurisdiction.

🚨 IMPORTANT WARNINGS:
   • Unauthorized network scanning may be illegal
   • Accessing networks without permission is a criminal offense
   • Educational use does not exempt you from legal requirements
   • Always obtain written consent before testing
""")

        # Require explicit consent
        print("\nI understand and agree to use this tool ethically and legally.")
        consent = input("Type 'I AGREE' to continue: ").strip().upper()

        if consent != 'I AGREE':
            print("\n❌ Ethical consent not provided. Cannot proceed.")
            return False

        # Network ownership verification
        print("\n🔍 NETWORK OWNERSHIP VERIFICATION:")
        print("1. I own this network")
        print("2. I have written permission to test this network")
        print("3. This is a designated testing environment")

        ownership = input("\nSelect your situation (1-3): ").strip()

        if ownership not in ['1', '2', '3']:
            print("\n❌ Valid authorization not confirmed. Cannot proceed.")
            return False

        if ownership == '2':
            print("\n📋 Please ensure you have WRITTEN permission before proceeding.")
            confirm = input("Do you have written permission? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("\n❌ Written permission required. Cannot proceed.")
                return False

        self.consent_verified = True
        self.legal_warnings_shown = True

        # Log ethical verification
        self._log_ethical_verification(ownership)

        print("\n✅ Ethical verification completed successfully.")
        return True

    def _log_ethical_verification(self, ownership_type):
        """Log the ethical verification for audit purposes"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "verification_status": "passed",
            "ownership_type": ownership_type,
            "user": os.getenv("USER", "unknown")
        }

        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # Log to file
        log_file = f"logs/ethical_verification_{datetime.now().strftime('%Y%m%d')}.json"

        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"⚠️  Warning: Could not write to log file: {e}")

    def show_educational_disclaimer(self):
        """Show educational disclaimer"""
        print("""
📚 EDUCATIONAL DISCLAIMER:

This tool is designed for:
✓ Learning network security concepts
✓ Understanding WiFi protocols and security
✓ Practicing ethical hacking in controlled environments
✓ Developing defensive cybersecurity skills

This tool is NOT designed for:
❌ Accessing unauthorized networks
❌ Malicious hacking activities  
❌ Circumventing security controls
❌ Any illegal activities

Remember: With great power comes great responsibility!
""")

    def get_safety_guidelines(self):
        """Return safety guidelines for users"""
        return [
            "Always obtain explicit written permission before testing",
            "Only test networks you own or are authorized to test",
            "Document all testing activities for legal protection",
            "Follow responsible disclosure practices",
            "Respect privacy and confidentiality",
            "Stay within the agreed scope of testing",
            "Stop immediately if asked by network owners",
            "Keep learning materials and tools updated",
            "Report any accidents or unintended access immediately",
            "Maintain professional ethics at all times"
        ]

    def is_authorized(self):
        """Check if ethical authorization has been verified"""
        return self.consent_verified and self.legal_warnings_shown
