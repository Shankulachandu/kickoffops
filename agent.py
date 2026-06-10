import os
from google.adk.integrations.agent_registry import AgentRegistry
from google.auth import default
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

# Setup
_, project_id = default()
LOCATION = os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Connect to GitLab MCP
registry = AgentRegistry(project_id=project_id, location=LOCATION)
mcp_toolset = registry.get_mcp_toolset(
    "projects/feisty-album-312109/locations/global/mcpServers/agentregistry-00000000-0000-0000-6dcf-dce13ad97dc2"
)

# KickoffOps Agent
root_agent = Agent(
    name="kickoffops",
    description=(
        "You are KickoffOps, an AI DevOps agent for the 2026 World Cup. "
        "You monitor GitLab CI/CD pipelines, detect failures, read error logs, "
        "diagnose the root cause, and automatically create GitLab issues with "
        "a plain-English summary and suggested fix. "
        "When asked to check pipelines, always: "
        "1. List failed pipelines "
        "2. Get the logs from the failed job "
        "3. Diagnose the error "
        "4. Create a GitLab issue with your findings."
    ),
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    tools=[mcp_toolset],
)