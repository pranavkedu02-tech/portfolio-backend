from rest_framework import serializers


class ContactMessageSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    message = serializers.CharField()

    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Full name cannot be empty.")
        return value.strip()

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value.strip()