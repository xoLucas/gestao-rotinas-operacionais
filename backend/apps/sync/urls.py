from django.urls import path
from .views import SyncInitialView, SyncUploadView

urlpatterns = [
    path('initial/', SyncInitialView.as_view(), name='sync-initial'),
    path('upload/', SyncUploadView.as_view(), name='sync-upload'),
]