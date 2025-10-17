from django.contrib.auth import logout as auth_logout

def logout_view(request):
    # Clear all session data
    request.session.flush()
    # If using Django auth, also log out
    auth_logout(request)
    return redirect('create-room')
from django.shortcuts import render, redirect
from .models import *

def CreateRoom(request):

    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)
        except Room.DoesNotExist:
            new_room = Room(room_name = room)
            new_room.save()
            return redirect('room', room_name=room, username=username)
        
    return render(request, 'index.html')

def MessageView(request, room_name, username):

    # Use session to store messages per room
    session_key = f"messages_{room_name}"
    if session_key not in request.session:
        request.session[session_key] = []

    if request.method == 'POST':
        message = request.POST['message']
        print(message)
        # Append new message to session
        messages = request.session[session_key]
        messages.append({'sender': username, 'message': message})
        request.session[session_key] = messages

    get_messages = request.session.get(session_key, [])

    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'message.html', context)