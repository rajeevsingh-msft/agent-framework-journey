"""
Agent Framework Multi-Agent Demo
Simple demonstration of creating multiple specialized agents
"""

import asyncio
import os
import time
import json
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

load_dotenv()

class MultiAgentDemo:
    def __init__(self):
        self.credential = None
        self.food_agent_client = None
        self.meal_agent_client = None
        self.food_agent = None
        self.meal_agent = None
        self.system_ready = False
        self.registry_file = "agents_registry.json"
        
    async def initialize(self):
        """Initialize the multi-agent system"""
        print("🚀 Initializing Multi-Agent System...")
        
        try:
            # Create separate clients for each agent
            self.credential = AzureCliCredential()
            self.food_agent_client = AzureAIAgentClient(async_credential=self.credential)
            self.meal_agent_client = AzureAIAgentClient(async_credential=self.credential)
            
            # Check existing agents
            await self.check_registry()
            #1. Agent Creation – The Foundation
            # Create Food Expert Agent
            if self.food_agent is None:
                self.food_agent = ChatAgent(
                    chat_client=self.food_agent_client,
                    name="FoodExpertAgent",
                    instructions="""You are a Food & Nutrition Expert. Provide accurate nutritional 
                    information, calorie content, and ingredient analysis. Be specific and helpful."""
                )
                
                # Test agent creation
                await self.food_agent.run("Hello!")
                self.register_agent("FoodExpertAgent", "nutrition")
                print("✅ FoodExpertAgent created")
                
            # Create Meal Planning Agent
            if self.meal_agent is None:
                self.meal_agent = ChatAgent(
                    chat_client=self.meal_agent_client,
                    name="MealPlanningAgent",
                    instructions="""You are a Meal Planning Specialist. Suggest healthy meals, 
                    recipes, and dietary plans based on user preferences and needs."""
                )
                
                # Test agent creation
                await self.meal_agent.run("Hello!")
                self.register_agent("MealPlanningAgent", "meal_planning")
                print("✅ MealPlanningAgent created")
            
            self.system_ready = True
            print("🎉 Multi-Agent System Ready!")
            
        except Exception as e:
            print(f"❌ Initialization failed: {str(e)}")
            self.system_ready = False
    
    def load_registry(self):
        """Load agent registry"""
        try:
            if os.path.exists(self.registry_file):
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def save_registry(self, registry):
        """Save agent registry"""
        try:
            with open(self.registry_file, 'w') as f:
                json.dump(registry, f, indent=2)
        except:
            pass
    
    def register_agent(self, agent_name, agent_type):
        """Register agent to prevent duplicates"""
        registry = self.load_registry()
        registry[agent_name] = {
            "type": agent_type,
            "created_at": time.time(),
            "status": "active"
        }
        self.save_registry(registry)
    #5. Agent Persistence – The Efficiency
    async def check_registry(self):
        """Check for existing agents"""
        registry = self.load_registry()
        
        if "FoodExpertAgent" in registry:
            print("📋 FoodExpertAgent found in registry")
        else:
            print("🆕 Creating new FoodExpertAgent")
            
        if "MealPlanningAgent" in registry:
            print("📋 MealPlanningAgent found in registry")  
        else:
            print("🆕 Creating new MealPlanningAgent")
    
    def detect_intent(self, user_input):
        """Route queries to appropriate agent"""
        text = user_input.lower()
        
        # Nutrition-related keywords
        food_keywords = ['calories', 'nutrition', 'protein', 'carbs', 'fat', 
                        'vitamins', 'nutrients', 'ingredients', 'analyze']
        
        # Meal-related keywords  
        meal_keywords = ['suggest', 'recommend', 'meal', 'breakfast', 'lunch', 
                        'dinner', 'recipe', 'cook', 'plan', 'diet']
        
        if any(keyword in text for keyword in food_keywords):
            return "food_expert"
        elif any(keyword in text for keyword in meal_keywords):
            return "meal_planner"
        else:
            return "meal_planner"
    
    #2. Intelligent Query Routing – The Brain
    async def process_query(self, user_input):
        """Process user query with intelligent routing"""
        if not self.system_ready:
            return {"error": "System not ready"}
        
        intent = self.detect_intent(user_input)
        
        try:
            if intent == "food_expert":
                print("🍎 Routing to FoodExpertAgent...")
                result = await self.food_agent.run(user_input)
                return {"agent": "Food Expert", "response": result.text}
            else:
                print("🍽️ Routing to MealPlanningAgent...")
                result = await self.meal_agent.run(user_input)
                return {"agent": "Meal Planner", "response": result.text}
                
        except Exception as e:
            return {"error": str(e)}
    
    #4. Multi-Agent Coordination – The Power
    #One simple .run() call executes the agent with full Azure AI power behind it.
    async def multi_agent_query(self, user_input):
        """Use both agents for comprehensive analysis"""
        print("🤝 Using both agents...")
        
        try:
            food_task = self.food_agent.run(f"Analyze nutrition: {user_input}")
            meal_task = self.meal_agent.run(f"Suggest meals for: {user_input}")
            
            food_result, meal_result = await asyncio.gather(food_task, meal_task)
            
            return {
                "food_analysis": food_result.text,
                "meal_suggestions": meal_result.text
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def run_demo(self):
        """Interactive demo"""
        print("\n" + "="*50)
        print("AGENT FRAMEWORK MULTI-AGENT DEMO")
        print("="*50)
        print("Commands: 'both' (use both agents), 'quit' (exit)")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                elif user_input.lower() == 'both':
                    question = input("Question for both agents: ").strip()
                    if question:
                        response = await self.multi_agent_query(question)
                        if "error" in response:
                            print(f"❌ Error: {response['error']}")
                        else:
                            print(f"\n🍎 Food Expert: {response['food_analysis']}")
                            print(f"\n🍽️ Meal Planner: {response['meal_suggestions']}")
                    continue
                
                elif not user_input:
                    continue
                
                response = await self.process_query(user_input)
                
                if "error" in response:
                    print(f"❌ Error: {response['error']}")
                else:
                    print(f"\n{response['agent']}: {response['response']}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.credential:
                await self.credential.close()
        except:
            pass

async def main():
    """Main function"""
    print("Agent Framework Multi-Agent Demo")
    print("=" * 40)
    
    demo = MultiAgentDemo()
    
    try:
        await demo.initialize()
        
        if demo.system_ready:
            await demo.run_demo()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        
    finally:
        await demo.cleanup()
        print("👋 Demo complete!")

if __name__ == "__main__":
    asyncio.run(main())