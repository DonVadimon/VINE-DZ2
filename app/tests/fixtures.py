from app.message.gateway import MessageSelection
from app.chat.gateway import ChatSelection
from app.user.gateway import UserSelection
from app.face.gateway import FaceInfoSelection


SINGLE_USER_SELECTION_FIXTURE: UserSelection = {
    'id': 1,
    'email': 'email@mail.ru',
    'name': 'Vasya Pupkin',
    'username': 'vasyan228',
    'faceInfo_id': None  # type: ignore
}

# id, username, name, email, faceInfo_id
SINGLE_USER_SELECTION_FIXTURE_TUPPLE: tuple = SINGLE_USER_SELECTION_FIXTURE['id'], SINGLE_USER_SELECTION_FIXTURE[
    'username'], SINGLE_USER_SELECTION_FIXTURE['name'], SINGLE_USER_SELECTION_FIXTURE['email'], SINGLE_USER_SELECTION_FIXTURE['faceInfo_id']

SINGLE_MESSAGE_SELECTION_FIXTURE: MessageSelection = {
    'id': 1,
    'chat_id': 1,
    'author_id': 1,
    'content': 'Hello world!'
}

# id, content, author_id, chat_id
SINGLE_MESSAGE_SELECTION_FIXTURE_TUPPLE: tuple = SINGLE_MESSAGE_SELECTION_FIXTURE['id'], SINGLE_MESSAGE_SELECTION_FIXTURE[
    'content'], SINGLE_MESSAGE_SELECTION_FIXTURE['author_id'], SINGLE_MESSAGE_SELECTION_FIXTURE['chat_id']

SINGLE_CHAT_SELECTION_FIXTURE: ChatSelection = {
    'id': 1,
    'chatType': 'PRIVATE',
    'description': 'wow chat',
    'name': 'Cool Chat'
}

# id, chatType, name, description
SINGLE_CHAT_SELECTION_FIXTURE_TUPPLE: tuple = SINGLE_CHAT_SELECTION_FIXTURE['id'], SINGLE_CHAT_SELECTION_FIXTURE[
    'chatType'], SINGLE_CHAT_SELECTION_FIXTURE['name'], SINGLE_CHAT_SELECTION_FIXTURE['description']


SINGLE_FACEINFO_SELECTION_FIXTURE: FaceInfoSelection = {
    'id': 1,
    'age': '22',
    'gender': 'MALE',
    'hairColor': 'brown',
    'leftEyeColor': 'blue',
    'rightEyeColor': 'blue',
    'skinColor': 'white'
}

# id, gender, age, leftEyeColor, rightEyeColor, hairColor, skinColor
SINGLE_FACEINFO_SELECTION_FIXTURE_TUPPLE: tuple = SINGLE_FACEINFO_SELECTION_FIXTURE['id'], SINGLE_FACEINFO_SELECTION_FIXTURE['gender'], SINGLE_FACEINFO_SELECTION_FIXTURE[
    'age'], SINGLE_FACEINFO_SELECTION_FIXTURE['leftEyeColor'], SINGLE_FACEINFO_SELECTION_FIXTURE['rightEyeColor'], SINGLE_FACEINFO_SELECTION_FIXTURE['hairColor'], SINGLE_FACEINFO_SELECTION_FIXTURE['skinColor']
