from common.http_status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED


uploaded_successfully = {
    "status_code": HTTP_200_OK,
    "description": "Files uploaded successfully",
    "example": {
        "message": "Files uploaded successfully."
    },
}


retrieved_successfully = {
    "status_code": HTTP_200_OK,
    "description": "Files Retrieved successfully",
    "example": [{
        "file_extension": "jpg",
        "file_name": "andrey-stakhovskiy-VWLvZo8Gvcs-unsplash",
        "file_path": "/absolute/path/to/media/media/rgb/andrey-stakhovskiy-VWLvZo8Gvcs-unsplash.jpg",
        "file_type": "rgb",
        "upload_date": "Sun, 01 Sep 2024 07:31:18 GMT"
    },],
}




success_docs = {
    "status_code": HTTP_200_OK,
    "description": "user login in successfully",
    "example": {
        "message": "Files uploaded successfully."
    },
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
