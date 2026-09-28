import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("HINDSIGHT_API_KEY")

if not api_key:
    raise ValueError("HINDSIGHT_API_KEY is missing from .env")

# Connect to Hindsight
client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=api_key,
)

# Your Hindsight memory bank
BANK_ID = "incident-agent"

# 15 sample cybersecurity/IT incidents
incidents = [
    {
        "service": "Payment API",
        "symptom": "Frequent database connection timeouts",
        "error_log": "Connection pool exhausted",
        "root_cause": "Too many simultaneous database connections",
        "fix": "Increased database connection pool size and restarted the service",
        "minutes_to_resolve": 18,
    },
    {
        "service": "Web Server",
        "symptom": "CPU usage reached 100%",
        "error_log": "High CPU utilization detected",
        "root_cause": "A runaway application process consumed excessive CPU",
        "fix": "Identified and terminated the runaway process, then restarted the application",
        "minutes_to_resolve": 22,
    },
    {
        "service": "SSH Server",
        "symptom": "Hundreds of failed login attempts",
        "error_log": "Multiple authentication failures from external IP",
        "root_cause": "Automated SSH brute-force attack",
        "fix": "Blocked the attacking IP and enabled stronger SSH authentication controls",
        "minutes_to_resolve": 12,
    },
    {
        "service": "Network Gateway",
        "symptom": "Sudden massive increase in network traffic",
        "error_log": "Inbound traffic exceeded normal threshold",
        "root_cause": "Possible DDoS traffic spike",
        "fix": "Applied traffic filtering and rate limiting to suspicious sources",
        "minutes_to_resolve": 35,
    },
    {
        "service": "Customer Database",
        "symptom": "Suspicious SQL queries detected",
        "error_log": "Unexpected UNION SELECT query in web request",
        "root_cause": "SQL injection attempt through an input field",
        "fix": "Enabled parameterized queries and blocked the malicious request",
        "minutes_to_resolve": 25,
    },
    {
        "service": "Authentication Service",
        "symptom": "Large number of login failures for multiple accounts",
        "error_log": "Repeated authentication failures",
        "root_cause": "Credential brute-force attack",
        "fix": "Enabled account rate limiting and temporarily blocked suspicious IP addresses",
        "minutes_to_resolve": 20,
    },
    {
        "service": "File Server",
        "symptom": "Large number of files changed unexpectedly",
        "error_log": "Rapid file modification activity detected",
        "root_cause": "Possible malware or ransomware-like activity",
        "fix": "Isolated the affected machine and restored affected files from backup",
        "minutes_to_resolve": 45,
    },
    {
        "service": "Network Monitor",
        "symptom": "One internal host contacted many different ports",
        "error_log": "Port scan pattern detected",
        "root_cause": "Network reconnaissance activity",
        "fix": "Isolated the suspicious host and investigated the source process",
        "minutes_to_resolve": 28,
    },
    {
        "service": "DNS Service",
        "symptom": "Applications could not resolve domain names",
        "error_log": "DNS resolution timeout",
        "root_cause": "DNS server became unavailable",
        "fix": "Restarted the DNS service and configured a secondary DNS server",
        "minutes_to_resolve": 15,
    },
    {
        "service": "API Gateway",
        "symptom": "Large number of authentication errors",
        "error_log": "Invalid API token",
        "root_cause": "Expired API credentials were being used by an application",
        "fix": "Generated new credentials and updated the application configuration",
        "minutes_to_resolve": 17,
    },
    {
        "service": "Outbound Network",
        "symptom": "Unexpected outbound connections from an internal server",
        "error_log": "Connection to unknown external destination",
        "root_cause": "Suspicious application process making external connections",
        "fix": "Blocked the destination and isolated the server for investigation",
        "minutes_to_resolve": 30,
    },
    {
        "service": "File Storage",
        "symptom": "Files were being renamed with unusual extensions",
        "error_log": "Abnormal file rename pattern detected",
        "root_cause": "Malware attempting to modify user files",
        "fix": "Disconnected the affected system and restored files from a clean backup",
        "minutes_to_resolve": 50,
    },
    {
        "service": "Linux Server",
        "symptom": "A normal user gained unexpected administrative privileges",
        "error_log": "Unexpected sudo activity detected",
        "root_cause": "Misconfigured permissions allowed privilege escalation",
        "fix": "Removed excessive permissions and corrected sudo configuration",
        "minutes_to_resolve": 32,
    },
    {
        "service": "Web Application",
        "symptom": "Response times increased dramatically",
        "error_log": "Request queue exceeded configured limit",
        "root_cause": "Sudden increase in legitimate and suspicious web requests",
        "fix": "Enabled rate limiting and increased application capacity",
        "minutes_to_resolve": 27,
    },
    {
        "service": "Database Server",
        "symptom": "Unauthorized queries were detected",
        "error_log": "Database access from an unknown application account",
        "root_cause": "Compromised database credentials",
        "fix": "Disabled the compromised account, rotated credentials, and reviewed database access logs",
        "minutes_to_resolve": 40,
    },
]

print(f"Loading {len(incidents)} incidents into Hindsight...")

for i, incident in enumerate(incidents, start=1):

    content = f"""
Incident #{i}

Service: {incident['service']}

Symptom:
{incident['symptom']}

Error/Alert Log:
{incident['error_log']}

Root Cause:
{incident['root_cause']}

Fix:
{incident['fix']}

Minutes to Resolve:
{incident['minutes_to_resolve']}
"""

    client.retain(
        bank_id=BANK_ID,
        content=content,
    )

    print(f"Incident #{i} stored successfully.")

print("\nAll incidents have been loaded into Hindsight!")