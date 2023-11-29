from django.shortcuts import render
from messenger_app.models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .rsa_utils import generate_rsa_keypair, encrypt_message, decrypt_message


@login_required
def home(request):

    return render(request, 'home.html')


@login_required
def chat(request):

    all_chats = Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user)).order_by('-last_message_time')

    print(all_chats)

    return render(request, 'chat.html', {'all_chats': all_chats})


@login_required
def chat_with(request, user_name):
    user = get_object_or_404(User, username=user_name)
    chat_with_list = Chat.objects.filter(Q(user_1=request.user, user_2=user) | Q(user_1=user, user_2=request.user))
    if len(chat_with_list) == 0:
        chat_with = Chat.objects.create(user_1=request.user, user_2=user)
    else:
        chat_with = chat_with_list[0]

    another_user = chat_with.user_2 if chat_with.user_1 == request.user else chat_with.user_1

    if request.method == 'POST':
        print(request.POST)
        message = request.POST.get('messageInput', '')
        photo_input = request.FILES.get('photoInput')

        if photo_input:
            file_path = default_storage.save('media/' + photo_input.name, ContentFile(photo_input.read()))
            message = file_path

        if message != '':
            messages_all = Message.objects.filter(chat=chat_with)

            if messages_all.exists():
                message_page = messages_all.last()
            else:
                message_page = Message.objects.create(chat=chat_with)

            time = timezone.now()
            message_page.messages = f'{message_page.messages}@@@{message}^^^{request.user}^^^{time}'
            message_page.save()
            messages_list = [i.split('^^^') for i in message_page.messages.split('@@@')]
            messages_list = messages_list[::-1]
            chat_with.last_message_time = time
            chat_with.last_message = message
            chat_with.save()

            return render(request, 'chat_with.html', {'chat_with': chat_with,
                                                      'another_user': another_user,
                                                      'messages_list': messages_list,
                                                      })

    messages_all = Message.objects.filter(chat=chat_with)
    if messages_all.exists():
        message_page = messages_all.last()
        messages_list = [i.split('^^^') for i in message_page.messages.split('@@@')]
        messages_list = messages_list[::-1]
    else:
        messages_ob = Message.objects.create(chat=chat_with)
        messages_list = messages_ob.messages

    return render(request, 'chat_with.html', {'chat_with': chat_with,
                                              'another_user': another_user,
                                              'messages_list': messages_list,
                                              })


def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query)[:10]

    user_list = [{'id': user.id, 'username': user.username} for user in users]

    return JsonResponse(user_list, safe=False)


def generate_keys(request):
    private_key, public_key = generate_rsa_keypair()
    return JsonResponse({'private_key': private_key, 'public_key': public_key})


def encrypt(request):
    public_key = request.POST.get('public_key', '')
    message = request.POST.get('message', '')

    if not public_key or not message:
        return JsonResponse({'error': 'Public key and message are required.'})

    ciphertext = encrypt_message(public_key, message)
    return JsonResponse({'ciphertext': ciphertext})


def decrypt(request):
    private_key = request.POST.get('private_key', '')
    ciphertext = request.POST.get('ciphertext', '')

    if not private_key or not ciphertext:
        return JsonResponse({'error': 'Private key and ciphertext are required.'})

    plaintext = decrypt_message(private_key, ciphertext)
    return JsonResponse({'plaintext': plaintext})