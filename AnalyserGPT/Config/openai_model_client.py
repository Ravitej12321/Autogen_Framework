from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def get_model_client(api_key):

    model_client = OpenAIChatCompletionClient(

    model="gpt-4o",
    api_key=api_key

    )
    return model_client 