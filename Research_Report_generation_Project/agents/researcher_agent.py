# from config.config import model_client
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.tools import DuckDuckGoSearchRun
import asyncio


from autogen_ext.models.openai import OpenAIChatCompletionClient

MODEL = "gemini-2.0-flash"
GEMINI_API_KEY = "AIzaSyDsIcBSy9KNdsJrRTbd_5v4yA6bQXQa6HM"

model_client  = OpenAIChatCompletionClient(model=MODEL,api_key = GEMINI_API_KEY)



#### Researcher agent used to search the content from web and get the information for the searched topic 
# PlayWright Browser Toolkit
# Brave Search tool is enough for that



def duck_duck_search_tool(topic:str) -> str:
    print(topic)
    search = DuckDuckGoSearchRun()

    result = search.invoke(f"{topic}") 
    return result

researcher_agent = AssistantAgent(
        name  = "Research_agent",
        model_client=model_client,
        description= f"""A researcher agent able to retrieve topic as a task from researching all the topics using the langchain tools.""",
        system_message= """Imagine you are a great research scientist agent used to retrieve the information 
                        using the duck_duck_search_tool. Based on the information from the tool produce the result with a neat format
                        Instructions 
                        1. Input format to the tool is a string for searching about topic.
                          """,
        tools = [duck_duck_search_tool],


    )
async def main():
    topic  = "Treatment for Cancer"

    result = await researcher_agent.run(task = topic)
    print(result.messages[-1])

if __name__ == "__main__":
    # print(duck_duck_search_tool())
    asyncio.run(main())

