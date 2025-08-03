from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ResourceListCreateView, FileUploadView, ResourceUploadView  # Add ResourceUploadView

urlpatterns = [
    path('resources/', ResourceListCreateView.as_view()),
    path('upload/file/', FileUploadView.as_view()),
    path('upload/resource/', ResourceUploadView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
