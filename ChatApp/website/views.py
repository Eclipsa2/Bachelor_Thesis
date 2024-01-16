from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .forms import SignUpForm
from .models import ChatSession, Message
import torch
from transformers import BertTokenizer, BertModel, BertForSequenceClassification
import spacy

label_mapping = {
    "Adeverinta licenta": 0,
    "Reinscriere an univeristar": 1,
    "Esalonarea platii taxei": 2
}
def write_bot_message(request, chat_session_id, message):
    new_message = Message(
        message=message,
        chat_session_id=chat_session_id,
        user_id=0
    )
    new_message.save()

    chat_session = ChatSession.objects.get(id=chat_session_id)
    chat_session.last_updated = timezone.now()
    chat_session.save()
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

            chat_sessions = ChatSession.objects.filter(user_id=request.user.id, is_active=True
                                                       ).order_by(
                '-last_updated')
            for session in chat_sessions:
                session.last_message = Message.objects.filter(chat_session=session).order_by(
                    '-timestamp').first()

            for session in chat_sessions:
                session.last_message = Message.objects.filter(chat_session=session).order_by(
                    '-timestamp').first()

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

def process_message(request, chat_session_id, new_message_content):
    new_message = Message(
        message=new_message_content,  # Assuming the field is named 'message_text'
        chat_session_id=chat_session_id,
        user_id=request.user.id  # Use the ID of the user
        )
    new_message.save()

    chat_session = ChatSession.objects.get(id=chat_session_id)
    chat_session.last_updated = timezone.now()
    chat_session.save()

def clasify_request(request, new_message_content):
    tokenizer = BertTokenizer.from_pretrained('modele/modelClasificare/')
    model_clasificare = BertForSequenceClassification.from_pretrained('modele/modelClasificare/')

    prompt_tokenized = tokenizer(new_message_content, truncation=True, padding=True, max_length=512,
                                 return_tensors="pt")
    model_clasificare = model_clasificare.to('cpu')
    inputs = {key: value.to('cpu') for key, value in prompt_tokenized.items()}

    with torch.no_grad():
        outputs = model_clasificare(**inputs)
        logits = outputs.logits

    predicted_class = torch.argmax(logits, dim=1).item()
    predicted_label = [k for k, v in label_mapping.items() if v == predicted_class][0]

    return predicted_class, predicted_label

def process_answer(request, chat_session_id, new_message_content):
    current_chat_session = ChatSession.objects.get(id=chat_session_id)
    if current_chat_session.request_type == -1:
        predicted_class, predicted_label = clasify_request(request, new_message_content)
        ChatSession.objects.filter(id=chat_session_id).update(request_type=predicted_class)

        if predicted_class == 0:
            write_bot_message(request, chat_session_id, "Cred ca ai nevoie de o adeverinta "
            "de licenta. Te rog sa imi spui numele profesorului, numele studentului, grupa si "
                                                        "titlul licentei.")
        elif predicted_class == 1:
            write_bot_message(request, chat_session_id, "Cred ca ai nevoie de o cerere de "
                                                        "reinscriere in anul universitar. Te rog "
                                                        "sa imi spui numele studentului, grupa, "
                                                        "programul de studii, anul de studii, "
                                                        "forma de invatamant si titlul "
                                                        "programului de studii")

        elif predicted_class == 2:
            write_bot_message(request, chat_session_id, "Cred ca ai nevoie de o esalonare a "
                                                        "platii taxei. Te rog sa imi spui numele "
                                                        "studentului, anul de studii, programul "
                                                        "de studii, forma de invatamant si grupa")

    else:
        nlp = spacy.load("/Users/Andrei/Desktop/Licenta/ChatApp/ChatApp/modele/modelNER")
        doc = nlp(new_message_content)

        for ent in doc.ents:
            print(ent.text, ent.label_)


def chat_session_detail(request, chat_session_id):
    if request.method == "POST":
        new_message_content = request.POST.get('new_message')
        if new_message_content:
            process_message(request, chat_session_id, new_message_content)
            process_answer(request, chat_session_id, new_message_content)

    chat_session = get_object_or_404(ChatSession, id=chat_session_id)
    selected_messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')

    chat_sessions = ChatSession.objects.filter(user_id=request.user.id, is_active=True).order_by(
        '-last_updated')
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

def start_new_chat(request):
    new_chat_session = ChatSession(user_id=request.user.id)
    new_chat_session.save()

    new_message = Message(
        message = "Salut! Cu ce te pot ajuta?",
        chat_session_id = new_chat_session.id,
        user_id = 0
    )
    new_message.save()

    return redirect('chat_session_detail', chat_session_id=new_chat_session.id)

def delete_chat(request, chat_session_id):
    ChatSession.objects.filter(id=chat_session_id).update(is_active=False)
    messages.success(request, "Chat deleted successfully")

        # for message in Message.objects.filter(chat_session_id=chat_session_id):
        #     message.delete()

    return redirect('home')