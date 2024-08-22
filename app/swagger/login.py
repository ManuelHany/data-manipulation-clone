from common.http_status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED

success_docs = {
    "status_code": HTTP_200_OK,
    "description": "user login in successfully",
    "example": {"access": "<access_token>", "refresh": "<refresh_token>"},
}

unauthorized_docs = {
    "status_code": HTTP_401_UNAUTHORIZED,
    "description": "if not valid credentials",
    "example": {
        "code": HTTP_401_UNAUTHORIZED,
        "message": "not valid credentials",
        "status": "Unauthorized",
    },
}

refresh_token_docs = {
    "status_code": HTTP_200_OK,
    "description": "refresh token",
    "example": {"access": "<access_token>"},
}

refresh_token_failed_docs = {
    "status_code": HTTP_401_UNAUTHORIZED,
    "description": "refresh token",
    "example": {"error": "invalid_token", "message": "Signature verification failed."},
}
