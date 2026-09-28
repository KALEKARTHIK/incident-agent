import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load variables from .env
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

print("Connected to Hindsight!")

# Store a test memory
client.retain(
    bank_id="incident-agent",
    content="Database timeouts on the payments API were fixed by increasing the connection pool size."
)

print("Memory stored successfully!")

# Search the memory
result = client.recall(
    bank_id="incident-agent",
    query="What fixed the payments API timeouts?"
)

print("\nMemories found:")

for memory in result.results:
    print(memory.text)