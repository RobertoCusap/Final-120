from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'recipient_url', 'timestamp', 'status']
        read_only_fields = ['timestamp', 'status']