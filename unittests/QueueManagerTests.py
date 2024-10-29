import unittest
from QueueManager import QueueManager


class QueuemMnagerTests(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.manager = QueueManager()

    def test_action(self):
        pass
