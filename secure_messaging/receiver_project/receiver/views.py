from rest_framework import viewsets
from rest_framework.response import Response
from .models import ReceivedMessage
from .serializers import ReceivedMessageSerializer
from .encryption import MessageEncryption  # Changed this line to use local import

class ReceivedMessageViewSet(viewsets.ModelViewSet):
    queryset = ReceivedMessage.objects.all()
    serializer_class = ReceivedMessageSerializer

    def create(self, request):
        decryptor = MessageEncryption()
        encrypted_content = request.data.get('encrypted_content').encode()
        sender_id = request.data.get('sender_id')
        
        try:
            decrypted_content = decryptor.decrypt_message(encrypted_content)
            message = ReceivedMessage.objects.create(
                sender_id=sender_id,
                encrypted_content=encrypted_content,
                decrypted_content=decrypted_content
            )
            serializer = self.get_serializer(message)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)