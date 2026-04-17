import asyncio
import os
from dotenv import load_dotenv
from agent_framework import Agent  # GA API: Using Agent class
from agent_framework.foundry import FoundryChatClient  # 🆕 Enhanced client
from azure.identity.aio import AzureCliCredential

load_dotenv()

async def main():
    try:  # 🆕 Enhanced error handling
        async with (
            AzureCliCredential() as credential,
            Agent(
                client=FoundryChatClient(
                    model=os.getenv("FOUNDRY_MODEL", "gpt-4o"),
                    credential=credential
                ),  # GA API: 'client' parameter with model
                instructions="You are helpful.",
                name="MyAgent"  # 🆕 GA feature: named agents
            ) as agent,
        ):
            result = await agent.run("Tell me a joke")
            print(f"Agent: {result.text}")  # 🆕 Enhanced output formatting
    except Exception as e:  # 🆕 Structured error handling
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())