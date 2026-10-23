import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, BlogPostForm
from django.contrib import messages
from .models import BlogPost, Profile
from django.db.models import Count,Sum
from .models import Newsletter
from django.contrib import messages
from django.db.models import Q
from .models import Message, Like, Comment, SavedBlog, CommentLike, CommentReply
from .models import ContactMessage
from django.http import JsonResponse,HttpResponseForbidden
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Message, Notification
from django.urls import reverse

# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect('register')

        # Password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')

        # Uppercase
        if not re.search(r'[A-Z]', password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect('register')

        # Lowercase
        if not re.search(r'[a-z]', password):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return redirect('register')

        # Number
        if not re.search(r'[0-9]', password):
            messages.error(request, "Password must contain at least one number.")
            return redirect('register')

        # Special symbol
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\[\]]', password):
            messages.error(request, "Password must contain at least one special symbol.")
            return redirect('register')

        # Create user
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'accounts/register.html')


# Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Entered username or password is wrong.")
            return redirect('login')

    return render(request, 'accounts/login.html')


# Home View
def home(request):
    return render(request, 'accounts/home.html')

# Edit Profile View
@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def write_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)

            blog.user = request.user
            blog.category = request.POST.get('category')

            blog.save()

            return redirect(
                'profile_view',
                username=request.user.username
            )

    else:
        form = BlogPostForm()

    return render(
        request,
        'accounts/write_blog.html',
        {'form': form}
    )
    
def home(request):
    # Latest blog
    blogs = BlogPost.objects.all().order_by('-created_at')

    # Top creator
    top_creators = User.objects.annotate(
        blog_count=Count('blogs')
    ).order_by('-blog_count')[:5]

    # Trending blog
    trending_blogs = BlogPost.objects.all().order_by('-views')[:10]

    unread_count = 0

    if request.user.is_authenticated:
        unread_count = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()

    return render(request, 'accounts/home.html', {
        'blogs': blogs,
        'top_creators': top_creators,
        'trending_blogs': trending_blogs,
        'unread_count': unread_count,
    })

def about(request):
    return render(request, 'accounts/about.html')

def contact(request):
    return render(request, 'accounts/contact.html')

def subscribe_newsletter(request):

    if request.method == "POST":

        email = request.POST.get('email')

        if email:

            obj, created = Newsletter.objects.get_or_create(
                email=email
            )

            if created:

                messages.success(
                    request,
                    "✅ Successfully subscribed!"
                )

            else:

                messages.warning(
                    request,
                    "⚠ Email already subscribed!"
                )

    return redirect('home')

def send_newsletter(request):
    blogs = BlogPost.objects.order_by('-created_at')[:5]

    site_url = request.build_absolute_uri('/').rstrip('/')

    context = {
        'blogs': blogs,
        'site_url': site_url,
    }

    html_content = render_to_string(
        'accounts/newsletter_email.html',
        context
    )

    text_content = strip_tags(html_content)

    # Get all newsletter subscribers
    subscribers = Newsletter.objects.all()

# Get their email addresses
    recipient_list = [
    subscriber.email
    for subscriber in subscribers
    ]

# Create the email
    email = EmailMultiAlternatives(
    subject='Latest Blogs from iBlog',
    body=text_content,
    from_email=None,
    to=recipient_list,
)

# Attach the styled HTML template
    email.attach_alternative(html_content, 'text/html')

# Send the email
    email.send()

    return HttpResponse('Test newsletter sent successfully!')

@login_required
def profile_view(request, username):

    user = get_object_or_404(User, username=username)

    user_profile = Profile.objects.get(user=user)

    user_blogs = BlogPost.objects.filter(user=user).order_by('-created_at')

    context = {
        'user_profile': user_profile,
        'user_blogs': user_blogs,
        'profile_user': user,
    }

    return render(request, 'accounts/profile.html', context)


def follow_user(request, username):

    target_user = get_object_or_404(
        User,
        username=username
    )

    profile = target_user.profile

    if request.user in profile.followers.all():

        profile.followers.remove(request.user)

    else:

        profile.followers.add(request.user)

    return redirect(
        'profile_view',
        username=username
    )

