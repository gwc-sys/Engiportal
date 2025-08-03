from rest_framework import serializers
from .models import Resource, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def validate_file(self, value):
        valid_extensions = ['pdf', 'docx', 'pptx', 'txt']
        extension = value.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            raise serializers.ValidationError(f"File type not supported. Allowed: {', '.join(valid_extensions)}")
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

class ResourceSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)
    
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'branch', 'created_at', 'upload_date', 'document']  # 'branch' moved before dates
        read_only_fields = ['created_at', 'upload_date']

    def to_internal_value(self, data):
        print("\n[ResourceSerializer] Raw input data:", data)
        try:
            result = super().to_internal_value(data)
            print("[ResourceSerializer] Processed internal value:", result)
            return result
        except Exception as e:
            print("[ResourceSerializer] Error in to_internal_value:", str(e))
            raise

    def to_representation(self, instance):
        print("\n[ResourceSerializer] Converting instance to representation:", instance)
        try:
            result = super().to_representation(instance)
            print("[ResourceSerializer] Final representation:", result)
            return result
        except Exception as e:
            print("[ResourceSerializer] Error in to_representation:", str(e))
            raise

    def validate(self, data):
        print("\n[ResourceSerializer] Validating data:", data)
        try:
            # Add your custom validation logic here if needed
            return super().validate(data)
        except Exception as e:
            print("[ResourceSerializer] Validation error:", str(e))
            raise

    def create(self, validated_data):
        print("\n[ResourceSerializer] Creating with validated data:", validated_data)
        try:
            instance = super().create(validated_data)
            print("[ResourceSerializer] Created instance:", instance)
            return instance
        except Exception as e:
            print("[ResourceSerializer] Error during creation:", str(e))
            raise

    def update(self, instance, validated_data):
        print("\n[ResourceSerializer] Updating instance:", instance)
        print("[ResourceSerializer] With validated data:", validated_data)
        try:
            instance = super().update(instance, validated_data)
            print("[ResourceSerializer] Updated instance:", instance)
            return instance
        except Exception as e:
            print("[ResourceSerializer] Error during update:", str(e))
            raise