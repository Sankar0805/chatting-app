from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from .models import Room, Message


def logout_view(request):
    # Delete messages created by this user so they disappear after logout
    username = request.session.get('username')
    if username:
        Message.objects.filter(sender=username).delete()

    # Clear all session data and log out
    request.session.flush()
    auth_logout(request)
    return redirect('create-room')


def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        # store username in session so logout can reference it
        request.session['username'] = username

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
            return redirect('room', room_name=room, username=username)

    return render(request, 'index.html')


def MessageView(request, room_name, username):
    # Ensure the session knows this username
    request.session['username'] = username

    get_room = Room.objects.get(room_name=room_name)

    # If the client posts via normal HTTP form, persist message
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Message.objects.create(room=get_room, sender=username, message=message)

    # Load messages from DB for the room
    get_messages = Message.objects.filter(room=get_room)

    context = {
        'messages': get_messages,
        'user': username,
        'room_name': room_name,
    }
    return render(request, 'message.html', context)
