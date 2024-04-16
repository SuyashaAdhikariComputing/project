from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Notification

@login_required
def view_notifications(request):
    # Fetch notifications for the logged-in user
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'home/notification.html', {'notifications': notifications})

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    return redirect('view_notifications')