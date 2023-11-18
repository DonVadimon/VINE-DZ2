import json
from django.db import connection
from typing_extensions import Unpack
from typing import TypedDict, Optional

from app.utils import dictEntries, filterDict, formatSQLValue, listJoin


class CreateFaceInfoDto(TypedDict):
    gender: str
    age: str
    leftEyeColor: str
    rightEyeColor: str
    hairColor: str
    skinColor: str


class PatchFaceInfoDto(TypedDict):
    gender: Optional[str]
    age: Optional[str]
    leftEyeColor: Optional[str]
    rightEyeColor: Optional[str]
    hairColor: Optional[str]
    skinColor: Optional[str]


class FaceInfoSelection(TypedDict):
    id: int
    gender: str
    age: str
    leftEyeColor: str
    rightEyeColor: str
    hairColor: str
    skinColor: str


class FaceInfoConverter:

    @staticmethod
    def tuppleToDict(t: tuple) -> FaceInfoSelection:
        id, gender, age, leftEyeColor, rightEyeColor, hairColor, skinColor = t

        return {
            'id': id,
            'gender': gender,
            'age': age,
            'leftEyeColor': leftEyeColor,
            'rightEyeColor': rightEyeColor,
            'hairColor': hairColor,
            'skinColor': skinColor,
        }

    @staticmethod
    def dictToJSON(d: FaceInfoSelection):
        return json.dumps(d)


class FaceInfoGateway:
    @staticmethod
    def getFaceInfo(id: int) -> FaceInfoSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, gender, age, leftEyeColor, rightEyeColor, hairColor, skinColor 
                FROM app_faceinfo
                WHERE id = %(id)s;
                """, {'id': id})

            info = cursor.fetchone()

            if info == None:
                raise RuntimeError('FaceInfo doesnt exist')

            return FaceInfoConverter.tuppleToDict(info)

    @staticmethod
    def createFaceInfo(**kwargs: Unpack[CreateFaceInfoDto]) -> FaceInfoSelection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO app_faceinfo 
                (gender, age, leftEyeColor, rightEyeColor, hairColor, skinColor) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, gender, age, leftEyeColor, rightEyeColor, hairColor, skinColor;
                """, (
                    kwargs.get('gender'),
                    kwargs.get('age'),
                    kwargs.get('leftEyeColor'),
                    kwargs.get('rightEyeColor'),
                    kwargs.get('hairColor'),
                    kwargs.get('skinColor')
                ))
            connection.commit()

            info = cursor.fetchone()

            if info == None:
                raise RuntimeError('Cannot find created FaceInfo')

            return FaceInfoConverter.tuppleToDict(info)

    @staticmethod
    def patchFaceInfo(id: int, patch: PatchFaceInfoDto) -> FaceInfoSelection:
        with connection.cursor() as cursor:

            filteredPatch = filterDict(patch)  # type: ignore

            cursor.execute(f"""
                UPDATE app_faceinfo SET
                {listJoin(list(map(
                    lambda pair: f"{pair[0]} = {formatSQLValue(pair[1])}", dictEntries(filteredPatch))), ', ')}
                WHERE id = {id}
                RETURNING id, gender, age, leftEyeColor, rightEyeColor, hairColor, skinColor;
                """)

            info = cursor.fetchone()

            if info == None:
                raise RuntimeError('FaceInfo doesnt exist')

            return FaceInfoConverter.tuppleToDict(info)

    @staticmethod
    def deleteFaceInfo(id: int) -> FaceInfoSelection:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM app_faceinfo
                WHERE id = %(id)s
                RETURNING id, gender, age, leftEyeColor, rightEyeColor, hairColor, skinColor;
            """, {'id': id})

            info = cursor.fetchone()

            if info == None:
                raise RuntimeError('FaceInfo doesnt exist')

            return FaceInfoConverter.tuppleToDict(info)
