from typing import Optional

from app.face.gateway import CreateFaceInfoDto, FaceInfoGateway
from app.chat.gateway import ChatGateway, CreateChatDto, PatchChatDto
from app.message.gateway import ChatMessageGateway, CreateMessageDto
from app.user.gateway import CreateUserDto, PatchUserDto, UserGateway
from app.utils import filterDict


class ChatMessageModel:
    id: int = None  # type: ignore
    content: str = None  # type: ignore
    author_id: int = None  # type: ignore
    chat_id: int = None  # type: ignore

    def __init__(self, **kwargs):

        dto: Optional[CreateMessageDto] = kwargs.get('dto')
        if dto is not None:
            self.author_id = dto['author_id']
            self.chat_id = dto['chat_id']
            self.content = dto['content']

        id: Optional[int] = kwargs.get('id')
        if id is not None:
            record = ChatMessageGateway.getMessage(id=id)
            self.id = record['id']
            self.author_id = record['author_id']
            self.chat_id = record['chat_id']
            self.content = record['content']

    def getChat(self):
        return ChatModel(id=self.chat_id)

    def getAuthor(self):
        return UserModel(id=self.author_id)

    def create(self):
        record = ChatMessageGateway.createMessage(
            chat_id=self.chat_id, author_id=self.author_id, content=self.content)
        self.id = record['id']
        self.content = record['content']
        self.author_id = record['author_id']
        self.chat_id = record['chat_id']

        return self

    def patch(self):
        ChatMessageGateway.patchMessage(id=self.id, patch={
            'content': self.content
        })

        return self

    def toDict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author_id': self.author_id,
            'chat_id': self.chat_id,
        }


class ChatModel:
    id: int = None  # type: ignore
    chatType: str = None  # type: ignore
    name: str = None  # type: ignore
    description: str = None  # type: ignore
    messages: list[ChatMessageModel] = None  # type: ignore

    def __init__(self, **kwargs):

        dto: Optional[CreateChatDto] = kwargs.get('dto')
        if dto is not None:
            self.chatType = dto['chatType']
            self.name = dto['name']
            self.description = dto['description']

        id: Optional[int] = kwargs.get('id')
        if id is not None:
            record = ChatGateway.getChat(id=id)
            self.id = record['id']
            self.patchInstance(patch={
                'chatType': record['chatType'],
                'name': record['name'],
                'description': record['description'],
            })
            self.messages = list(map(lambda x: ChatMessageModel(
                id=x['id']), ChatMessageGateway.getChatMessages(chatId=self.id)))

    def create(self):
        record = ChatGateway.createChat(
            chatType=self.chatType,
            description=self.description,
            name=self.name
        )
        self.id = record['id']
        self.patchInstance(patch=record)

        return self

    def patch(self):
        ChatGateway.patchChat(id=self.id, patch={
            'chatType': self.chatType,
            'name': self.name,
            'description': self.description,
        })

        return self

    def save(self):
        if self.id != None:
            return self.patch()
        return self.create()

    def patchInstance(self, patch: PatchChatDto):
        filteredPatch = filterDict(d=patch)  # type: ignore
        self.id = filteredPatch['id'] if 'id' in filteredPatch else self.id
        self.chatType = filteredPatch['chatType'] if 'chatType' in filteredPatch else self.chatType
        self.name = filteredPatch['name'] if 'name' in filteredPatch else self.name
        self.description = filteredPatch['description'] if 'description' in filteredPatch else self.description

    def toDict(self):
        return {
            'id': self.id,
            'chatType': self.chatType,
            'name': self.name,
            'description': self.description,
            'messages': list(map(lambda x: x.toDict(), self.messages)) if self.messages != None else list()
        }


class FaceInfoModel:
    id: int = None  # type: ignore
    gender: str = None  # type: ignore
    age: str = None  # type: ignore
    leftEyeColor: str = None  # type: ignore
    rightEyeColor: str = None  # type: ignore
    hairColor: str = None  # type: ignore
    skinColor: str = None  # type: ignore

    def __init__(self, **kwargs):

        dto: Optional[CreateFaceInfoDto] = kwargs.get('dto')
        if dto is not None:
            self.gender = dto['gender']
            self.age = dto['age']
            self.leftEyeColor = dto['leftEyeColor']
            self.rightEyeColor = dto['rightEyeColor']
            self.hairColor = dto['hairColor']
            self.skinColor = dto['skinColor']

        id: Optional[int] = kwargs.get('id')
        if id is not None:
            record = FaceInfoGateway.getFaceInfo(id=id)
            self.id = record['id']
            self.gender = record['gender']
            self.age = record['age']
            self.leftEyeColor = record['leftEyeColor']
            self.rightEyeColor = record['rightEyeColor']
            self.hairColor = record['hairColor']
            self.skinColor = record['skinColor']

    def patchInstance(self, patch: PatchUserDto):
        filteredPatch = filterDict(d=patch)  # type: ignore

        self.id = filteredPatch['id'] if 'id' in filteredPatch else self.id
        self.gender = filteredPatch['gender'] if 'gender' in filteredPatch else self.gender
        self.age = filteredPatch['age'] if 'age' in filteredPatch else self.age
        self.leftEyeColor = filteredPatch['leftEyeColor'] if 'leftEyeColor' in filteredPatch else self.leftEyeColor
        self.rightEyeColor = filteredPatch['rightEyeColor'] if 'rightEyeColor' in filteredPatch else self.rightEyeColor
        self.hairColor = filteredPatch['hairColor'] if 'hairColor' in filteredPatch else self.hairColor
        self.skinColor = filteredPatch['skinColor'] if 'skinColor' in filteredPatch else self.skinColor

    def create(self):
        record = FaceInfoGateway.createFaceInfo(
            gender=self.gender,
            age=self.age,
            leftEyeColor=self.leftEyeColor,
            rightEyeColor=self.rightEyeColor,
            hairColor=self.hairColor,
            skinColor=self.skinColor,
        )
        self.id = record['id']
        self.gender = record['gender']
        self.age = record['age']
        self.leftEyeColor = record['leftEyeColor']
        self.rightEyeColor = record['rightEyeColor']
        self.hairColor = record['hairColor']
        self.skinColor = record['skinColor']

        return self

    def patch(self):
        FaceInfoGateway.patchFaceInfo(id=self.id, patch={
            'gender': self.gender,
            'age': self.age,
            'leftEyeColor': self.leftEyeColor,
            'rightEyeColor': self.rightEyeColor,
            'hairColor': self.hairColor,
            'skinColor': self.skinColor,
        })

        return self

    def save(self):
        if self.id != None:
            return self.patch()
        return self.create()

    def toDict(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'age': self.age,
            'leftEyeColor': self.leftEyeColor,
            'rightEyeColor': self.rightEyeColor,
            'hairColor': self.hairColor,
            'skinColor': self.skinColor,
        }


