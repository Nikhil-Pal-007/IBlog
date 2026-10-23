from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg'
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    followers = models.ManyToManyField(
        User,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.user.username


    
#  Blog Post model
class BlogPost(models.Model):

    CATEGORY_CHOICES = [
        ('Technology', 'Technology'),
        ('Travel', 'Travel'),
        ('Food', 'Food'),
        ('Entertainment', 'Entertainment'),
        ('Fitness', 'Fitness'),
        ('Photography', 'Photography'),
        ('Nature', 'Nature'),
        ('PersonalStories', 'Personal Stories'),
        ('Sports', 'Sports'),
        ('SelfImprovement', 'Self Improvement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    content = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Technology'
    )
    
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Newsletter(models.Model):

    email = models.EmailField(unique=True)

    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
# Message Model 
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    

class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    notification_type = models.CharField(
        max_length=20,
        choices=[
            ("follow", "Follow"),
            ("comment", "Comment"),
            ("reply", "Reply"),
            ("message", "Message"),
        ]
    )

    message = models.CharField(max_length=255)

    target_url = models.CharField(
        max_length=500,
        blank=True
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.actor} - {self.notification_type} - {self.recipient}"

    
# models.py

# models.py

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    blog = models.ForeignKey(
        "BlogPost",
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "blog")


class Comment(models.Model):
    blog = models.ForeignKey(
        "BlogPost",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.comment_likes.count()

    def __str__(self):
        return f"{self.user.username} commented on {self.blog.title}"


# ❤️ Like on Comment
class CommentLike(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="comment_likes"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")

    def __str__(self):
        return f"{self.user.username} liked a comment"


# 💬 Reply to Comment
class CommentReply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} replied to a comment"


# 🔖 Saved Blogs
class SavedBlog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    blog = models.ForeignKey(
        "BlogPost",
        on_delete=models.CASCADE
    )

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "blog")

    def __str__(self):
        return f"{self.user.username} saved {self.blog.title}"