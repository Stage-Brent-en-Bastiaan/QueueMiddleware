import unittest
from MiddleWare.QueueManager import QueueManager
import unittest
from unittest.mock import MagicMock, patch, call


class QueueManagerTests(unittest.TestCase):
    @patch("your_module.SqlServerConnection")
    @patch("your_module.LoggingMessage")
    def test_action_connection_failure(
        self, MockLoggingMessage, MockSqlServerConnection
    ):
        # Setup
        mock_log_factory = MagicMock()
        instance = QueueManager(mock_log_factory)

        # Simulate connection failure
        MockSqlServerConnection.side_effect = Exception("Connection error")

        # Call the action method
        instance.action()

        # Assertions
        mock_log_factory.Log.assert_called_once_with(
            loggingMessage=MockLoggingMessage(
                "er kon geen verbinding gemaakt worden met de database",
                unittest.mock.ANY,  # You can specify more detailed checks if needed
            )
        )
        instance.standBy.assert_called_once()

    @patch("your_module.SqlServerConnection")
    def test_action_no_task_found(self, MockSqlServerConnection):
        # Setup
        mock_log_factory = MagicMock()
        instance = QueueManager(mock_log_factory)
        mock_connection_instance = MockSqlServerConnection.return_value
        mock_connection_instance.getNextQueueItem.return_value = None

        # Call the action method
        instance.action()

        # Assertions
        mock_log_factory.Log.assert_called_once()
        instance.standBy.assert_called_once()

    @patch("your_module.SqlServerConnection")
    def test_action_with_task(self, MockSqlServerConnection):
        # Setup
        mock_log_factory = MagicMock()
        instance = QueueManager(mock_log_factory)
        mock_connection_instance = MockSqlServerConnection.return_value
        mock_task = MagicMock()
        mock_connection_instance.getNextQueueItem.return_value = mock_task

        # Call the action method
        instance.action()

        # Assertions
        instance.activate.assert_called_once()
        instance.handleTask.assert_called_once_with(mock_task)
