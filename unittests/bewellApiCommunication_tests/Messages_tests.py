import unittest
from BewellApiCommunication.Messages import Messages
from BewellApiCommunication.Models2 import *
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import requests


class Messages_tests(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self):
        self.messages = Messages()

    @patch("requests.get")
    def test_get_most_recent_message_success(self, mock_get):
        # Mock the response data
        mock_response_data = [
            {
                "created_timestamp": datetime.timestamp(
                    datetime.now() - timedelta(days=2)
                ),
                "message": "Old message",
            },
            {
                "created_timestamp": datetime.timestamp(datetime.now()),
                "message": "Recent message",
            },
        ]
        mock_get.return_value = Mock(
            status_code=200, json=Mock(return_value=mock_response_data)
        )
        most_recent_message = self.messages.getMostRecentMessage()

        self.assertIsInstance(most_recent_message, MessageGet)
        self.assertEqual(most_recent_message.message, "Recent message")
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_get_most_recent_message_failure(self, mock_get):
        mock_get.return_value = Mock(status_code=404)

        with self.assertRaises(requests.exceptions.HTTPError):
            self.messages.getMostRecentMessage()

    @patch("requests.post")
    def test_post_new_message_success(self, mock_post):
        # Mock the response data for post
        mock_response_data = {"message_id": "12345"}
        mock_post.return_value = Mock(
            ok=True, json=Mock(return_value=mock_response_data)
        )

        message_to_post = MessagePost(content="Hello World")  # Adjust as necessary
        message_id = self.messages.PostNewMessage(message_to_post)

        self.assertEqual(message_id, "12345")
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_post_new_message_failure(self, mock_post):
        mock_post.return_value = Mock(ok=False, status_code=400)

        message_to_post = MessagePost(content="Hello World")  # Adjust as necessary

        with self.assertRaises(requests.exceptions.HTTPError):
            self.messages.PostNewMessage(message_to_post)
