"""
Semantic Kernel equivalent of demo1-AIFoundryAgents.py
This demonstrates the differences between Agent Framework and Semantic Kernel
"""
import asyncio
import os
from dotenv import load_dotenv

# Semantic Kernel imports - notice more imports needed
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from azure.identity.aio import DefaultAzureCredential

load_dotenv()

async def main():
    # 1. Create Kernel - this is required in SK but not in Agent Framework
    kernel = Kernel()    
    # 2. Configure the Azure OpenAI service
    # Need more configuration compared to Agent Framework
    credential = DefaultAzureCredential()
    
    # Add the chat completion service to the kernel
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            ad_token_provider=credential.get_token,
        )
    )    
    # 3. Create the agent with kernel and instructions
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="JokeAgent",
        instructions="You are good at telling jokes.",
    )    
    # 4. Create chat history (required in SK)
    chat_history = ChatHistory()    
    # 5. Add user message to history
    chat_history.add_user_message("Tell me a joke about a pirate.")    
    # 6. Invoke the agent
    async for message in agent.invoke(chat_history):
        print(message.content)


if __name__ == "__main__":
    asyncio.run(main())
