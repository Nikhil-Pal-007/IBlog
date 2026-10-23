from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='ai_dashboard'),
    path('summarizer/',views.summarizer,name='summarizer'),
    path('translator/',views.translator,name='translator'),
    path("text-to-speech/",views.text_to_speech,name="text_to_speech"),
    path("mood-selector/",views.mood_selector,name="mood_selector"),
    path("check-writing/", views.check_writing, name="check_writing"),
]
