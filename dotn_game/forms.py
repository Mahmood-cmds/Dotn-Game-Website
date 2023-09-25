from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',) 

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class EnterRoomForm(forms.Form):
    room_id = forms.CharField(label='Room ID')
    room_password = forms.CharField(label='Room Password', widget=forms.PasswordInput)
