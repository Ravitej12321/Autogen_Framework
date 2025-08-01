from autogen_agentchat.agents import AssistantAgent
from Agents.prompts.DataAnalyzerPrompt import DataAnalyzer_prompt

from Config.Constants import model
def get_data_analyser_agent(model_client):
    analyzer_agent = AssistantAgent(
        name = "Data_Analyzer_agent",
        description = DataAnalyzer_prompt,
        system_message= DataAnalyzer_prompt,
        model_client= model_client
    )
    return analyzer_agent
