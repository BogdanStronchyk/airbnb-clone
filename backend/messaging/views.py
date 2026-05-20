from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from users.models import User

@login_required(login_url='/api/users/login/')
def inbox_view(request):
    user = request.user
    # Get all distinct users that the current user has exchanged messages with
    sent_to = Message.objects.filter(sender=user).values_list('recipient', flat=True)
    received_from = Message.objects.filter(recipient=user).values_list('sender', flat=True)
    
    interacted_user_ids = set(list(sent_to) + list(received_from))
    conversations = User.objects.filter(id__in=interacted_user_ids)
    
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required(login_url='/api/users/login/')
def conversation_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Mark messages from this user as read
    Message.objects.filter(sender=other_user, recipient=request.user, is_read=False).update(is_read=True)
    
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) | 
        Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=other_user,
                content=content
            )
            return redirect('conversation', user_id=other_user.id)
            
    return render(request, 'messaging/conversation.html', {'messages': messages, 'other_user': other_user})
