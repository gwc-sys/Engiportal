
from rest_framework import serializers
from .models import  Document


class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"
        # If you want *all* fields read-only
        read_only_fields = [f.name for f in Document._meta.get_fields()]

    def get_file_url(self, obj):
        return obj.file.url if obj.file else None

    def get_file_type(self, obj):
        return obj.file.name.split('.')[-1].lower() if obj.file else None

    def get_size(self, obj):
        return obj.file.size if obj.file else None

    def validate_file(self, value):
        valid_extensions = ['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx']
        extension = value.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            raise serializers.ValidationError(
                f"Unsupported file type. Allowed: {', '.join(valid_extensions)}"
            )
        return value

    def to_internal_value(self, data):
        print("\n[DocumentSerializer] Raw input data:", data)
        try:
            result = super().to_internal_value(data)
            print("[DocumentSerializer] Processed internal value:", result)
            return result
        except Exception as e:
            print("[DocumentSerializer] Error in to_internal_value:", str(e))
            raise

    def to_representation(self, instance):
        print("\n[DocumentSerializer] Converting instance to representation:", instance)
        try:
            result = super().to_representation(instance)
            print("[DocumentSerializer] Final representation:", result)
            return result
        except Exception as e:
            print("[DocumentSerializer] Error in to_representation:", str(e))
            raise


# class ResourceSerializer(serializers.ModelSerializer):
#     document = DocumentSerializer(read_only=True)

#     class Meta:
#         model = Resource
#         fields = [
#             'id', 'title', 'description', 'branch', 'college',
#             'file', 'file_url', 'file_type', 'size',
#             'public_id', 'resource_type', 'uploaded_at', 'upload_date', 'created_at'
#         ]
#         read_only_fields = ['uploaded_at', 'upload_date', 'created_at', 'file_url', 'size']

#     def to_internal_value(self, data):
#         print("\n[ResourceSerializer] Raw input data:", data)
#         try:
#             result = super().to_internal_value(data)
#             print("[ResourceSerializer] Processed internal value:", result)
#             return result
#         except Exception as e:
#             print("[ResourceSerializer] Error in to_internal_value:", str(e))
#             raise

#     def to_representation(self, instance):
#         print("\n[ResourceSerializer] Converting instance to representation:", instance)
#         try:
#             result = super().to_representation(instance)
#             print("[ResourceSerializer] Final representation:", result)
#             return result
#         except Exception as e:
#             print("[ResourceSerializer] Error in to_representation:", str(e))
#             raise

#     def validate(self, data):
#         print("\n[ResourceSerializer] Validating data:", data)
#         try:
#             return super().validate(data)
#         except Exception as e:
#             print("[ResourceSerializer] Validation error:", str(e))
#             raise

#     def create(self, validated_data):
#         print("\n[ResourceSerializer] Creating with validated data:", validated_data)
#         try:
#             document_data = {
#                 'file': validated_data.pop('file', None),
#                 'resource_type': validated_data.get('resource_type'),
#                 'college': validated_data.get('college'),
#             }

#             instance = Resource.objects.create(**validated_data)

#             if document_data['file']:
#                 document = Document.objects.create(
#                     resource=instance,
#                     file=document_data['file'],
#                     resource_type=document_data['resource_type'],
#                     college=document_data['college'],
#                     name=document_data['file'].name
#                 )
#                 instance.document = document
#                 instance.save()

#             print("[ResourceSerializer] Created instance:", instance)
#             return instance
#         except Exception as e:
#             print("[ResourceSerializer] Error during creation:", str(e))
#             raise

#     def update(self, instance, validated_data):
#         print("\n[ResourceSerializer] Updating instance:", instance)
#         print("[ResourceSerializer] With validated data:", validated_data)
#         try:
#             instance = super().update(instance, validated_data)
#             print("[ResourceSerializer] Updated instance:", instance)
#             return instance
#         except Exception as e:
#             print("[ResourceSerializer] Error during update:", str(e))
#             raise
