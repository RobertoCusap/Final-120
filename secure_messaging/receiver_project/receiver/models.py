from django.db import models

class ReceivedMessage(models.Model):
    sender_id = models.IntegerField()
    encrypted_content = models.TextField()
    decrypted_content = models.TextField(null=True)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from sender {self.sender_id}"

# # models.py in receiver application
# class ReceivedMessage(models.Model):
#     STATUS_CHOICES = [
#         ('received', 'Received'),
#         ('decrypted', 'Decrypted'),
#         ('processed', 'Processed'),
#         ('error', 'Error')
#     ]
#     sender_id = models.IntegerField()
#     encrypted_content = models.BinaryField()
#     received_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')