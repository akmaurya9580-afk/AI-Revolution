from django.shortcuts import render, redirect
from django.http import JsonResponse

import ollama
import re

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from .models import ContactMessage, Activity, ChatMessage
from .forms import (
    ProfileForm,
    RegisterForm,
    LoginForm
)


# ==================================================
# HOME
# ==================================================

def home(request):
    return render(request, "index.html")


# ==================================================
# TEXT ANALYZER
# ==================================================

def analyze_text(request):

    result = None

    if request.method == "POST":

        text = request.POST.get(
            "text",
            ""
        ).strip()

        words = len(text.split())

        characters = len(text)

        sentences = 0

        for char in text:
            if char in ".!?":
                sentences += 1

        reading_time = max(
            1,
            round(words / 200)
        )

        result = {
            "words": words,
            "characters": characters,
            "sentences": sentences,
            "reading_time": reading_time,
        }

        # Save activity only for logged-in users
        if request.user.is_authenticated:

            Activity.objects.create(
                user=request.user,
                activity_type="Text Analysis",
                description=f"Analyzed {words} words",
            )

    return render(
        request,
        "index.html",
        {"result": result}
    )


# ==================================================
# REGISTER
# ==================================================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


# ==================================================
# LOGIN
# ==================================================

def login_view(request):

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("dashboard")

    else:

        form = LoginForm()

    return render(
        request,
        "login.html",
        {"form": form}
    )


# ==================================================
# LOGOUT
# ==================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")


# ==================================================
# DASHBOARD
# ==================================================

@login_required(login_url="/login/")
def dashboard(request):

    activities = Activity.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )[:10]

    chat_history = ChatMessage.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )[:10]

    return render(
        request,
        "dashboard.html",
        {
            "activities": activities,
            "chat_history": chat_history,
        }
    )


# ==================================================
# PROFILE
# ==================================================

@login_required(login_url="/login/")
def profile(request):

    return render(
        request,
        "profile.html"
    )


# ==================================================
# CHANGE PASSWORD
# ==================================================

@login_required(login_url="/login/")
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "change_password.html",
        {
            "form": form
        }
    )


# ==================================================
# EDIT PROFILE
# ==================================================

@login_required(login_url="/login/")
def edit_profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )


# ==================================================
# CONTACT
# ==================================================

def contact(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(
            request,
            "Your message has been sent successfully."
        )

        return redirect("home")

    return redirect("home")


# ==================================================
# AI CHAT API - OLLAMA WITH MEMORY
# ==================================================

def chat_api(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Only POST method is allowed."
            },
            status=405
        )

    message = request.POST.get(
        "message",
        ""
    ).strip()

    if not message:

        return JsonResponse({
            "reply": "Please enter a message."
        })

    try:

        # ------------------------------------------
        # Detect user's language
        # ------------------------------------------

        hindi_chars = re.findall(
            r"[\u0900-\u097F]",
            message
        )

        english_chars = re.findall(
            r"[A-Za-z]",
            message
        )

        if hindi_chars and english_chars:

            language = "HINGLISH"

        elif hindi_chars:

            language = "HINDI"

        else:

            language = "ENGLISH"

        # ------------------------------------------
        # Language instruction
        # ------------------------------------------

        if language == "ENGLISH":

            language_instruction = (
                "The user is writing in English. "
                "Reply ONLY in English. "
                "Do not use Hindi or Hinglish."
            )

        elif language == "HINDI":

            language_instruction = (
                "The user is writing in Hindi. "
                "Reply in natural Hindi. "
                "Do not switch to English unnecessarily."
            )

        else:

            language_instruction = (
                "The user is writing in Hinglish. "
                "Reply in natural Hinglish."
            )

        # ------------------------------------------
        # Get previous conversations
        # ------------------------------------------

        previous_chats = []

        if request.user.is_authenticated:

            previous_chats = ChatMessage.objects.filter(
                user=request.user
            ).order_by(
                "-created_at"
            )[:10]

            previous_chats = list(
                reversed(previous_chats)
            )

        # ------------------------------------------
        # Build AI messages
        # ------------------------------------------

        messages_for_ai = [
            {
                "role": "system",
                "content": (
                    "You are AI-Revolution Assistant.\n\n"

                    "You are a helpful, intelligent and "
                    "natural conversational AI assistant.\n\n"

                    "IMPORTANT RULES:\n"
                    "1. Answer the user's actual question directly.\n"
                    "2. Do not repeat the user's message.\n"
                    "3. Do not unnecessarily repeat the user's name.\n"
                    "4. Do not start with filler phrases such as "
                    "'Arre', 'No No', 'Yes Yes', etc.\n"
                    "5. Do not invent facts.\n"
                    "6. If you do not know something, say so clearly.\n"
                    "7. Keep answers natural and useful.\n"
                    "8. Use previous conversation when relevant.\n\n"

                    "LANGUAGE INSTRUCTION:\n"
                    f"{language_instruction}"
                )
            }
        ]

        # ------------------------------------------
        # Add previous conversation
        # ------------------------------------------

        for chat in previous_chats:

            messages_for_ai.append(
                {
                    "role": "user",
                    "content": chat.user_message
                }
            )

            messages_for_ai.append(
                {
                    "role": "assistant",
                    "content": chat.ai_response
                }
            )

        # ------------------------------------------
        # Add current user message
        # ------------------------------------------

        messages_for_ai.append(
            {
                "role": "user",
                "content": message
            }
        )

        # ------------------------------------------
        # Send request to Ollama
        # ------------------------------------------

        response = ollama.chat(
            model="llama3.2:3b",
            messages=messages_for_ai
        )

        reply = response["message"]["content"].strip()

    except Exception as e:

        print("Ollama Error:", e)

        return JsonResponse(
            {
                "reply": (
                    "Sorry, something went wrong "
                    "while connecting to the AI server."
                )
            },
            status=500
        )

    # ------------------------------------------
    # Save conversation
    # ------------------------------------------

    if request.user.is_authenticated:

        ChatMessage.objects.create(
            user=request.user,
            user_message=message,
            ai_response=reply,
        )

        Activity.objects.create(
            user=request.user,
            activity_type="AI Chat",
            description=f"Sent message: {message[:50]}",
        )

    return JsonResponse({
        "reply": reply
    })

# ==================================================
# DELETE CHAT HISTORY
# ==================================================

@login_required(login_url="/login/")
def delete_chat_history(request):

    if request.method == "POST":

        ChatMessage.objects.filter(
            user=request.user
        ).delete()

        messages.success(
            request,
            "Your chat history has been deleted successfully."
        )

    return redirect("dashboard")

# ========================================
# OLLAMAAI
# ==========================================

