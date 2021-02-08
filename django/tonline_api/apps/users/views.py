from django.shortcuts import render
from django.db import IntegrityError
from .models import CustomUser
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
from tonline_api.utils import StandardErrorResponse
from .utils import (
    RegistrationValidationValues,
    LoginValidationValues,
    ValidationErrorStrs,
    validate_registration,
    validate_login,
    returnUserAuthFailedError,
)
from users import doc_schemas as ds


@swagger_auto_schema(
    method="post",
    request_body=ds.LOGIN_REQUEST_BODY,
    responses=ds.LOGIN_RESPONSE,
)
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def login(request):
    """
    post:타입별 커스텀 유저 로그인 API

    ---
    ## API URL: `/users/login/`
    """
    email = request.data.get("email")
    password = request.data.get("password")

    # Validation check
    validation_result = validate_login(LoginValidationValues(request))
    if isinstance(validation_result, StandardErrorResponse):
        return validation_result

    # 유저 타입 체크가 완료되면 타입별로 유저 정보를 확인하여 로그인 처리
    try:
        user = CustomUser.objects.get(email=email)
        is_password_valid = user.check_password(password)
    except CustomUser.DoesNotExist:
        return returnUserAuthFailedError()
    else:
        if not is_password_valid:
            return returnUserAuthFailedError()

        # 해당 유저의 토큰이 존재하면 그대로 리턴, 없으면 새로 만들어 리턴
        try:
            token_obj = Token.objects.create(user=user)
        except IntegrityError:
            token_obj = Token.objects.get(user=user)
        token = token_obj.key

        # 유저의 last_login값 업데이트
        user.last_login = datetime.now()
        user.save(update_fields=["last_login"])

    return Response({"token": token})


@swagger_auto_schema(
    method="get",
    request_body=ds.CURRENT_REQUEST_BODY,
    responses=ds.CURRENT_RESPONSE,
)
@api_view(["GET"])
@permission_classes((permissions.IsAuthenticated,))
def current(request):
    """
    get:현재 로그인한 유저의 정보를 조회하는 API

    ---
    ## API URL: `/users/current/`
    """
    return Response(
        {
            "email": request.user.email,
            "username": request.user.username,
        }
    )


@swagger_auto_schema(
    method="post",
    request_body=ds.REGISTRATION_REQUEST_BODY,
    responses=ds.REGISTRATION_RESPONSE,
)
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def registration(request):
    """
    post: user_type별로 가입 처리를 하는 API

    ---
    ## API URL: `/users/registration/`
    """
    email = request.data.get("email")
    username = request.data.get("username")  # 유저명은 None도 허용. 즉, optional
    password1 = request.data.get("password1")
    # password2 = request.data.get('password2')  # password2는 validation에서만 사용하므로 주석처리

    # 기본 Validation check
    validation_result = validate_registration(
        RegistrationValidationValues(request)
    )
    if isinstance(validation_result, StandardErrorResponse):
        return validation_result

    # Validation check를 모두 통확하면 user_type에 따른 중복검사 진행
    users = CustomUser.objects.filter(email=email)
    if users.count() > 0:
        return StandardErrorResponse(
            detail=ValidationErrorStrs.email_exist,
            code="email_already_exists",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # user_type에 동일한 email이 없다면 회원 등록(create) 진행
    user = CustomUser.objects.create(
        email=email,
        username=username,
    )

    user.set_password(password1)
    user.save(update_fields=["password"])

    try:
        token_obj = Token.objects.create(user=user)
    except IntegrityError:
        token_obj = Token.objects.get(user=user)
    token = token_obj.key

    return Response({"token": token})
