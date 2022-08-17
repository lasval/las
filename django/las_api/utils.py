# las_api/utils.py (common utils)
from rest_framework.response import Response
from drf_yasg.inspectors import SwaggerAutoSchema
from collections import OrderedDict


class StandardErrorResponse(Response):
    def __init__(self, detail, code: str, status: int):
        payload = {"detail": detail, "code": code}
        super().__init__(data=payload, status=status)


# ***************************************************************
# drf-yasg SWAGGER_SETTINGS에서 사용
# - read_only / write_only 필드가 doc에서 한번에 노출되지 않도록 하기 위함
# ***************************************************************
class ReadOnly:  # pragma: no cover
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.write_only:
                new_fields[fieldName] = field
        return new_fields


class BlankMeta:  # pragma: no cover
    pass


class WriteOnly:  # pragma: no cover
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.read_only:
                new_fields[fieldName] = field
        return new_fields


class ReadWriteAutoSchema(SwaggerAutoSchema):  # pragma: no cover
    def get_view_serializer(self):
        return self._convert_serializer(WriteOnly)

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override

        return self._convert_serializer(ReadOnly)

    def _convert_serializer(self, new_class):
        serializer = super().get_view_serializer()
        if not serializer:
            return serializer

        class CustomSerializer(new_class, serializer.__class__):
            class Meta(getattr(serializer.__class__, "Meta", BlankMeta)):
                ref_name = new_class.__name__ + serializer.__class__.__name__

        new_serializer = CustomSerializer(data=serializer.data)
        return new_serializer
