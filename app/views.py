import json
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound

from app.domains import ChatModel, FaceInfoModel, UserModel


def getJSONBody(request: HttpRequest):
    body_unicode = request.body.decode('utf-8')
    return json.loads(body_unicode)


def createUser(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    body = getJSONBody(request)

    user = UserModel(dto=body).save()

    return JsonResponse(data=user.toDict())


def getUsersList(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    users = list(map(lambda u: u.toDict(), UserModel.getAllUsers()))

    return JsonResponse(data={'users': users})


def patchUser(request: HttpRequest, id: int):
    if request.method != 'POST' or id is None:
        return HttpResponseBadRequest()

    body = getJSONBody(request)

    user = UserModel(id=id)
    user.patchInstance(patch=body)

    user.save()

    return JsonResponse(data=user.toDict())


def getUser(request: HttpRequest, id: int):
    if request.method != 'GET' or id is None:
        return HttpResponseBadRequest()

    user = UserModel(id=id)

    return JsonResponse(data=user.toDict())


def deleteUser(request: HttpRequest, id: int):
    if request.method != 'POST' or id is None:
        return HttpResponseBadRequest()

    user = UserModel(id=id).delete()

    return JsonResponse(data=user.toDict())


def getUserChats(request: HttpRequest, id: int):
    if request.method != 'GET' or id is None:
        return HttpResponseBadRequest()

    chats = UserModel(id=id).toDict()['chats']

    return JsonResponse(data={'chats': chats})


def sendMessage(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    body = getJSONBody(request)

    userId = body['userId']
    chatId = body['chatId']
    content = body['content']

    user = UserModel(id=userId)

    if user == None:
        return HttpResponseNotFound()

    chat = next((c for c in user.chats if c.id == chatId), None)

    if chat == None:
        return HttpResponseNotFound()

    message = user.writeMessage(chat=chat, content=content)

    return JsonResponse(data={'message': message.toDict(), 'chat': chat.toDict()})


def createChat(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    body = getJSONBody(request)

    chat = ChatModel(dto={
        'chatType': body['chatType'],
        'name': body['name'],
        'description': body['description'],
    }).save()

    return JsonResponse({'chat': chat.toDict()})


def joinChat(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    body = getJSONBody(request)

    chatId = body['chatId']
    userId = body['userId']

    user = UserModel(id=userId)
    chat = ChatModel(id=chatId)

    try:
        user.joinChat(chat)
    except RuntimeError:
        return HttpResponseBadRequest(content='Already exist')

    return JsonResponse({'user': user.toDict(), 'chat': chat.toDict()})


def leaveChat(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    body = getJSONBody(request)

    chatId = body['chatId']
    userId = body['userId']

    user = UserModel(id=userId)
    chat = ChatModel(id=chatId)

    try:
        user.leaveChat(chat)
    except RuntimeError:
        return HttpResponseBadRequest(content='Not a member')

    return JsonResponse({'user': user.toDict(), 'chat': chat.toDict()})


def getChat(request: HttpRequest, id: int):
    if request.method != 'GET' or id == None:
        return HttpResponseBadRequest()

    chat = ChatModel(id=id)

    return JsonResponse(data=chat.toDict())


def addFaceInfo(request: HttpRequest, id: int):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    body = getJSONBody(request)

    user = UserModel(id=id)

    if user.faceInfo_id != None:
        return HttpResponseBadRequest(content='Already exist')

    faceInfo = FaceInfoModel(dto=body).save()
    user.addFaceInfo(faceInfo=faceInfo)

    return JsonResponse(data=user.toDict())


# FaceInfoGateway.deleteFaceInfo - FK CONSTRAINT FAIL
def removeFaceInfo(request: HttpRequest, id: int):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    user = UserModel(id=id)

    try:
        user.removeFaceInfo()
    except:
        return HttpResponseBadRequest(content='Doesnt exist')

    return JsonResponse(data=user.toDict())
