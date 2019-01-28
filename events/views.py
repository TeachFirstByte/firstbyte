from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
def event_list(request):
    all_events = Event.objects.all()

    now = datetime.now(timezone.utc)

    upcoming_events = []
    past_events = []
    for event in all_events:
        if now < event.start_datetime:
            upcoming_events.append(event)
        else:
            past_events.append(event)

    event_set = {}
    if len(upcoming_events) > 0:
        event_set['Upcoming Events'] = upcoming_events
    if len(past_events) > 0:
        event_set['Past Events'] = past_events

    return render(request, 'event_list.html', {
        'event_set': event_set,
    })

def event_detail(request, pk, slug):
    obj = get_object_or_404(Event, pk=pk)
    if slug != obj.slug:
        # Replace old slug with correct one
        return redirect(obj.get_absolute_url(), permanent=True)
    return render(request, 'event_detail.html', {
        'event': obj
    })