from django.db import models

class Message(models.Model):                                # class that represents messages being sent, processed, or stored in a secure messaging system
    content = models.TextField()
    encrypted_content = models.TextField(null=True)
    recipient_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)  
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Message {self.id} - {self.status}"
    
   

# models.py in sender application
# class Message(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('sending', 'Sending'),
#         ('sent', 'Sent'),
#         ('delivered', 'Delivered'),
#         ('failed', 'Failed')
#     ]
#     content = models.TextField()
#     encrypted_content = models.BinaryField()
#     recipient_url = models.URLField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)