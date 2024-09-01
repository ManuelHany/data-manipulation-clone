import os
from datetime import timedelta

DEBUG = bool(int(os.getenv("FLASK_DEBUG", 0)))
FLASK_APP = os.getenv("FLASK_APP", "app")
PROPAGATE_EXCEPTIONS = True
MEDIA = os.getenv("Media", "media")

API_TITLE = "Data Manipulation REST API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
API_SPEC_OPTIONS = {
    "security": [{"bearerAuth": []}],
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
}

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "381836fe163039ab7bcd0a84bf54dded9fbd4269"
)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

JSONIFY_PRETTYPRINT_REGULAR = True
