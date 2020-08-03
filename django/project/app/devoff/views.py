import math

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.devoff.serializers import EncryptSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def encrypt(request):
    """Encrypts a message using Scytale method."""
    serializer = EncryptSerializer(data=request.data)
    if serializer.is_valid():
        mensaje = serializer.validated_data["mensaje"]
        vueltas = serializer.validated_data["vueltas"]
        mensaje_encrypt = [
            c for index in range(0, vueltas) for c in mensaje[index::vueltas]
        ]
        return Response({"mensaje": "".join(mensaje_encrypt)})
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["POST"])
@permission_classes([AllowAny])
def decrypt(request):
    """Decrypts a message using Scytale method."""
    serializer = EncryptSerializer(data=request.data)
    if serializer.is_valid():
        mensaje = serializer.validated_data["mensaje"]
        vueltas = serializer.validated_data["vueltas"]
        rows = math.ceil(len(mensaje) / vueltas)
        for missing in range(1, rows * vueltas - len(mensaje)):
            # Fill missing spaces
            position = missing * rows
            mensaje = mensaje[:-position] + " " + mensaje[-position:]
        mensaje_decrypt = [c for index in range(0, rows) for c in mensaje[index::rows]]
        # Joins the whole list and remove extra spaces.
        mensaje_decrypt = "".join(mensaje_decrypt).strip()
        return Response({"mensaje": mensaje_decrypt})
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
