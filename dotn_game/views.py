from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,EnterRoomForm
from .models import CustomUser,Room
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.save()
            return redirect('home') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password. Please try again."

    else:
        form = AuthenticationForm()

    return render(request, 'authentication/login.html', {'form': form, 'error_message': error_message})

def logout(request):
    return redirect(request,'authentication/logout.html')
@login_required
def home(request):
    return render(request, 'home.html')
@login_required
def offline_mode(request):
    return render(request, 'offline_mode.html')
@login_required
def online_mode(request):
    return render(request, 'online_mode.html')


@login_required
def create_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room_name = request.POST.get('room_name')
        password = request.POST.get('room_password')
        open_party = request.POST.get('open_party')
        
        existing_room = Room.objects.filter(room_id=room_id, is_active=False).first()
        if existing_room:
            existing_room.is_active = True
            existing_room.save()
            is_creator = False
        else:
            try:
                room = Room(room_id=room_id, password=password)
                room.save()
                is_creator = True
            except IntegrityError:
                error_message = "Room ID already in use"
                return render(request, 'create_room.html', {'error_message': error_message})

        return redirect('/play_online/' + room_id + '/?symbol=1&is_creator=' + str(int(is_creator)))
    
    return render(request, 'create_room.html')


@login_required
def play_online(request, room_id):
    symbol = request.GET.get('symbol')
    is_creator = request.GET.get('is_creator')
    username = request.user.username
    print(symbol)
    context = {'room_id': room_id,'symbol':symbol,'is_creator':is_creator,'username': username}

    return render(request, 'play_online.html',context)

@login_required
def enter_room(request):
    form = EnterRoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        room_id = form.cleaned_data['room_id']
        room_password = form.cleaned_data['room_password']
        is_creator = False
        try:
            room = Room.objects.get(room_id=room_id)
            if room.password == room_password:
                request.session['current_room'] = room_id
                return redirect('/play_online/' + room_id + '/?symbol=2&is_creator=' + str(int(is_creator)))
            else:
                error_message = "Invalid password"
        except Room.DoesNotExist:
            error_message = "Invalid room ID"
        
        return render(request, 'enter_room.html', {'form': form, 'error_message': error_message})
    
    return render(request, 'enter_room.html', {'form': form})
