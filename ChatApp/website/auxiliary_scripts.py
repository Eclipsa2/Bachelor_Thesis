from views import *

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