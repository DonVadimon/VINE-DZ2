import json
from django.db import connection
from typing_extensions import Unpack
from typing import TypedDict, Optional

from app.utils import dictEntries, filterDict, formatSQLValue, listJoin


class CreateMessageDto(TypedDict):
    content: str
    author_id: int
    chat_id: int


class PatchMessageDto(TypedDict):
    content: Optional[str]


class MessageSelection(TypedDict):
    id: int
    content: str
    author_id: int
    chat_id: int


class MessageConverter:

    @staticmethod
    def tuppleToDict(t: tuple) -> MessageSelection:
        id, content, author_id, chat_id = t

        return {
            'id': id,
            'content': content,
            'author_id': author_id,
            'chat_id': chat_id,
        }

    @staticmethod
    def dictToJSON(d: MessageSelection):
        return json.dumps(d)


class ChatMessageGateway:
    @staticmethod
    def getMessage(id: int) -> MessageSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, content, author_id, chat_id
                FROM app_chatmessage
                WHERE id = %(id)s;
                """, {'id': id})

            msg = cursor.fetchone()

            if msg == None:
                raise RuntimeError('Message doesnt exist')

            return MessageConverter.tuppleToDict(msg)

    @staticmethod
    def getAllMessages() -> list[MessageSelection]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, content, author_id, chat_id 
                from app_chatmessage;
                """)
            msgs = cursor.fetchall()

            return list(map(lambda msg: MessageConverter.tuppleToDict(msg), msgs))

    @staticmethod
    def createMessage(**kwargs: Unpack[CreateMessageDto]) -> MessageSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO app_chatmessage 
                (content, author_id, chat_id) VALUES (%s, %s, %s)
                RETURNING id, content, author_id, chat_id;
                """, (kwargs.get('content'), kwargs.get('author_id'), kwargs.get('chat_id')))
            connection.commit()

            msg = cursor.fetchone()

            if msg == None:
                raise RuntimeError('Cannot find created message')

            return MessageConverter.tuppleToDict(msg)

    @staticmethod
    def patchMessage(id: int, patch: PatchMessageDto) -> MessageSelection:
        with connection.cursor() as cursor:

            filteredPatch = filterDict(patch)  # type: ignore

            cursor.execute(f"""
                UPDATE app_chatmessage SET
                {listJoin(list(map(
                    lambda pair: f"{pair[0]} = {formatSQLValue(pair[1])}", dictEntries(filteredPatch))), ', ')}
                WHERE id = {id}
                RETURNING id, content, author_id, chat_id;
                """)

            msg = cursor.fetchone()

            if msg == None:
                raise RuntimeError('Message doesnt exist')

            return MessageConverter.tuppleToDict(msg)

    @staticmethod
    def deleteMessage(id: int) -> MessageSelection:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM app_chatmessage
                WHERE id = %(id)s
                RETURNING id, content, author_id, chat_id;
            """, {'id': id})

            msg = cursor.fetchone()

            if msg == None:
                raise RuntimeError('Message doesnt exist')

            return MessageConverter.tuppleToDict(msg)

    @staticmethod
    def getChatMessages(chatId: int) -> list[MessageSelection]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, content, author_id, chat_id
                FROM app_chatmessage 
                WHERE chat_id = %(chat_id)s;
            """, {'chat_id': chatId})

            msgs = cursor.fetchall()

            return list(map(lambda msg: MessageConverter.tuppleToDict(msg), msgs))
