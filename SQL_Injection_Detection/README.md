# SQL Injection Detection & Data Leak Prevention System

## Overview

This project is developed as part of the CodeAlpha Cloud Computing Internship.

The system is designed to protect user data against SQL Injection attacks using secure coding practices, AES encryption, capability code verification, and a double-layer security protocol.

---

## Objectives

- Secure user data against SQL Injection attacks.
- Encrypt sensitive user credentials.
- Implement capability code verification.
- Provide double-layer security protection.
- Monitor and log security-related events.
- Build a lightweight cloud-accessible web application.

---

## Features

### Security Layer 1
- AES Encrypted Credential Storage
- Secure Password Protection

### Security Layer 2
- SQL Injection Detection Engine
- Capability Code Verification
- Parameterized SQL Queries

### Monitoring
- Security Event Logging
- Login Monitoring
- Attack Detection Tracking

### Dashboard
- Total Registered Users
- Security Event Statistics
- Recent Security Logs
- Security Layer Status

---

## Technologies Used

- Python
- Flask
- SQLite
- Cryptography Library
- HTML
- CSS

---

## Project Structure

```text
CodeAlpha_SQL_Injection_Detection
│
├── app.py
├── users.db
├── secret.key
├── requirements.txt
├── README.md
└── templates
    ├── login.html
    ├── register.html
    └── dashboard.html
```

---

## Security Architecture

### AES Encryption
User credentials are encrypted before storage to ensure data confidentiality.

### SQL Injection Protection
The application detects malicious SQL patterns and blocks unauthorized access attempts.

### Capability Code Mechanism
Only users with a valid capability code can register within the system.

### Double Layer Security Protocol

Layer 1:
- AES Encryption

Layer 2:
- SQL Injection Detection
- Capability Code Validation

---

## Test Cases

### Valid Registration
- User successfully registers with correct capability code.

### Invalid Capability Code
- Registration is blocked.

### SQL Injection Attempt

Example:

```sql
' OR 1=1 --
```

Result:
- Attack detected and blocked.

---

## Future Enhancements

- Role-Based Access Control
- Multi-Factor Authentication
- Cloud Deployment
- Real-Time Security Analytics

---

## Author

**Yaseera**

CodeAlpha Cloud Computing Internship

Task 2 – Detecting Data Leaks Using SQL Injection