def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)

    viewed_posts = request.session.get('viewed_posts', [])

    if blog.id not in viewed_posts:
        blog.views += 1
        blog.save()

        viewed_posts.append(blog.id)
        request.session['viewed_posts'] = viewed_posts

    # Get all comments with related replies and likes
    comments = blog.comments.select_related(
        "user",
        "user__profile"
    ).prefetch_related(
        "replies__user__profile",
        "comment_likes"
    ).order_by("-created_at")

    # Check if the logged-in user has liked the blog
    liked = False
    is_saved = False
    liked_comment_ids = set()
    if request.user.is_authenticated:
        liked = Like.objects.filter(
            user=request.user,
            blog=blog
        ).exists()
        is_saved = SavedBlog.objects.filter(
            user=request.user,
            blog=blog
        ).exists()
        liked_comment_ids = set(
            CommentLike.objects.filter(
                user=request.user,
                comment__blog=blog
            ).values_list('comment_id', flat=True)
        )

    return render(
        request,
        "accounts/blog_detail.html",
        {
            "blog": blog,
            "comments": comments,
            "liked": liked,
            "is_saved": is_saved,
            "liked_comment_ids": liked_comment_ids,
        }
    )

@login_required
def chat_view(request, username):
    receiver = get_object_or_404(User, username=username)

    # Mark incoming chat messages as read
    Message.objects.filter(
        sender=receiver,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    if request.method == "POST":
        content = request.POST.get("message", "").strip()

        if content and request.user != receiver:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )

            # Create a notification for the receiver
            Notification.objects.create(
                recipient=receiver,
                actor=request.user,
                notification_type="message",
                message="sent you a message",
                target_url=reverse(
                    "chat",
                    kwargs={"username": request.user.username}
                )
            )

        return redirect("chat", username=username)

    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by("timestamp")

    return render(request, "accounts/chat.html", {
        "receiver": receiver,
        "messages": messages
    })

@login_required
def inbox_view(request):
    # Get the latest message for each conversation
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related(
        "sender", "receiver"
    ).order_by("-timestamp")

    conversations = {}

    for msg in messages:
        other_user = (
            msg.receiver
            if msg.sender_id == request.user.id
            else msg.sender
        )

        if other_user.pk not in conversations:
            unread_count = Message.objects.filter(
                sender=other_user,
                receiver=request.user,
                is_read=False
            ).count()

            conversations[other_user.pk] = {
                "type": "conversation",
                "user": other_user,
                "last_message": msg,
                "unread_count": unread_count,
                "sort_time": msg.timestamp,
            }

    # Get follower, comment, and reply notifications
    activity = Notification.objects.filter(
        recipient=request.user
    ).exclude(
        notification_type="message"
    ).select_related("actor")

    items = list(conversations.values())

    for notification in activity:
        items.append({
            "type": "notification",
            "notification": notification,
            "sort_time": notification.created_at,
        })

    # Newest message or activity first
    items.sort(
        key=lambda item: item["sort_time"],
        reverse=True
    )

    return render(request, "accounts/inbox.html", {
        "items": items,
    })

@login_required
def notification_list(request):
    
    notifications = Notification.objects.filter(
        recipient=request.user
    ).exclude(
        notification_type="message"
    ).select_related("actor")


    notifications.filter(is_read=False).update(
        is_read=True
    )

    return render(
        request,
        "accounts/notifications.html",
        {"notifications": notifications}
    )

def search_view(request):
    query = request.GET.get('q', '').strip()

    users = []
    blogs = []
    categories = []

    if query:
        # Search creators by username
        matching_users = User.objects.filter(
            username__icontains=query
        )[:10]

        for user in matching_users:
            profile = getattr(user, 'profile', None)

            users.append({
                "username": user.username,
                "image": (
                    profile.profile_image.url
                    if profile and profile.profile_image
                    else ""
                ),
                "bio": profile.bio if profile and profile.bio else ""
            })

        # Search blogs by title, content, or category
        matching_blogs = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        ).select_related('user').distinct()[:10]

        for blog in matching_blogs:
            blogs.append({
                "id": blog.id,
                "title": blog.title,
                "category": blog.category,
                "username": blog.user.username
            })

        # Search category choices
        categories = [
            {"name": choice[0]}
            for choice in BlogPost._meta.get_field('category').choices
            if query.lower() in choice[0].lower()
        ][:10]

    return JsonResponse({
        "users": users,
        "blogs": blogs,
        "categories": categories
    })


def ai_tools_page(request):
    return render(request, 'accounts/ai_tools.html')


def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )

        messages.success(
            request,
            "Your message has been sent successfully!"
        )

    return render(request, 'accounts/contact.html')

def category_blogs(request, category_name):

    blogs = BlogPost.objects.filter(
        category=category_name
    ).order_by('-created_at')

    total_blogs = blogs.count()

    total_views = blogs.aggregate(
        total=Sum('views')
    )['total'] or 0

    trending_blogs = blogs.order_by('-views')[:5]

    top_creators = User.objects.filter(
        blogs__category=category_name
    ).annotate(
        total_blogs=Count('blogs')
    ).order_by('-total_blogs')[:5]

    context = {
        'category': category_name,
        'blogs': blogs,
        'total_blogs': total_blogs,
        'total_views': total_views,
        'trending_blogs': trending_blogs,
        'top_creators': top_creators,
    }

    return render(
        request,
        'accounts/category_blogs.html',
        context
    )

