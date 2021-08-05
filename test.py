import unittest

from main import Agent

class TestAgent(unittest.TestCase):

    def setUp(self) -> None:
        self.agent1 = Agent()
        self.agent2 = Agent()

        self.agent1.set_outbox(self.agent2.inbox)
        self.agent2.set_outbox(self.agent1.inbox)


    def test_agent_outbox(self,):
        self.assertEqual(self.agent1.inbox, self.agent2.outbox)
        self.assertEqual(self.agent1.outbox, self.agent2.inbox)


if __name__ == "__main__":
    unittest.main()