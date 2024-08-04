# admin.py
from django.contrib import admin
from .models import Host, Participant

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']
