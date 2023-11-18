import json
from django.db import connection
from typing_extensions import Unpack
from typing import TypedDict, Optional

from app.utils import dictEntries, filterDict, formatSQLValue, listJoin


class CreateUserDto(TypedDict):
    username: str
    name: str
    email: str


class PatchUserDto(TypedDict):
    username: Optional[str]
    name: Optional[str]
    email: Optional[str]
    faceInfo_id: Optional[int]


class UserSelection(TypedDict):
    id: int
    username: str
    name: str
    email: str
    faceInfo_id: int


class UserConverter:

    @staticmethod
    def tuppleToDict(t: tuple) -> UserSelection:
        id, username, name, email, faceInfo_id = t

        return {
            'id': id,
            'username': username,
            'name': name,
            'email': email,
            'faceInfo_id': faceInfo_id,
        }

    @staticmethod
    def dictToJSON(d: UserSelection):
        return json.dumps(d)


class UserGateway:
    @staticmethod
    def getUser(id: int) -> UserSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, username, name, email, faceInfo_id 
                FROM app_user
                WHERE id = %(id)s;
                """, {'id': id})

            user = cursor.fetchone()

            if user == None:
                raise RuntimeError('User doesnt exist')

            return UserConverter.tuppleToDict(user)

    @staticmethod
    def getAllUsers() -> list[UserSelection]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, username, name, email, faceInfo_id 
                from app_user;
                """)
            users = cursor.fetchall()

            return list(map(lambda user: UserConverter.tuppleToDict(user), users))

    @staticmethod
    def createUser(**kwargs: Unpack[CreateUserDto]) -> UserSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO app_user 
                (username, name, email) VALUES (%s, %s, %s)
                RETURNING id, username, name, email, faceInfo_id;
                """, (kwargs.get('username'), kwargs.get('name'), kwargs.get('email')))
            connection.commit()

            user = cursor.fetchone()

            if user == None:
                raise RuntimeError('Cannot find created user')

            return UserConverter.tuppleToDict(user)

    @staticmethod
    def patchUser(id: int, patch: PatchUserDto) -> UserSelection:
        with connection.cursor() as cursor:
            filteredPatch = filterDict(patch)  # type: ignore

            cursor.execute(f"""
                UPDATE app_user SET
                {listJoin(list(map(
                    lambda pair: f"{pair[0]} = {formatSQLValue(pair[1])}", dictEntries(filteredPatch))), ', ')}
                WHERE id = {id}
                RETURNING id, username, name, email, faceInfo_id;
                """)

            user = cursor.fetchone()

            if user == None:
                raise RuntimeError('User doesnt exist')

            return UserConverter.tuppleToDict(user)

    @staticmethod
    def deleteUser(id: int) -> UserSelection:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM app_user
                WHERE id = %(id)s
                RETURNING id, username, name, email, faceInfo_id;
            """, {'id': id})

            user = cursor.fetchone()

            if user == None:
                raise RuntimeError('User doesnt exist')

            return UserConverter.tuppleToDict(user)
