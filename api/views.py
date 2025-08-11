from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import Resource, Document
from .serializers import ResourceSerializer, DocumentSerializer
import logging
import cloudinary.uploader
import cloudinary.api
from django.shortcuts import get_object_or_404
import hashlib

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
                folder='documents/',
                public_id=request.FILES['file'].name.rsplit('.', 1)[0]  # Use original filename without extension
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
    parser_classes = (MultiPartParser,)
    
    def post(self, request):
        try:
            # Get the uploaded file
            file = request.FILES['file']

            # Calculate checksum (SHA256)
            sha256 = hashlib.sha256()
            for chunk in file.chunks():
                sha256.update(chunk)
            checksum = sha256.hexdigest()
            file.seek(0)  # Reset file pointer after reading

            # Upload to Cloudinary
            cloudinary_response = cloudinary.uploader.upload(
                file,
                folder="resources/",
                resource_type="auto",
                public_id=file.name.rsplit('.', 1)[0]  # Use original filename without extension
            )
            
            # Create resource in your database
            resource = Resource.objects.create(
                title=request.data['title'],
                description=request.data['description'],
                college=request.data['college'],
                branch=request.data['branch'],
                resource_type=request.data['resource_type'],
                file_url=cloudinary_response['secure_url'],
                file_type=file.name.split('.')[-1].lower(),
                size=file.size,
                # Add checksum field if your model supports it
                checksum=checksum
            )
            
            # Optionally, update Cloudinary credentials here if needed (usually not required per request)
            
            return Response({
                'id': resource.id,
                'title': resource.title,
                'file_url': resource.file_url,
                'checksum': checksum,
                # Include other fields as needed
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
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