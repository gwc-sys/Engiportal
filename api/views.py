from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import  Document
from .serializers import  DocumentSerializer
import logging
import cloudinary.uploader
import cloudinary.api
from django.shortcuts import get_object_or_404
import hashlib

class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        try:
            if 'file' not in request.FILES:
                return Response(
                    {"error": "No file provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            file = request.FILES['file']
            upload_result = cloudinary.uploader.upload(
                file,
                resource_type='auto',
                folder='documents/',
                public_id=file.name.rsplit('.', 1)[0]
            )

            document = Document.objects.create(
                title=request.data.get('title', upload_result['original_filename']),
                name=request.data.get('name', upload_result['original_filename']),
                description=request.data.get('description', ''),
                file_url=upload_result['secure_url'],  # Store Cloudinary URL here
                public_id=upload_result['public_id'],
                file_type=file.name.split('.')[-1].lower(),
                college=request.data.get('college', ''),
                branch=request.data.get('branch', ''),
                resource_type=upload_result['resource_type']
            )

            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(f"Cloudinary upload error: {str(e)}")
            return Response(
                {"error": "File upload failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DocumentDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            # Try to get by public_id first
            try:
                document = Document.objects.get(public_id=pk)
            except Document.DoesNotExist:
                # If not found, try by file name
                document = Document.objects.get(file__icontains=pk)

            cloudinary_resource = cloudinary.api.resource(document.public_id)
            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(f"Document retrieval error: {str(e)}")
            return Response(
                {"error": "Document retrieval failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class DocumentListView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer