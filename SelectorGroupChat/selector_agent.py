from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.base import TaskResult
from autogen_core import CancellationToken
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("GEMINI_KEY")

model_client = OpenAIChatCompletionClient(model="gemini-2.0-flash",api_key=api_key)

planning_agent = AssistantAgent(
    name = "planning_agent",
    model_client = model_client,
    description="You are a planning agent to create a plan for the task given by the user.",
    system_message= """
    You are a planning agent,
    Your job is to break down complex tasks into smaller sub tasks. 
    Your team members are:

            web_search_agent : Searches for the information in the web.
            data_analyst_agent: performs Calculations.
    You only plan and delegate task - You donot execute themselves.
    When assigning a task use the below format:
    1. <Agent_name>:<task>


    After all the tasks completed,summarize the findings and end with 'TERMINATE'

"""
)

def search_web_tool(query:str)-> str:
    """tools performs the  web search and returns the result.
        args:query 
        """
    if "2006 - 2007 " in query:
        return "The 2006-2007 season was the 105th season of competitive football in England. Chelsea won the Premier League, while Liverpool won the FA Cup."
    elif "2007 - 2008" in query:
        return "The 2007-2008 season was the 106th season of competitive football in England. Manchester United won the Premier League, while Portsmouth won the FA Cup."
    else:
        return "No information available for the specified query."
   
WebSearchAgent = AssistantAgent(
    name = 'web_search_agent',
    description = "You are a great web search agent who solves the task using web.",
    model_client=model_client,
    system_message="""You are a web search agent,
    your only tool is to search the web and return the result.
    You are given a query and you need to search the web and return the result.
    Once you have the result, you never do calculations or analysis.""",
    tools=[search_web_tool],
)

def percentage_calculation_tool(start:float,end:float) -> float:
    """tools performs the percentage calculation and returns the result.
        args : start: float, end: float
        returns: float 
        """
    if start == 0:
        return 0.0
    return ((end - start) / start) * 100
    
DataAnalysisAgent = AssistantAgent(
    name = 'data_analyst_agent',
    description = "You are a great data analysis agent who solves the task.",
    model_client=model_client,
    system_message="""You are a data analysis agent,
    ,Given the data you have assigned.You should analyse the data 
    and provide the results using the tools provided.
    if you have not seen the data, you can ask for it.""",
    tools=[percentage_calculation_tool],
)

