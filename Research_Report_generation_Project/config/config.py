


from autogen_ext.models.openai import OpenAIChatCompletionClient

MODEL = "gemini-2.0-flash"
GEMINI_API_KEY = "AIzaSyDsIcBSy9KNdsJrRTbd_5v4yA6bQXQa6HM"

model_client  = OpenAIChatCompletionClient(model=MODEL,api_key = GEMINI_API_KEY)

