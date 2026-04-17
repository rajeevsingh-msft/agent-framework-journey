import asyncio
import os
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient  # Client adapter for Azure AI Foundry model access
from azure.identity.aio import AzureCliCredential

load_dotenv()

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())