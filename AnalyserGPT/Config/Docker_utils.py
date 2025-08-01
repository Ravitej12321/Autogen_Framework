from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from Constants import *
def GetDockerCommandLineExecutor():
    docker = DockerCommandLineCodeExecutor(
        work_dir = WORKDIR,
        timeout = TIMEOUT_DOCKER
    )
    return docker

async def startDockerContainer(docker):
    print("Docker Container Started......")
    await docker.start()
async def stopDockerContainer(docker):
    print("Docker Container Stopped......")
    await docker.stop()