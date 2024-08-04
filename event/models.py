from django.db import models
from django.conf import settings
from user.models import User

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_events'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through = 'EventParticipant',
        related_name='participating_events',
        blank=True
    )
    capacity = models.IntegerField(default=10)
    
    def __str__(self):
        return self.name

class EventParticipant(models.Model):
    event = models.ForeignKey(Event ,on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event' ,'participant')
    
    def __str__(self):
        return f'{self.participant.username} joined {self.event.name}'

class Review(models.Model):
    content = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} commented: {self.content}"


