from django.db import models
from django.contrib.auth.models import User


# ==============================
# Contact Message Model
# ==============================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# ==============================
# Activity Model
# ==============================

class Activity(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    activity_type = models.CharField(
        max_length=100
    )

    description = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"


# ==============================
# Chat Message Model
# ==============================

class ChatMessage(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    user_message = models.TextField()

    ai_response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.created_at.strftime('%d %b %Y %H:%M')}"
        )