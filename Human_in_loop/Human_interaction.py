from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from dotenv import load_dotenv
import os,asyncio

### Loading The model###########

load_dotenv()
api_key = os.getenv("GEMINI_KEY")
if api_key is None:
    raise ValueError("GEMINI_KEY environment variable not set. Please set it before running the script.")
model_client = OpenAIChatCompletionClient(model= "gemini-2.0-flash",api_key=api_key)

#### Creation of agents########

agent_1 = AssistantAgent(
    model_client = model_client,
    name = "Assistant",
    system_message="""You are an Advanced Stock Market Trader 
    gives best signals to make profit in Options Trading in two Sentences
     with output format of Option Strike price and Buy Price and Expected Target and 
     Return Ratio and Strategy"""
)
user_agent = UserProxyAgent(
    name= "UserProxy",
    description= "A human user",
    
    input_func = input,
)
Agent_team = RoundRobinGroupChat(
    participants = [agent_1,user_agent],
    termination_condition=TextMentionTermination("Approve"),
    max_turns = 4
)
stream = Agent_team.run_stream(task ="Nifty 50")    

async def run_team():
    await Console(stream)
if __name__=="__main__":
    asyncio.run(run_team())