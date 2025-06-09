from google.adk.agents import Agent
import os

def _load_instructions():
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r", encoding="utf-8") as f:
        return f.read()

root_agent = Agent(
    name="user_profile_agent",
    model="gemini-2.5-flash-preview-05-20",
    description=(
        "Manages user identity, authentication, and persistent profile data in Firebase."
    ),
    instruction=_load_instructions(),
    tools=[],
)
