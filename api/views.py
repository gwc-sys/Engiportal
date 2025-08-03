from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import Resource, Document
from .serializers import ResourceSerializer, DocumentSerializer
import logging

# Create your views here.

class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all().order_by('-upload_date')
    serializer_class = ResourceSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            # Log the error for debugging
            logging.error(f"Cloudinary upload error: {str(e)}")
            # Return a custom error response
            return Response(
                {"error": "File upload failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, format=None):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        file_serializer = DocumentSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResourceUploadView(APIView):
    def post(self, request, format=None):
        try:
            document_id = request.data.get('document_id')
            if document_id:
                document = Document.objects.get(id=document_id)
            else:
                # Fallback: Create new document if no ID provided
                document = Document.objects.create(
                    name=request.data.get('title', 'Untitled'),
                    file=request.data['file']
                )

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
