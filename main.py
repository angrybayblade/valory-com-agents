import asyncio
import string
import random
import typing as T

words = (
    "hello",
    "sun",
    "world",
    "space",
    "moon",
    "crypto",
    "sky",
    "ocean",
    "universe",
    "huma"
)


class MessageBox:

    _messages: T.List[str]

    def __init__(self, idx: str):
        """
        Args: 
            idx : str 
        """
        self._idx = idx
        self._messages = []
        self._running = True

    async def listen(self,) -> None:
        while not len(self._messages):
            await asyncio.sleep(0.5)
        return self._messages.pop(0)

    async def write(self, message: str) -> None:
        self._messages.append(message)


class Agent:

    message_handler: T.Callable
    behaviour_handler: T.Callable

    _inbox: MessageBox
    _outbox: MessageBox
    _running = True

    def __init__(self, ):
        self._idx = "".join(
            random.choices(string.ascii_lowercase+string.digits, k=6))
        self._inbox = MessageBox(self._idx)

    @property
    def inbox(self,) -> MessageBox:
        return self._inbox

    @property
    def outbox(self,) -> MessageBox:
        return self._outbox

    def set_outbox(self, outbox: MessageBox) -> None:
        self._outbox = outbox

    def register_message_handler(self, handle: T.Callable) -> None:
        self.message_handler = handle

    def register_behaviour_handler(self, handle: T.Callable) -> None:
        self.behaviour_handler = handle

    async def message_handle_runner(self, ):
        while self._running:
            message = await self._inbox.listen()
            response = await self.message_handler(message, self)
            if response:
                await self.outbox.write(response)

    async def behaviour_handle_runner(self, ):
        while self._running:
            await self.behaviour_handler(self,)
            await asyncio.sleep(2)

    async def start(self, ):
        await asyncio.gather(
            self.message_handle_runner(),
            self.behaviour_handle_runner()
        )

    async def run(self, ):
        await self.start()

    def stop(self,):
        self._running = False


async def message_handler(message: str, agent: Agent):
    print("[recv] Agent({idx}) : {output}".format(
        idx=agent._idx, output=message.replace("hello", "")))
    return False


async def behaviour_handler(agent: Agent):
    message = random.choices(words, k=2)
    message = " ".join(message)
    await agent.outbox.write(message)


async def main():
    agent1 = Agent()
    agent2 = Agent()

    agent1.set_outbox(agent2._inbox)
    agent2.set_outbox(agent1._inbox)

    agent1.register_message_handler(message_handler)
    agent2.register_message_handler(message_handler)
    agent1.register_behaviour_handler(behaviour_handler)
    agent2.register_behaviour_handler(behaviour_handler)

    try:
        await asyncio.gather(
            agent1.run(),
            agent2.run()
        )
    except KeyboardInterrupt:
        agent1.stop()
        agent2.stop()
        exit()


if __name__ == "__main__":
    asyncio.run(main())