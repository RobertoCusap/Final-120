from rest_framework import serializers
from .models import ReceivedMessage

class ReceivedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivedMessage
        fields = ['id', 'sender_id', 'decrypted_content', 'received_at']