from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReceivedMessageViewSet

router = DefaultRouter()
router.register(r'received-messages', ReceivedMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]