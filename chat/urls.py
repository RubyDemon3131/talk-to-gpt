from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('gpt-response/', views.gpt_response, name='gpt_response'),
    path('whisper/', views.whisper_view, name='whisper'),
]
