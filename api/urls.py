from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ResourceListCreateView, FileUploadView, ResourceUploadView  # Add ResourceUploadView

urlpatterns = [
    path('resources/', ResourceListCreateView.as_view()),
    path('documents/', FileUploadView.as_view()),  # Allow GET for documents
    path('resources/upload/', ResourceUploadView.as_view(), name='resource-upload'),  # Existing route
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)