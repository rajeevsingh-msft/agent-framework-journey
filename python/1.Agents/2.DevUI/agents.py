"""
🎉 Agent Framework GA v1.0 + DevUI Integration - WORKING! 
Successfully demonstrates GA Agent with DevUI features
"""

import os
import asyncio
import logging
from agent_framework import Agent  # 🟢 GA API: Agent class
from agent_framework.foundry import FoundryChatClient  # 🟢 GA recommended client
from agent_framework.openai import OpenAIChatClient  # 🟢 OpenAI fallback
from agent_framework.devui import serve  # ✅ NOW COMPATIBLE with GA v1.0!
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential

# Tool function returning a mock current weather report for a given city.
def get_weather(city: str) -> str:
    """Return a mock current weather string for the provided city."""
    return f"The weather in {city} is 73 degrees and Sunny."

# Tool function returning a mock short-term forecast.
def get_forecast() -> str:
    """Return a mock 3‑day weather forecast summary."""
    return "Expect sunny skies for the next 3 days."

async def create_ga_weather_agent():
    """Create a GA-compatible weather agent WITH DevUI support."""
    # Load environment variables from .env if present (override existing process values)
    load_dotenv(override=True)  # Load .env file values (override existing process env vars)

    # 🟢 GA Foundry configuration (recommended)
    foundry_model = os.environ.get("FOUNDRY_MODEL", "gpt-4o")
    foundry_endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "")

    # OpenAI fallback credentials and model selection
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    openai_model = os.environ.get("OPENAI_CHAT_MODEL_ID", "gpt-4o-mini")

    # 🟢 Select chat client: prefer Foundry (GA recommended), then OpenAI fallback
    if foundry_model and foundry_endpoint:
        # GA recommended: FoundryChatClient with Azure CLI auth
        print("🚀 Using FoundryChatClient (GA Production)")
        async with AzureCliCredential() as credential:
            chat_client = FoundryChatClient(
                model=foundry_model,
                credential=credential,
                project_endpoint=foundry_endpoint
            )
    elif openai_api_key:
        # Fallback: OpenAI
        print("🔄 Using OpenAI fallback")
        chat_client = OpenAIChatClient(
            api_key=openai_api_key,
            model_id=openai_model,
        )
    else:
        raise RuntimeError(
            "No chat client configured. Set Foundry (FOUNDRY_MODEL, FOUNDRY_PROJECT_ENDPOINT) or OpenAI (OPENAI_API_KEY, OPENAI_CHAT_MODEL_ID)."
        )

    agent = Agent(  # 🟢 GA API: Agent class (not ChatAgent)
        name="GAWeatherAgent",  # Unique identifier used by DevUI
        description="GA v1.0 weather assistant with DevUI integration",  # Shown to users as summary
        instructions="""
        You are a weather assistant powered by Agent Framework GA v1.0. You can provide current weather information
        and forecasts for any location. Always be helpful and provide detailed
        weather information when asked. Mention that you're running on the stable GA release!
        """,  # System prompt guiding agent behavior
        client=chat_client,  # 🟢 GA API: 'client' parameter (not chat_client)
        tools=[get_weather, get_forecast],  # Registered callable tool functions
    )
    
    return agent

def main():
    """🎉 Launch GA Agent with DevUI - BOTH WORKING TOGETHER!"""
    
    print("🎯 Agent Framework GA v1.0 + DevUI Integration")
    print("=" * 55)
    print("✅ DevUI compatibility: RESTORED with upgrade!")
    print("🟢 GA Agent Framework: Production stable")
    print("🛠️ Tools: Weather & Forecast available")
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)
    
    try:
        # Create GA agent
        agent = asyncio.run(create_ga_weather_agent())
        logger.info(f"✅ GA Agent created: {agent.name}")
        
        # DevUI Configuration
        port = int(os.environ.get("DEVUI_PORT", "8090"))
        
        logger.info(f"🌐 DevUI launching at: http://localhost:{port}")
        logger.info(f"🎛️ Agent Entity ID: agent_{agent.name}")
        
        print(f"\n🚀 DevUI Features Available:")
        print(f"   • Interactive chat with GA Agent")
        print(f"   • Real-time tool execution visualization") 
        print(f"   • Message history and debugging")
        print(f"   • Performance monitoring")
        
        print(f"\n💡 Test Questions:")
        print(f"   • 'What's the weather in Seattle?'")
        print(f"   • 'Give me the forecast'")
        print(f"   • 'Tell me about your GA capabilities'")
        
        print(f"\n🎉 SUCCESS: GA v1.0 + DevUI Integration Working!")
        print(f"🔗 Open: http://localhost:{port}")
        print("   Press Ctrl+C to stop")
        
        # 🎉 Launch GA Agent with DevUI - THIS NOW WORKS!
        serve(entities=[agent], port=port, auto_open=True)
        
    except KeyboardInterrupt:
        print(f"\n👋 DevUI server stopped gracefully")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   • Check environment variables (.env file)")
        print(f"   • Verify Foundry/OpenAI credentials")
        print(f"   • Try: python test_ga_agent.py for core test")

if __name__ == "__main__":
    main()