@login_required
def toggle_like(request, blog_id):

    blog = get_object_or_404(BlogPost, id=blog_id)

    like = Like.objects.filter(
        user=request.user,
        blog=blog
    ).first()

    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(
            user=request.user,
            blog=blog
        )
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": blog.likes.count()
    })

@login_required
def add_comment(request, blog_id):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Invalid request."},
            status=405
        )

    blog = get_object_or_404(BlogPost, id=blog_id)

    content = (request.POST.get("content") or "").strip()

    if not content:
        return JsonResponse({
            "success": False,
            "message": "Comment cannot be empty."
        })

    # Save the comment
    comment = Comment.objects.create(
        blog=blog,
        user=request.user,
        content=content
    )

    # Notify the blog owner, but not when commenting on your own blog
    if blog.user_id != request.user.id:
        Notification.objects.create(
            recipient=blog.user,
            actor=request.user,
            notification_type="comment",
            message=f"commented on your blog: {blog.title}",
            target_url=""
        )

    # Preserve your existing AJAX response
    profile_image = request.user.profile.profile_image

    return JsonResponse({
        "success": True,
        "comment_id": comment.id,
        "username": request.user.username,
        "profile": (
            profile_image.url if profile_image else ""
        ),
        "content": comment.content,
        "created_at": "Just now",
        "comments_count": blog.comments.count()
    })

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({
            "success": False
        }, status=403)

    comment.delete()

    return JsonResponse({
        "success": True
    })


# ── Save / Unsave ─────────────────────────────────────────────────────────────
from .models import SavedBlog

@login_required
def toggle_save(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)

    saved = SavedBlog.objects.filter(user=request.user, blog=blog).first()

    if saved:
        saved.delete()
        is_saved = False
    else:
        SavedBlog.objects.create(user=request.user, blog=blog)
        is_saved = True

    return JsonResponse({
        "saved": is_saved
    })


# ── Saved Blogs List ──────────────────────────────────────────────────────────
@login_required
def saved_blogs(request):
    saved = SavedBlog.objects.filter(user=request.user).select_related('blog').order_by('-saved_at')
    blogs = [s.blog for s in saved]
    return render(request, 'accounts/saved_blog.html', {'blogs': blogs})


# ── Toggle Comment Like ───────────────────────────────────────────────────────
@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    existing = CommentLike.objects.filter(
        user=request.user,
        comment=comment
    ).first()

    if existing:
        existing.delete()
        liked = False
    else:
        CommentLike.objects.create(user=request.user, comment=comment)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": comment.comment_likes.count()
    })


# ── Add Reply to Comment ──────────────────────────────────────────────────────
@login_required
def add_reply(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        content = request.POST.get("content", "").strip()

        if not content:
            return JsonResponse({"success": False, "message": "Reply cannot be empty."})

        reply = CommentReply.objects.create(
            comment=comment,
            user=request.user,
            content=content
        )

        return JsonResponse({
            "success": True,
            "reply_id": reply.id,
            "username": request.user.username,
            "profile": request.user.profile.profile_image.url,
            "content": reply.content,
            "created_at": "Just now",
            "replies_count": comment.replies.count()
        })

    return JsonResponse({"success": False})

@login_required
def delete_blog(request, blog_id):

    blog = get_object_or_404(BlogPost, id=blog_id)

    # Only the owner can delete the blog
    if blog.user != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this blog."
        )

    if request.method == "POST":
        blog.delete()
        return redirect("home")

    return redirect("blog_detail", blog_id=blog_id)
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(
        BlogPost,
        id=blog_id,
        user=request.user
    )

    if request.method == "POST":
        blog.title = request.POST.get("title")
        blog.content = request.POST.get("content")
        blog.category = request.POST.get("category")

        if request.FILES.get("image"):
            blog.image = request.FILES.get("image")

        blog.save()

        return redirect("blog_detail", blog_id=blog.id)

    return render(request, "accounts/edit_blog.html", {
    "blog": blog,
    "categories": BlogPost.CATEGORY_CHOICES
})
    
@login_required
def followers_list(request, username):

    profile = get_object_or_404(
        Profile,
        user__username=username
    )

    followers = profile.followers.all()

    return render(
        request,
        "accounts/followers.html",
        {
            "profile": profile,
            "users": followers,
            "title": "Followers"
        }
    )
    
@login_required
def following_list(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    following = profile_user.following.all()

    return render(
        request,
        "accounts/following.html",
        {
            "profile_user": profile_user,
            "users": following,
        }
    )
    