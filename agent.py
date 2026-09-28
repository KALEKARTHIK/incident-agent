import os
import json

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

from groq_llm import generate_response


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

HINDSIGHT_URL = "https://api.hindsight.vectorize.io"
BANK_ID = "incident-agent"

hindsight = Hindsight(
    base_url=HINDSIGHT_URL,
    api_key=os.environ["HINDSIGHT_API_KEY"]
)


# --------------------------------------------------
# HINDSIGHT RECALL
# --------------------------------------------------

def recall_incidents(alert: str, limit: int = 8):
    """
    Retrieve previous incidents related to the
    current incident.
    """

    result = hindsight.recall(
        bank_id=BANK_ID,
        query=alert
    )

    memories = []

    for memory in result.results[:limit]:
        memories.append(memory.text)

    return memories


# --------------------------------------------------
# ASK LLM TO ANALYZE MEMORY
# --------------------------------------------------

def analyze_incident(alert: str, memories: list[str]):
    """
    Ask the LLM to determine whether a previous
    solved incident can be reused.

    If no sufficiently similar solved incident
    exists, the LLM solves the incident from scratch.
    """

    if memories:

        memory_text = "\n\n".join(
            f"MEMORY {i + 1}:\n{memory}"
            for i, memory in enumerate(memories)
        )

    else:

        memory_text = "NO PREVIOUS MEMORIES FOUND."


    prompt = f"""
You are a cybersecurity incident-response AI assistant.

Your task is to analyze the CURRENT INCIDENT using
the PREVIOUS INCIDENT MEMORIES.

CURRENT INCIDENT:
{alert}


PREVIOUS INCIDENT MEMORIES:
{memory_text}


FOLLOW THESE RULES CAREFULLY:

1. Look through the previous memories.

2. Determine whether there is a genuinely similar
   previously resolved incident.

3. A memory should only be reused if it is directly
   relevant to the current incident and contains a
   useful previous resolution.

4. Do NOT reuse a vaguely related incident. If the memories
   only partially overlap with the current incident, or
   describe a different root cause, prefer "NEW" over "REUSE".

5. If a sufficiently similar previous resolution exists:
   - Set mode to "REUSE"
   - Use the previous solution
   - Do not invent a completely different solution.

6. If no sufficiently similar previous resolution exists:
   - Set mode to "NEW"
   - Analyze the current incident yourself.
   - Identify the likely root cause.
   - Provide recommended actions.

7. Do not claim certainty when the evidence is insufficient.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "mode": "REUSE" or "NEW",
    "root_cause": "Likely root cause",
    "solution": "Recommended or previously used solution",
    "reason": "Why the previous solution was reused or why a new analysis was required"
}}
"""


    response = generate_response(prompt)

    response = response.strip()

    # Remove markdown code fences if the model adds them
    if response.startswith("```"):

        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()


    try:

        result = json.loads(response)

        return result

    except json.JSONDecodeError:

        print("\nWarning: LLM returned invalid JSON.")

        return {
            "mode": "NEW",
            "root_cause": "Unable to parse model response.",
            "solution": response,
            "reason": "The LLM did not return valid JSON."
        }


# --------------------------------------------------
# SAVE VERIFIED INCIDENT RESOLUTION
# --------------------------------------------------

def save_incident_resolution(
    alert: str,
    root_cause: str,
    solution: str,
    source: str
):
    """
    Store a verified incident resolution in Hindsight.
    """

    content = f"""
INCIDENT RESOLUTION

Incident:
{alert}

Root Cause:
{root_cause}

Solution:
{solution}

Resolution Source:
{source}
"""

    hindsight.retain(
        bank_id=BANK_ID,
        content=content,
        context="Verified cybersecurity incident resolution"
    )

    print("\nIncident resolution saved to Hindsight.")


# --------------------------------------------------
# MAIN INCIDENT HANDLER
# --------------------------------------------------

def handle_incident(alert: str):

    print("\n========================================")
    print("       INCIDENT RESPONSE AGENT")
    print("========================================")

    print("\nCurrent Incident:")
    print(alert)


    # ----------------------------------------------
    # STEP 1: HINDSIGHT RECALL
    # ----------------------------------------------

    print("\n[1] Searching Hindsight memory...")

    memories = recall_incidents(alert)

    print(
        f"Found {len(memories)} related memories."
    )

    # Debug: show exactly what was recalled, so you can verify
    # the LLM's REUSE/NEW decision is actually justified.
    for i, m in enumerate(memories, start=1):
        print(f"\n--- Memory {i} ---\n{m}")


    # ----------------------------------------------
    # STEP 2: LLM ANALYSIS
    # ----------------------------------------------

    print("\n[2] Asking LLM to analyze memories...")

    result = analyze_incident(
        alert,
        memories
    )


    # ----------------------------------------------
    # STEP 3: DISPLAY RESULT
    # ----------------------------------------------

    print("\n========================================")

    if result["mode"] == "REUSE":

        print("PREVIOUS SOLUTION FOUND")

    else:

        print("NO SUFFICIENT PREVIOUS SOLUTION")

    print("========================================")


    print("\nRoot Cause:")
    print(result["root_cause"])


    print("\nSolution:")
    print(result["solution"])


    print("\nReason:")
    print(result["reason"])


    # ----------------------------------------------
    # STEP 4: VERIFY NEW SOLUTION
    # ----------------------------------------------

    if result["mode"] == "NEW":

        print("\n========================================")
        print("The LLM generated a new solution.")
        print("Review the solution above before saving it.")
        print("========================================")

        approval = input(
            "\nDo you approve this solution for future use? (yes/no): "
        ).strip().lower()


        if approval == "yes":

            save_incident_resolution(
                alert=alert,
                root_cause=result["root_cause"],
                solution=result["solution"],
                source="LLM generated and user verified"
            )

        else:

            print("\nSolution was NOT saved to Hindsight.")


    print("\n========================================")


# --------------------------------------------------
# PROGRAM ENTRY
# --------------------------------------------------

if __name__ == "__main__":

    alert = input(
        "\nEnter an incident: "
    )

    handle_incident(alert)