class UserModel:
    id: int = None  # type: ignore
    username: str = None  # type: ignore
    name: str = None  # type: ignore
    email: str = None  # type: ignore
    faceInfo_id: int = None  # type: ignore
    faceInfo: FaceInfoModel = None  # type: ignore
    chats: list[ChatModel] = None  # type: ignore

    def __init__(self, **kwargs):

        dto: Optional[CreateUserDto] = kwargs.get('dto')
        if dto != None:
            self.name = dto['name']
            self.username = dto['username']
            self.email = dto['email']

        id: Optional[int] = kwargs.get('id')
        if id != None:
            record = UserGateway.getUser(id=id)
            self.id = record['id']
            self.patchInstance(patch={
                'name': record['name'],
                'username': record['username'],
                'email': record['email'],
                'faceInfo_id': record['faceInfo_id'],
            })
            self.faceInfo = FaceInfoModel(id=record['faceInfo_id'])
            self.chats = list(map(lambda x: ChatModel(
                id=x['id']), ChatGateway.getUserChats(userId=self.id)))

    def patchInstance(self, patch: PatchUserDto):
        filteredPatch = filterDict(d=patch)  # type: ignore
        self.name = filteredPatch['name'] if 'name' in filteredPatch else self.name
        self.username = filteredPatch['username'] if 'username' in filteredPatch else self.username
        self.email = filteredPatch['email'] if 'email' in filteredPatch else self.email
        self.faceInfo_id = filteredPatch['faceInfo_id'] if 'faceInfo_id' in filteredPatch else self.faceInfo_id
        self.id = filteredPatch['id'] if 'id' in filteredPatch else self.id

    def create(self):
        record = UserGateway.createUser(
            username=self.username, name=self.name, email=self.email)
        self.id = record['id']
        self.username = record['username']
        self.name = record['name']
        self.email = record['email']
        self.faceInfo_id = record['faceInfo_id']

        return self

    def patch(self):
        UserGateway.patchUser(id=self.id, patch={
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'faceInfo_id': self.faceInfo_id,
        })

        return self

    def save(self):
        if self.id != None:
            return self.patch()
        return self.create()

    def delete(self):
        patch = UserGateway.deleteUser(id=self.id)
        self.patchInstance(patch=patch)
        return self

    def joinChat(self, chat: ChatModel):
        ChatGateway.joinChat(chatId=chat.id, userId=self.id)
        self.chats = self.chats if self.chats != None else list()
        self.chats.append(chat)

    def leaveChat(self, chat: ChatModel):
        ChatGateway.leaveChat(chatId=chat.id, userId=self.id)
        self.chats = self.chats if self.chats != None else list()
        self.chats = [c for c in self.chats if c.id != chat.id]

    def writeMessage(self, chat: ChatModel, content: str):
        return ChatMessageModel(dto={
            'author_id': self.id,
            'chat_id': chat.id,
            'content': content
        }).create()

    def addFaceInfo(self, faceInfo: FaceInfoModel):
        if self.faceInfo_id != None:
            raise RuntimeError('FaceInfo already exist in UserModel')
        self.faceInfo = faceInfo
        self.faceInfo_id = faceInfo.id
        return self.save()

    def removeFaceInfo(self):
        if self.faceInfo_id == None:
            raise RuntimeError('No face info in UserModel')

        # FaceInfoGateway.deleteFaceInfo(id=self.faceInfo_id)
        self.faceInfo = None  # type: ignore
        self.faceInfo_id = None  # type: ignore
        return self.save()

    @staticmethod
    def getAllUsers():
        return list(map(lambda x: UserModel(id=x['id']), UserGateway.getAllUsers()))

    def toDict(self):

        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'faceInfo_id': self.faceInfo_id,
            'faceInfo': None if self.faceInfo == None or self.faceInfo.id == None else self.faceInfo.toDict(),
            'chats': [] if self.chats == None else list(map(lambda chat: chat.toDict(), self.chats))
        }
