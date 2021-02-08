from django.shortcuts import render

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def test_app(request):
    """
    get:
        - test_app
    """

    result = {"result": "HelloWorld!!"}

    return Response(result)
