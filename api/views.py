from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import Resource, Document
from .serializers import ResourceSerializer, DocumentSerializer
import logging
import cloudinary.uploader

class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all().order_by('-upload_date')
    serializer_class = ResourceSerializer

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        try:
            if 'file' not in request.FILES:
                return Response(
                    {"error": "No file provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                request.FILES['file'],
                resource_type='auto',
                folder='documents/'
            )

            # Create Document instance
            document = Document.objects.create(
                name=request.data.get('name', upload_result['original_filename']),
                file=upload_result['secure_url'],
                public_id=upload_result['public_id'],
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

class ResourceUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        try:
            # First upload the file
            file_view = FileUploadView()
            file_response = file_view.post(request)
            
            if file_response.status_code != status.HTTP_201_CREATED:
                return file_response

            # Create the Resource
            document_id = file_response.data['id']
            resource = Resource.objects.create(
                title=request.data.get('title', 'Untitled'),
                description=request.data.get('description', ''),
                branch=request.data.get('branch', ''),
                document_id=document_id
            )

            serializer = ResourceSerializer(resource)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(f"Resource creation error: {str(e)}")
            return Response(
                {"error": "Resource creation failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )