from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Event ,Review
from .forms import EventForm ,ReviewForm
from datetime import datetime

def event_list(request):
    # Get filter and sort parameters from request
    date_filter = request.GET.get('date', None)
    sort_order = request.GET.get('sort', 'latest')  # Default to 'latest'

    # Filter events based on the provided criteria
    events = Event.objects.all()

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            events = events.filter(date=filter_date)
        except ValueError:
            pass  # Invalid date format, ignore filter

    # Sort events based on the provided order
    if sort_order == 'latest':
        events = events.order_by('date', 'time')  # Sort by date and time descending
    elif sort_order == 'oldest':
        events = events.order_by('-date', '-time')  # Sort by date and time ascending

    return render(request, 'event/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = Review.objects.filter(event_id=event_id)
    return render(request, 'event/event_detail.html', {'event': event ,'reviews':reviews})

@login_required
def create_event(request):
    if not request.user.role == 'HOST':
        return redirect('event_list')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.participants.count() >= event.capacity:
        # Handle the case where the event is full
        return render(request, 'event/event_full.html', {'event': event})
    event.participants.add(request.user)
    
    # Prepare email content
    subject = f'Confirmation for joining {event.name}'
    html_message = render_to_string('event/confirmation_email.html', {
        'event': event,
        'user': request.user,
    })
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = request.user.email
    
    # Print email content to console for debugging
    print("Subject:", subject)
    print("From Email:", from_email)
    print("To:", to)
    print("Plain Message:", plain_message)
    print("HTML Message:", html_message)
    
    return redirect('event_detail', event_id=event.id)

@login_required
def myevents(request):
    if request.user.role != 'HOST':
        return redirect('home')
    
    hosted_events = Event.objects.filter(host=request.user)
    return render(request ,'event/myevents.html' ,{'hosted_events':hosted_events})

@login_required
def addreview(request ,event_id):
    event = get_object_or_404(Event ,id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assign the current user as the reviewer
            review.event = event  # Link the review to the event
            review.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = ReviewForm()
    return render(request ,'event/addreview.html' ,{'form':form})

