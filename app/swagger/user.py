from common.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

success_docs = {
    "status_code": HTTP_201_CREATED,
    "description": "user created successfully",
    "example": {
        "message": "User created successfully",
        "user_id": "<user_id>",
        "user_email": "<user_email>",
    },
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

update_user_docs = {
    "status_code": HTTP_200_OK,
    "description": "update user info",
    "example": {"success": "User updated successfully."},
}

delete_user_docs = {
    "status_code": HTTP_204_NO_CONTENT,
    "description": "delete user",
}

user_list_sample = {
    "status_code": HTTP_200_OK,
    "description": "get user list",
    "example": {
        "number_of_pages": 1,
        "results": [
            {
                "_id": "667d0f00d8c088f2efd1ef28",
                "code": 112345,
                "country": "Egypt",
                "created_at": "Thu, 27 Jun 2024 07:04:32 GMT",
                "email": "admin4@admin.com",
                "first_name": "mousa",
                "last_name": "nageh",
                "updated_at": "Thu, 27 Jun 2024 07:11:29 GMT",
            },
        ],
    },
}
subscription_plan_created = {
    "status_code": HTTP_201_CREATED,
    "description": "create subscription plan",
    "example": {"created_plan": "str<id of plan>"},
}
platform_created = {
    "status_code": HTTP_201_CREATED,
    "description": "create subscription plan",
    "example": {"created_platform": "str<id of plan>"},
}

user_plan_created = {
    "status_code": HTTP_201_CREATED,
    "description": "create user plan",
    "example": {"user_plan_created": "str<id of plan>"},
}
subscription_plan_updated = {
    "status_code": HTTP_200_OK,
    "description": "update subscription plan",
    "example": {
        "_id": "66848f2e9529aef16ef94bff",
        "description": "this is plan 3",
        "months": 6,
        "name": "plan2",
        "price": 443.0,
        "updated_at": "Wed, 03 Jul 2024 00:28:32 GMT",
    },
}

platform_updated = {
    "status_code": HTTP_200_OK,
    "description": "update platform info",
    "example": {
        "_id": "66866e83029df367da82d820",
        "orchestrator_key": "Search_USA_Today_News",
        "platform": "USA Today",
    },
}
user_plan_list_sample = {
    "status_code": HTTP_200_OK,
    "description": "update subscription plan",
    "example": {
        "number_of_pages": 1,
        "results": [
            {
                "_id": "668521353aac37fa95f03e72",
                "created_at": "Wed, 03 Jul 2024 10:00:21 GMT",
                "is_expired": False,
                "subscription_plan": {
                    "_id": "66849660add6f37bf7224f73",
                    "created_at": "Wed, 03 Jul 2024 00:08:00 GMT",
                    "description": "this is plan 1",
                    "months": 6,
                    "name": "plan 2",
                    "price": 234.0,
                    "updated_at": "Wed, 03 Jul 2024 00:08:00 GMT",
                },
                "subscription_plan_id": "66849660add6f37bf7224f73",
                "updated_at": "Wed, 03 Jul 2024 10:00:21 GMT",
                "user_id": "667d0f00d8c088f2efd1ef28",
                "user_info": [
                    {
                        "code": 112345,
                        "country": "Egypt",
                        "created_at": "Thu, 27 Jun 2024 07:04:32 GMT",
                        "email": "admin4@admin.com",
                        "first_name": "mousa",
                        "last_name": "nageh",
                        "updated_at": "Thu, 27 Jun 2024 07:11:29 GMT",
                    }
                ],
            }
        ],
    },
}
subscription_plan_deleted = {
    "status_code": HTTP_204_NO_CONTENT,
    "description": "delete subscription plan",
}
platform_deleted = {
    "status_code": HTTP_204_NO_CONTENT,
    "description": "delete platform",
}
