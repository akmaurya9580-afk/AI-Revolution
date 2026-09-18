from django.contrib import admin

from .models import (
    ContactMessage,
    Activity,
    ChatMessage
)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "activity_type",
        "description",
        "created_at",
    )

    list_filter = (
        "activity_type",
        "created_at",
    )

    search_fields = (
        "user__username",
        "description",
    )

    ordering = (
        "-created_at",
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "user_message",
        "ai_response",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user__username",
        "user_message",
        "ai_response",
    )

    ordering = (
        "-created_at",
    )