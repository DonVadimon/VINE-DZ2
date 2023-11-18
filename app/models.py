from django.db import models


class FaceInfo(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
    gender = models.CharField(max_length=10, choices=Gender.choices)

    age = models.CharField(max_length=256)
    leftEyeColor = models.CharField(max_length=256)
    rightEyeColor = models.CharField(max_length=256)
    hairColor = models.CharField(max_length=256)
    skinColor = models.CharField(max_length=256)


class Chat(models.Model):
    class ChatType(models.TextChoices):
        PRIVATE = 'PRIVATE', 'Private'
        GROUP = 'GROUP', 'Group'
    chatType = models.CharField(max_length=10, choices=ChatType.choices)

    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)


class User(models.Model):
    faceInfo = models.OneToOneField(
        FaceInfo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    username = models.CharField(max_length=512)
    name = models.CharField(max_length=512)
    email = models.CharField(max_length=512)

    chats = models.ManyToManyField(Chat, blank=True)


class ChatMessage(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='messages')
    chat = models.ForeignKey(Chat,
                             on_delete=models.CASCADE,
                             related_name='messages')
    content = models.TextField()
