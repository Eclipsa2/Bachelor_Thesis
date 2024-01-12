from django.db import models

# Create your models here.
class ChatSession(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message = models.TextField()
    user_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message