import json
from django.db import connection
from typing_extensions import Unpack
from typing import TypedDict, Optional

from app.utils import dictEntries, filterDict, formatSQLValue, listJoin


class CreateChatDto(TypedDict):
    chatType: str
    name: str
    description: str


class PatchChatDto(TypedDict):
    chatType: Optional[str]
    name: Optional[str]
    description: Optional[str]


class ChatSelection(TypedDict):
    id: int
    chatType: str
    name: str
    description: str


class ChatConverter:

    @staticmethod
    def tuppleToDict(t: tuple) -> ChatSelection:
        id, chatType, name, description = t

        return {
            'id': id,
            'chatType': chatType,
            'description': description,
            'name': name,
        }

    @staticmethod
    def dictToJSON(d: ChatSelection):
        return json.dumps(d)


class ChatGateway:
    @staticmethod
    def getChat(id: int) -> ChatSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, chatType, name, description
                FROM app_chat
                WHERE id = %(id)s;
                """, {'id': id})

            chat = cursor.fetchone()

            if chat == None:
                raise RuntimeError('Chat doesnt exist')

            return ChatConverter.tuppleToDict(chat)

    @staticmethod
    def getAllChats() -> list[ChatSelection]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, chatType, name, description
                FROM app_chat;
                """)
            chats = cursor.fetchall()

            return list(map(lambda chat: ChatConverter.tuppleToDict(chat), chats))

    @staticmethod
    def createChat(**kwargs: Unpack[CreateChatDto]) -> ChatSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO app_chat 
                (chatType, name, description) VALUES (%s, %s, %s)
                RETURNING id, chatType, name, description;
                """, (kwargs.get('chatType'), kwargs.get('name'), kwargs.get('description')))
            connection.commit()

            chat = cursor.fetchone()

            if chat == None:
                raise RuntimeError('Cannot find created chat')

            return ChatConverter.tuppleToDict(chat)

    @staticmethod
    def patchChat(id: int, patch: PatchChatDto) -> ChatSelection:
        with connection.cursor() as cursor:

            filteredPatch = filterDict(patch)  # type: ignore

            cursor.execute(f"""
                UPDATE app_chat SET
                {listJoin(list(map(
                    lambda pair: f"{pair[0]} = {formatSQLValue(pair[1])}", dictEntries(filteredPatch))), ', ')}
                WHERE id = {id}
                RETURNING id, chatType, name, description;
                """)

            chat = cursor.fetchone()

            if chat == None:
                raise RuntimeError('Chat doesnt exist')

            return ChatConverter.tuppleToDict(chat)

    @staticmethod
    def deleteChat(id: int) -> ChatSelection:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM app_chat
                WHERE id = %(id)s
                RETURNING id, chatType, name, description;
            """, {'id': id})

            chat = cursor.fetchone()

            if chat == None:
                raise RuntimeError('Chat doesnt exist')

            return ChatConverter.tuppleToDict(chat)

    @staticmethod
    def checkIsMember(chatId: int, userId: int) -> bool:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id
                FROM app_user_chats
                WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s;
            """, {'user_id': userId, 'chat_id': chatId})

            chat = cursor.fetchone()

            return chat != None

    @staticmethod
    def joinChat(chatId: int, userId: int) -> bool:
        if ChatGateway.checkIsMember(chatId=chatId, userId=userId):
            raise RuntimeError('Already member')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO app_user_chats
                (user_id, chat_id) VALUES (%(user_id)s, %(chat_id)s);
            """, {'user_id': userId, 'chat_id': chatId})

        return True

    @staticmethod
    def leaveChat(chatId: int, userId: int) -> bool:
        if not ChatGateway.checkIsMember(chatId=chatId, userId=userId):
            raise RuntimeError('Not a member')

        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM app_user_chats
                WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s;
            """, {'user_id': userId, 'chat_id': chatId})

        return True

    @staticmethod
    def getUserChats(userId: int) -> list[ChatSelection]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.chatType, c.name, c.description
                FROM app_chat AS c
                INNER JOIN app_user_chats AS r
                ON
                    c.id = r.chat_id
                INNER JOIN app_user AS u
                ON
                    u.id = r.user_id
                WHERE u.id = %(user_id)s;
            """, {'user_id': userId})

            chats = cursor.fetchall()

            return list(map(lambda chat: ChatConverter.tuppleToDict(chat), chats))
