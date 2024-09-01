from common.http_status_codes import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN
)


success_register_docs = {
    "status_code": HTTP_201_CREATED,
    "description": "user created successfully",
    "example": {
                   "message": "User created successfully",
                   "user_id": "<user_id>",
                   "user_email": "<user_email>",
               },
}


success_docs = {
    "status_code": HTTP_200_OK,
    "description": "user login in successfully",
    "example": {"access": "<access_token>", "refresh": "<refresh_token>"},
}

success_logout_docs = {
    "status_code": HTTP_200_OK,
    "description": "Successfully logged out",
    "example": {"message": "Successfully logged out"},
}

credentials_invalid_docs = {
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

invalid_token_docs = {
    "status_code": HTTP_401_UNAUTHORIZED,
    "description": "invalid token",
    "example": {
        "error": "invalid_token",
        "message": "Signature verification failed.",
    },
}
missing_token_docs = {
    "status_code": HTTP_401_UNAUTHORIZED,
    "description": "missing token",
    "example": {
        "description": "Request does not contain an access token.",
        "error": "authorization_required",
    },
}

unauthorized_docs = {
    "status_code": HTTP_403_FORBIDDEN,
    "description": "unauthorized request",
    "example": {
        "message": "You are not authorized to access this resource",
    },
}

refresh_token_failed_docs = {
    "status_code": HTTP_401_UNAUTHORIZED,
    "description": "refresh token",
    "example": {"error": "invalid_token", "message": "Signature verification failed."},
}

get_user_docs = {
    "status_code": HTTP_200_OK,
    "description": "getting user info",
    "example": {
        "_id": "6661b7f14b3589f6c76b1bc3",
        "created_at": "Thu, 06 Jun 2024 13:21:53 GMT",
        "email": "admin@admin.com",
        "is_admin": True,
        "updated_at": "Thu, 06 Jun 2024 13:21:53 GMT",
    },
}
