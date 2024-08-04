# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Host, Participant

class HostRegistrationForm(UserCreationForm):
    class Meta:
        model = Host
        fields = ['username', 'email', 'password1', 'password2']

class ParticipantRegistrationForm(UserCreationForm):
    class Meta:
        model = Participant
        fields = ['username', 'email', 'password1', 'password2']
