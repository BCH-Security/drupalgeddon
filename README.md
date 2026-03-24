# Drupalgeddon Vulnerability Research & Exploit Scripts

This project is a collection of proof-of-concept (PoC) scripts demonstrating and analyzing well-known vulnerabilities in Drupal CMS commonly referred to as:

- Drupalgeddon 1  
- Drupalgeddon 2  
- Drupalgeddon 3  

The goal of this project is to understand how these vulnerabilities work at a technical level, how they can be identified, and how they impact insecure systems.

---

##  Disclaimer

This project is intended strictly for:

- Educational purposes  
- Cybersecurity research  
- Authorized penetration testing in controlled environments (labs, CTFs, test systems)

**Do NOT use these scripts against systems you do not own or have explicit permission to test.**

---

## Objectives

- Understand common vulnerabilities affecting web applications
- Analyze exploitation techniques used in historical Drupal vulnerabilities
- Practice secure coding awareness and vulnerability assessment
- Demonstrate offensive security research skills

---

##  Requirements

- Python 3.x
- Required Python libraries (depending on script implementation):

```bash
pip install requests
```

## Usage

Each script may vary slightly depending on implementation, but generally:
```bash
python3 drupalgeddon1.py -u http://target-url
python3 drupalgeddon2.py -u http://target-url
python3 drupalgeddon3.py -u http://target-url
```

## Vulnerability Overview
1- Drupalgeddon 1:
- A remote code execution vulnerability affecting Drupal core
- Exploits insufficient input sanitization in form processing

2- Drupalgeddon 2:
- Remote code execution via renderable arrays
- Allows attackers to inject malicious payloads into form parameters

3- Drupalgeddon 3:
- Privilege escalation / access bypass scenario
- Involves exploitation of access control weaknesses




