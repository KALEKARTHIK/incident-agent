from local_llm import generate_response


prompt = """
You are a cybersecurity incident response assistant.

A server is receiving hundreds of failed SSH login
attempts from an external IP address.

Give:
1. Likely root cause
2. Recommended actions
3. Investigation steps
"""


print("Sending request to local LLM...\n")

response = generate_response(prompt)

print("LOCAL LLM RESPONSE")
print("==================")
print(response)