from rest_framework import viewsets
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from .encryption import MessageEncryption
import requests

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # Initialize encryption
        encryptor = MessageEncryption()
        
        # Get the original message content
        content = serializer.validated_data['content']
        
        # Encrypt the message
        encrypted_content = encryptor.encrypt_message(content)
        
        # Save both original and encrypted content
        message = serializer.save(encrypted_content=encrypted_content)
        
        # Send to recipient
        self.send_message(message)

    def send_message(self, message):
        try:
            response = requests.post(
                message.recipient_url,
                json={
                    'encrypted_content': message.encrypted_content.decode(),
                    'sender_id': message.id
                },
                headers={'Content-Type': 'application/json'}
            )
            message.status = 'sent' if response.status_code == 200 else 'received'
            message.save()
        except Exception as e:
            message.status = 'failed'
            message.save()


# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.utils import timezone
# import requests
# import logging

# from .models import Message
# from .serializers import MessageSerializer
# from .encryption import MessageEncryption

# logger = logging.getLogger(__name__)

# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

#     def perform_create(self, serializer):
#         """
#         Creates a new message with encryption and handles sending.
#         Implements proper error handling and status management.
#         """
#         try:
#             # Initialize encryption
#             encryptor = MessageEncryption()
            
#             # Get and validate the message content
#             content = serializer.validated_data['content']
#             if not content:
#                 raise ValueError("Message content cannot be empty")

#             # Set initial status and encrypt
#             initial_data = {
#                 'status': 'encrypting',
#                 'created_at': timezone.now()
#             }
            
#             try:
#                 encrypted_content = encryptor.encrypt_message(content)
#                 initial_data['status'] = 'encrypted'
#                 initial_data['encrypted_content'] = encrypted_content
#             except Exception as encryption_error:
#                 logger.error(f"Encryption failed: {encryption_error}")
#                 initial_data['status'] = 'encryption_failed'
#                 initial_data['error_message'] = str(encryption_error)[:255]
#                 raise

#             # Save the message with encrypted content
#             message = serializer.save(**initial_data)

#             # Only attempt to send if encryption succeeded
#             if message.status == 'encrypted':
#                 self.send_message(message)

#             return message

#         except Exception as e:
#             logger.error(f"Message creation failed: {e}")
#             # Let DRF handle the exception response
#             raise

#     def send_message(self, message):
#         """
#         Sends an encrypted message to the recipient URL with comprehensive
#         error handling and status tracking.
#         """
#         try:
#             # Mark as in progress
#             message.status = 'sending'
#             message.last_attempt = timezone.now()
#             message.save()

#             # Prepare the payload
#             payload = {
#                 'encrypted_content': message.encrypted_content.decode(),
#                 'sender_id': message.id,
#                 'timestamp': timezone.now().isoformat()
#             }

#             # Send with timeout
#             response = requests.post(
#                 message.recipient_url,
#                 json=payload,
#                 headers={
#                     'Content-Type': 'application/json',
#                     'X-Message-ID': str(message.id)
#                 },
#                 timeout=30  # 30 second timeout
#             )

#             # Handle different response scenarios
#             if response.status_code == 200:
#                 message.status = 'delivered'
#                 try:
#                     message.delivery_confirmation = response.json()
#                 except ValueError:
#                     message.delivery_confirmation = {'raw_status': response.status_code}
#             elif response.status_code >= 500:
#                 message.status = 'server_error'
#                 message.error_message = f"Server error {response.status_code}"
#             elif response.status_code >= 400:
#                 message.status = 'client_error'
#                 message.error_message = f"Client error {response.status_code}"
#             else:
#                 message.status = 'failed'
#                 message.error_message = f"Unexpected status {response.status_code}"

#             message.response_code = response.status_code

#         except requests.Timeout:
#             message.status = 'timeout'
#             message.error_message = "Request timed out after 30 seconds"
#         except requests.ConnectionError as e:
#             message.status = 'connection_error'
#             message.error_message = f"Connection failed: {str(e)[:255]}"
#         except Exception as e:
#             message.status = 'failed'
#             message.error_message = str(e)[:255]
#             logger.exception(f"Unexpected error sending message {message.id}")

#         finally:
#             message.save(update_fields=['status', 'last_attempt', 'response_code', 
#                                       'error_message', 'delivery_confirmation'])