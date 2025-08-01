from autogen_agentchat.agents import CodeExecutorAgent,AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.base import TaskResult


async def main():
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_KEY")
    model_client = OpenAIChatCompletionClient(model="gemini-2.0-flash",api_key=gemini_api_key)
    docker =DockerCommandLineCodeExecutor(
        work_dir= '/tmp',
        timeout= 120

    )

    code_executor_agent = CodeExecutorAgent(
        name = "Code_Executor_agent",
        # max_retries_on_error=3,
        code_executor=docker
    )
    problem_solving_agent = AssistantAgent(
        name = 'Problem_solving_agent',
        model_client = model_client,
        description = "you are a DSA problem solving  agent",
        system_message='''You are an expert DSA problem solving agent with highest level of accuracy and efficiency 
        with incredible history of time complexity and space Complexity.You will be given a task and you should.
        1. Write a code to solve the task only in python.Your code should be only in python.
        at the begining of task specify the response for the plan to solve the task. 
        then you should code the code in code block.
        2.write atleast 3 testcases to execute in code executor agent.
        3.You should write the code in one code block and pass it  to the code executor agent to execute it.
        5.After validating the code output from code_executor_agent if code executed without any error.
        you have to say "STOP" to stop the conversation.'''
    )
    termination_condition = TextMentionTermination("STOP")
    round_robin_team = RoundRobinGroupChat(
        [problem_solving_agent,code_executor_agent],
        termination_condition=termination_condition,
        max_turns=5
    )
    task = '''write a code to swap two numbers'''
    await docker.start()
    try:
        # result = await code_executor_agent.on_messages(messages=[task],cancellation_token=CancellationToken())
        # print(result.chat_message)
        async for message in round_robin_team.run_stream(task = task):
            if isinstance(message,TextMessage):
                print('==='*30)
                print(message.source,":",message.content)
            if isinstance(message,TaskResult):
                print('==='*30) 
                print("Stop Reason: ",message.stop_reason)

    except:
        print("Code is not executed.....")
    finally:
        await docker.stop()

if __name__=="__main__":
    asyncio.run(main())
