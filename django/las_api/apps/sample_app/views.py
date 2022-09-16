from django.shortcuts import render

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import socket


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def sample_app_view(request):
    """
    get:
        - sample_app_view
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    result = {"result": port}

    return Response(result)
