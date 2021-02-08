# tonline_api/utils.py (common utils)
from rest_framework.response import Response


class StandardErrorResponse(Response):
    def __init__(self, detail, code: str, status: int):
        payload = {"detail": detail, "code": code}
        super().__init__(data=payload, status=status)
