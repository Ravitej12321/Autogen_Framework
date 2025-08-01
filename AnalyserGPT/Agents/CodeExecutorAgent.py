from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_core import CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
# docker = DockerCommandLineCodeExecutor(
#     work_dir='temp',
#     timeout=120
# )
def code_executor(docker):
    agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker

    )
    return agent


async def main():
    docker = DockerCommandLineCodeExecutor(
    work_dir='temp',
    timeout=120
)
    await docker.start()
    code_executor_agent = code_executor(docker)

    task = TextMessage(source='User',content="""Here is the python code which you have to run
```python
print("Code Executor Agent is working")
```
"""   )
    try:
        result = await code_executor_agent.on_messages(
            messages=[task],
            cancellation_token=CancellationToken()

        )
        print("result is ",result)
        print("result content is :",result[-1].content)
    except Exception as e:
        print("Exception Occured at",e)
    finally:
        await docker.stop()
if __name__ == "__main__":  
    asyncio.run(main())