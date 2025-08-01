from autogen_agentchat.teams import Swarm
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination,HandoffTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os,asyncio

load_dotenv()
gemini_api_key = os.getenv("GEMINI_KEY")

model_client  = OpenAIChatCompletionClient(model="gemini-2.0-flash",api_key=gemini_api_key)

# Travel_Agent
travel_agent = AssistantAgent(
            name = "travel_agent",
            model_client=model_client,
            description = """You are a travel agent helps user queries to solve the travelling related queries and helps users
            to plan trips via flights """,
            handoffs=["flight_refunder_agent","user"],
            system_message="""You are a travel agent. The flight_refunder_agent is in charge of refunding flights.
            if you need information from the user, you must first send your message then you can handoff to the user.
            use TERMINATE when the travel planning is done."""

)
def flight_refund_tool(flight_id:str)->str:
    """
    this function used to validates the flight ticket is exact PNR number or Not using the input.
    args:
        flight_id: Input string of alpha numeric flight id.
    return :
        string: whether the return ticket or not."""
    return f"flight {flight_id} has been refunded."
# Flight Refunder agent
refunder_agent = AssistantAgent(
    name = "flight_refunder_agent",
    model_client = model_client,
    handoffs=["travel_agent","user"],
    tools= [flight_refund_tool],
    system_message= """ You are a flight refunder agent that specialized in refunding flights. 
    You only need the flight PNR  number to refund the flight tickets. 
    You have the ability to refund the tickets by using the flight_refund tool.
    When the transaction complete finally return to travel agent.
    """
)

    
termination_condition = TextMentionTermination("TERMINATE") |HandoffTermination("user")
travelling_team = Swarm(
    participants=[travel_agent,refunder_agent],
    termination_condition=termination_condition   
)

task = "Cancel my Flight Air India Airlines kolkata to mumbai PNR 123ABC immediately."
async def main()-> None:
    result = await Console(travelling_team.run_stream(task=task))
    last_message = result.messages[-1]
    while isinstance(last_message,HandoffMessage) and last_message.target =='user':
        user_message = input("User : ")
        task_result = await Console(
        travelling_team.run_stream(task=HandoffMessage(source = 'user',
        target  = last_message.source,content = user_message)))
        last_message = task_result.messages[-1]
        print(last_message)




    
if __name__ == "__main__":
    asyncio.run(main())
    
