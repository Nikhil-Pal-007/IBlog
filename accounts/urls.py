"""
URL configuration for Iblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name='home'),
    path('search/', views.search_view, name='search'),
    path('login/',views.user_login, name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('write-blog/', views.write_blog, name='write_blog'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/delete/',views.delete_blog,name='delete_blog'),
    path('subscribe/',views.subscribe_newsletter,
    name='subscribe_newsletter'),
    path('follow/<str:username>/',views.follow_user,name='follow_user'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:category_name>/',views.category_blogs,name='category_blogs'),
    path('blog/<int:blog_id>/like/',views.toggle_like,name='toggle_like'),
    path('blog/<int:blog_id>/comment/',views.add_comment,name='add_comment'),
    path("comment/<int:comment_id>/delete/",views.delete_comment,name="delete_comment"),
    path('blog/<int:blog_id>/save/', views.toggle_save, name='toggle_save'),
    path('saved/', views.saved_blogs, name='saved_blogs'),
    path('comment/<int:comment_id>/like/', views.toggle_comment_like, name='toggle_comment_like'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path("blog/<int:blog_id>/edit/", views.edit_blog, name="edit_blog"),
    path("blog/<int:blog_id>/delete/",views.delete_blog,name="delete_blog"),
    path("profile/<str:username>/followers/",views.followers_list,name="followers_list"),
    path("profile/<str:username>/following/",views.following_list,name="following_list"),
    path('send-newsletter/', views.send_newsletter,name='send_newsletter'),
    path("notifications/",views.notification_list,name="notification_list"),
]
