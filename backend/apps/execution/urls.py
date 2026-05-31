from django.urls import path
from .views import StartWorkSessionView

urlpatterns = [
    path('start-session/', StartWorkSessionView.as_view(), name='start-session'),
]