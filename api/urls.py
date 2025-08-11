from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ResourceListCreateView, FileUploadView, ResourceUploadView , DocumentDetailView # Add ResourceUploadView

urlpatterns = [
    path('resources/', ResourceListCreateView.as_view()),
    path('upload/', FileUploadView.as_view()),
    path('upload/', ResourceUploadView.as_view()),
    path('documents/', DocumentDetailView.as_view()),  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
