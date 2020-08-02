from rest_framework import serializers

class EncryptSerializer(serializers.Serializer):
    vueltas = serializers.IntegerField()
    mensaje = serializers.CharField()