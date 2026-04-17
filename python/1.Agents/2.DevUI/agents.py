"""DevUI demo script: builds a weather ChatAgent (Azure/OpenAI) and serves it locally."""

import os
import logging
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.openai import OpenAIChatClient
from agent_framework.devui import serve
from dotenv import load_dotenv

# Tool function returning a mock current weather report for a given city.
def get_weather(city: str) -> str:
    """Return a mock current weather string for the provided city."""
    return f"The weather in {city} is 73 degrees and Sunny."

# Tool function returning a mock short-term forecast.
def get_forecast() -> str:
    """Return a mock 3‑day weather forecast summary."""
    return "Expect sunny skies for the next 3 days."

# Create Agent instance following Agent Framework conventions
# Load environment variables from .env if present (override existing process values)
load_dotenv(override=True)  # Load .env file values (override existing process env vars)

# Azure credentials and deployment identifiers.
azure_api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
azure_deployment = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "")
# OpenAI fallback credentials and model selection.
openai_api_key = os.environ.get("OPENAI_API_KEY", "")
openai_model = os.environ.get("OPENAI_CHAT_MODEL_ID", "gpt-4o-mini")

# Select chat client: prefer Azure if fully configured, else fallback to OpenAI
if azure_api_key and azure_endpoint and azure_deployment:
    chat_client = AzureOpenAIChatClient(
        api_key=azure_api_key,
        endpoint=azure_endpoint,
        deployment_name=azure_deployment,
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "") or None,
    )
elif openai_api_key:
    chat_client = OpenAIChatClient(
        api_key=openai_api_key,
        model_id=openai_model,
    )
else:
    raise RuntimeError(
        "No chat client configured. Set Azure (AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME) or OpenAI (OPENAI_API_KEY, OPENAI_CHAT_MODEL_ID)."
    )


agent = ChatAgent(
    name="AzureWeatherAgent",  # Unique identifier used by DevUI
    description="A helpful agent that provides weather information and forecasts",  # Shown to users as summary
    instructions="""
    You are a weather assistant. You can provide current weather information
    and forecasts for any location. Always be helpful and provide detailed
    weather information when asked.
    """,  # System prompt guiding agent behavior
    chat_client=chat_client,  # Underlying model client (Azure or OpenAI)
    tools=[get_weather, get_forecast],  # Registered callable tool functions
)

def main():
    """Launch the Azure weather agent in DevUI."""
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)
    logger.info("Starting Azure Weather Agent")
    logger.info("Available at: http://localhost:8090")
    logger.info("Entity ID: agent_AzureWeatherAgent")

    # Launch server with the agent
    serve(entities=[agent], port=8090, auto_open=True)

if __name__ == "__main__":
    main()
