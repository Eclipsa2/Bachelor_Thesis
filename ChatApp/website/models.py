from django.db import models
from django.utils import timezone

class ChatSession(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    last_updated = models.DateTimeField(default=timezone.now)
    request_type = models.IntegerField(default=-1)
    is_active = models.BooleanField(default=True)

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message = models.TextField()
    user_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class RequiredEntities(models.Model):
    nume = models.BooleanField()
    program_studii = models.BooleanField()
    grupa = models.BooleanField()
    an_studii = models.BooleanField()
    forma_invatamant = models.BooleanField()
    mentiuni = models.BooleanField()
    titlu_licenta = models.BooleanField()
    titlu_program_studii = models.BooleanField()

class ChatEntities(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    nume = models.CharField(max_length=100, default="")
    program_studii = models.CharField(max_length=100, default="")
    grupa = models.CharField(max_length=100, default="")
    an_studii = models.CharField(max_length=100, default="")
    forma_invatamant = models.CharField(max_length=100, default="")
    mentiuni = models.CharField(max_length=500, default="")
    titlu_licenta = models.CharField(max_length=100, default="")
    titlu_program_studii = models.CharField(max_length=100, default="")