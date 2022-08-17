"""doc_schemas 모듈 설명

각 app별로 doc_schemas.py 모듈을 포함하여 해당 모듈내에서
변수로 각 API에 대한 request_body, response를 정의

정의된 값들은 views.py 내에서 각 API 상단에 데코레이터로 swagger / redoc 문서화에 필요한
request_body, response에 할당하여 사용
"""
from drf_yasg import openapi
from typing import Final

# /users/login API에서 문서화 (swagger / redoc)을 위해 사용하는 request_body & response
LOGIN_REQUEST_BODY: Final = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "phone": openapi.Schema(
            title="Phone Number",
            type=openapi.TYPE_STRING,
            description="`<= 20 characters`",
        ),
        "password": openapi.Schema(
            title="Password",
            type=openapi.TYPE_STRING,
            description="`8 <= & <= 128 characters`",
        ),
    },
    required=["email", "password"],
)
LOGIN_RESPONSE: Final = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "token": openapi.Schema(
                title="Token",
                type=openapi.TYPE_STRING,
                description="Token string",
            ),
        },
    )
}

# /users/current API에서 문서화 (swagger / redoc)을 위해 사용하는 request_body & response
CURRENT_REQUEST_BODY: Final = None
CURRENT_RESPONSE: Final = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone": openapi.Schema(
                title="Phone Number",
                type=openapi.TYPE_STRING,
                description="`<= 20 characters`",
            ),
            "username": openapi.Schema(
                title="Username",
                type=openapi.TYPE_STRING,
                description="`<= 150 characters` `Nullable`",
            ),
        },
    )
}

# /users/registration API에서 문서화 (swagger / redoc)을 위해 사용하는 request_body & response
REGISTRATION_REQUEST_BODY: Final = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "phone": openapi.Schema(
            title="Phone Number",
            type=openapi.TYPE_STRING,
            description="`<= 20 characters`",
        ),
        "username": openapi.Schema(
            title="Username",
            type=openapi.TYPE_STRING,
            description="`<= 150 characters` `Nullable`",
        ),
        "password1": openapi.Schema(
            title="Password1",
            type=openapi.TYPE_STRING,
            description="`8 <= & <= 128 characters`",
        ),
        "password2": openapi.Schema(
            title="Password2",
            type=openapi.TYPE_STRING,
            description="`8 <= & <= 128 characters`",
        ),
    },
    required=["email", "password1", "password2"],
)
REGISTRATION_RESPONSE: Final = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "token": openapi.Schema(
                title="Token",
                type=openapi.TYPE_STRING,
                description="Token string",
            )
        },
    )
}
