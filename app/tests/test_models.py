from unittest import TestCase
from unittest.mock import patch
from app.domains import ChatMessageModel, ChatModel, UserModel, FaceInfoModel
from app.tests.fixtures import SINGLE_USER_SELECTION_FIXTURE, SINGLE_MESSAGE_SELECTION_FIXTURE, SINGLE_CHAT_SELECTION_FIXTURE, SINGLE_FACEINFO_SELECTION_FIXTURE


class TestChatMessageModel(TestCase):

    @patch('app.message.gateway.ChatMessageGateway.getMessage')
    def test_ctor_by_id(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_MESSAGE_SELECTION_FIXTURE
        instance = ChatMessageModel(id=1)
        gateway_get_mock.assert_called_once()
        self.assertEqual(instance.id, SINGLE_MESSAGE_SELECTION_FIXTURE['id'])
        self.assertEqual(instance.content,
                         SINGLE_MESSAGE_SELECTION_FIXTURE['content'])
        self.assertEqual(instance.author_id,
                         SINGLE_MESSAGE_SELECTION_FIXTURE['author_id'])
        self.assertEqual(instance.chat_id,
                         SINGLE_MESSAGE_SELECTION_FIXTURE['chat_id'])

    def test_ctor_by_dto(self):
        instance = ChatMessageModel(dto=SINGLE_MESSAGE_SELECTION_FIXTURE)
        self.assertEqual(instance.id, None)
        self.assertEqual(instance.content,
                         SINGLE_MESSAGE_SELECTION_FIXTURE['content'])
        self.assertEqual(instance.author_id,
                         SINGLE_MESSAGE_SELECTION_FIXTURE['author_id'])
        self.assertEqual(instance.chat_id,
                         SINGLE_MESSAGE_SELECTION_FIXTURE['chat_id'])

    @patch('app.message.gateway.ChatMessageGateway.createMessage')
    def test_create(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_MESSAGE_SELECTION_FIXTURE
        instance = ChatMessageModel(dto=SINGLE_MESSAGE_SELECTION_FIXTURE)
        instance.create()
        self.assertEqual(instance.id, SINGLE_MESSAGE_SELECTION_FIXTURE['id'])


class TestChatModel(TestCase):
    @patch('app.chat.gateway.ChatGateway.getChat')
    def test_ctor_by_id(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_CHAT_SELECTION_FIXTURE
        instance = ChatModel(id=1)
        gateway_get_mock.assert_called_once()
        self.assertEqual(instance.id, SINGLE_CHAT_SELECTION_FIXTURE['id'])
        self.assertEqual(instance.chatType,
                         SINGLE_CHAT_SELECTION_FIXTURE['chatType'])
        self.assertEqual(instance.description,
                         SINGLE_CHAT_SELECTION_FIXTURE['description'])
        self.assertEqual(instance.name, SINGLE_CHAT_SELECTION_FIXTURE['name'])

    def test_ctor_by_dto(self):
        instance = ChatModel(dto=SINGLE_CHAT_SELECTION_FIXTURE)
        self.assertEqual(instance.id, None)
        self.assertEqual(instance.chatType,
                         SINGLE_CHAT_SELECTION_FIXTURE['chatType'])
        self.assertEqual(instance.description,
                         SINGLE_CHAT_SELECTION_FIXTURE['description'])
        self.assertEqual(instance.name, SINGLE_CHAT_SELECTION_FIXTURE['name'])
        instance.save()

    @patch('app.chat.gateway.ChatGateway.createChat')
    def test_save(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_CHAT_SELECTION_FIXTURE
        instance = ChatModel(dto=SINGLE_CHAT_SELECTION_FIXTURE)
        instance.save()
        self.assertEqual(instance.id, SINGLE_CHAT_SELECTION_FIXTURE['id'])


class TestUserModel(TestCase):
    @patch('app.user.gateway.UserGateway.getUser')
    def test_ctor_by_id(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_USER_SELECTION_FIXTURE
        instance = UserModel(id=1)
        gateway_get_mock.assert_called_once()
        self.assertEqual(instance.id, SINGLE_USER_SELECTION_FIXTURE['id'])
        self.assertEqual(
            instance.email, SINGLE_USER_SELECTION_FIXTURE['email'])
        self.assertEqual(instance.name, SINGLE_USER_SELECTION_FIXTURE['name'])
        self.assertEqual(instance.username,
                         SINGLE_USER_SELECTION_FIXTURE['username'])
        self.assertEqual(instance.faceInfo_id,
                         SINGLE_USER_SELECTION_FIXTURE['faceInfo_id'])

    def test_ctor_by_dto(self):
        instance = UserModel(dto=SINGLE_USER_SELECTION_FIXTURE)
        self.assertEqual(instance.id, None)
        self.assertEqual(
            instance.email, SINGLE_USER_SELECTION_FIXTURE['email'])
        self.assertEqual(instance.name, SINGLE_USER_SELECTION_FIXTURE['name'])
        self.assertEqual(instance.username,
                         SINGLE_USER_SELECTION_FIXTURE['username'])
        self.assertEqual(instance.faceInfo_id, None)

    @patch('app.user.gateway.UserGateway.createUser')
    def test_save(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_USER_SELECTION_FIXTURE
        instance = UserModel(dto=SINGLE_USER_SELECTION_FIXTURE)
        instance.save()
        self.assertEqual(instance.id, SINGLE_USER_SELECTION_FIXTURE['id'])


class TestFaceInfoModel(TestCase):
    @patch('app.face.gateway.FaceInfoGateway.getFaceInfo')
    def test_ctor_by_id(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_FACEINFO_SELECTION_FIXTURE
        instance = FaceInfoModel(id=1)
        gateway_get_mock.assert_called_once()
        self.assertEqual(instance.id, SINGLE_FACEINFO_SELECTION_FIXTURE['id'])
        self.assertEqual(
            instance.age, SINGLE_FACEINFO_SELECTION_FIXTURE['age'])
        self.assertEqual(
            instance.gender, SINGLE_FACEINFO_SELECTION_FIXTURE['gender'])
        self.assertEqual(instance.hairColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['hairColor'])
        self.assertEqual(instance.leftEyeColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['leftEyeColor'])
        self.assertEqual(instance.rightEyeColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['rightEyeColor'])
        self.assertEqual(instance.skinColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['skinColor'])

    def test_ctor_by_dto(self):
        instance = FaceInfoModel(dto=SINGLE_FACEINFO_SELECTION_FIXTURE)
        self.assertEqual(instance.id, None)
        self.assertEqual(
            instance.age, SINGLE_FACEINFO_SELECTION_FIXTURE['age'])
        self.assertEqual(
            instance.gender, SINGLE_FACEINFO_SELECTION_FIXTURE['gender'])
        self.assertEqual(instance.hairColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['hairColor'])
        self.assertEqual(instance.leftEyeColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['leftEyeColor'])
        self.assertEqual(instance.rightEyeColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['rightEyeColor'])
        self.assertEqual(instance.skinColor,
                         SINGLE_FACEINFO_SELECTION_FIXTURE['skinColor'])

    @patch('app.face.gateway.FaceInfoGateway.createFaceInfo')
    def test_save(self, gateway_get_mock):
        gateway_get_mock.return_value = SINGLE_FACEINFO_SELECTION_FIXTURE
        instance = FaceInfoModel(dto=SINGLE_FACEINFO_SELECTION_FIXTURE)
        instance.save()
        self.assertEqual(instance.id, SINGLE_FACEINFO_SELECTION_FIXTURE['id'])
