from .models import Server
from rest_framework import serializers

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ['title', 'body']