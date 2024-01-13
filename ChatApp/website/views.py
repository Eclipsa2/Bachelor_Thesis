from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import ChatSession, Message
def home(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}")
        else:
            messages.error(request, "Invalid username or password")
        return redirect("home")
    else:

        if request.user.is_authenticated:

            chat_sessions = ChatSession.objects.filter(user_id=request.user.id)

            for session in chat_sessions:
                session.last_message = Message.objects.filter(chat_session=session).order_by(
                    '-timestamp').first()
                print(session.last_message)

            return render(request, "home.html", {"chat_sessions": chat_sessions})

        return render(request, "home.html", {})
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")

    return redirect("home")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f"You have successfully signed up {username}")
            return redirect("home")

    else:
        form = SignUpForm()
        return render(request, "register.html", {'form': form})

    return render(request, "register.html", {'form': form})

def process_message(request, chat_session_id):
    new_message_content = request.POST.get('new_message')

    if new_message_content:
        # Use request.user.id to get the ID of the user
        new_message = Message(
            message=new_message_content,  # Assuming the field is named 'message_text'
            chat_session_id=chat_session_id,
            user_id=request.user.id  # Use the ID of the user
        )
        new_message.save()

def process_answer(request, chat_session_id):
    pass

def chat_session_detail(request, chat_session_id):
    if request.method == "POST":
        process_message(request, chat_session_id)
        process_answer(request, chat_session_id)

    chat_session = get_object_or_404(ChatSession, id=chat_session_id)
    selected_messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')

    chat_sessions = ChatSession.objects.filter(user_id=request.user.id)
    for session in chat_sessions:
        session.last_message = Message.objects.filter(chat_session=session).order_by(
            '-timestamp').first()

    # Fetch usernames
    user_ids = selected_messages.values_list('user_id', flat=True)
    usernames = User.objects.filter(id__in=user_ids).values_list('id', 'username')
    username_map = {uid: uname for uid, uname in usernames}

    # Add usernames to messages
    for message in selected_messages:
        message.sender_username = username_map.get(message.user_id)

    return render(request, "chat_session_detail.html", {
        "chat_sessions": chat_sessions,
        "selected_messages": selected_messages,
        "user": request.user,
        "current_path": request.path
    })
