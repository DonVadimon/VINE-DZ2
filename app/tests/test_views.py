from django.test import RequestFactory, TestCase
from unittest.mock import patch

from app.views import getUser, getUserChats
from app.tests.fixtures import SINGLE_USER_SELECTION_FIXTURE, SINGLE_CHAT_SELECTION_FIXTURE


class TestUserViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('app.user.gateway.UserGateway.getUser')
    def test_get_user(self, mock_gateway):
        mock_gateway.return_value = SINGLE_USER_SELECTION_FIXTURE
        request = self.factory.get("/user/1")
        response = getUser(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'chats': [],
                'faceInfo': None,
                'faceInfo_id': None,
                'id': SINGLE_USER_SELECTION_FIXTURE['id'],
                'email': SINGLE_USER_SELECTION_FIXTURE['email'],
                'name': SINGLE_USER_SELECTION_FIXTURE['name'],
                'username': SINGLE_USER_SELECTION_FIXTURE['username'],
            }
        )

    def test_get_user_400(self):
        request = self.factory.get("/user/not_int")
        response = getUser(request, None)  # type: ignore
        self.assertEqual(response.status_code, 400)


class TestChatViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('app.user.gateway.UserGateway.getUser')
    @patch('app.chat.gateway.ChatGateway.getUserChats')
    @patch('app.chat.gateway.ChatGateway.getChat')
    def test_get_user_chats(self, get_chat_mock, get_chats_mock, get_user_mock):
        get_chat_mock.return_value = SINGLE_CHAT_SELECTION_FIXTURE
        get_user_mock.return_value = SINGLE_USER_SELECTION_FIXTURE
        get_chats_mock.return_value = [SINGLE_CHAT_SELECTION_FIXTURE]
        request = self.factory.get('user/chats/1')
        response = getUserChats(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'chats': [{
                    'id': SINGLE_CHAT_SELECTION_FIXTURE['id'],
                    'chatType': SINGLE_CHAT_SELECTION_FIXTURE['chatType'],
                    'description': SINGLE_CHAT_SELECTION_FIXTURE['description'],
                    'name': SINGLE_CHAT_SELECTION_FIXTURE['name'],
                    'messages': []
                }],
            }
        )
