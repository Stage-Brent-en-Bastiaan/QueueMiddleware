import unittest
from .bewellApiCommunication_tests.Messages_tests import Messages_tests
from .bewellApiCommunication_tests.Patienten_tests import Patienten_tests


class TestManager:
    def __init__(self) -> None:
        pass

    def main(self):
        suite = unittest.TestSuite()

        suite.addTest(unittest.makeSuite(Messages_tests))
        suite.addTest(unittest.makeSuite(Patienten_tests))

        runner = unittest.TextTestRunner()
        runner.run(suite)
