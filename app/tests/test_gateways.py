from unittest import TestCase
from unittest.mock import patch
from app.chat.gateway import ChatGateway
from app.tests.fixtures import SINGLE_CHAT_SELECTION_FIXTURE_TUPPLE, SINGLE_CHAT_SELECTION_FIXTURE


class TestChatGateway(TestCase):
    @patch('django.db.connection.cursor')
    def test_get_chat(self, cursor_mock):
        cursor_mock.return_value.__enter__.return_value.fetchone.return_value = SINGLE_CHAT_SELECTION_FIXTURE_TUPPLE
        chat = ChatGateway.getChat(1)
        self.assertDictEqual(chat, SINGLE_CHAT_SELECTION_FIXTURE)
