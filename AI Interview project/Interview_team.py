from json import load
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("GEMINI_KEY")

model_client = OpenAIChatCompletionClient(model="gemini-2.0-flash",api_key = api_key)

### Define the Interviewer Assistant

interviewer_agent = AssistantAgent(
    name = "Interviewer_Assistant"
    model_client=model_client

)