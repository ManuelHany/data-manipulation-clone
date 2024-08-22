from flask_jwt_extended import create_access_token, create_refresh_token


def create_access_and_refresh_token(user):
    identity = {
        "id": str(user["_id"]),
        "username": user["email"],
        "is_admin": user["is_admin"],
    }
    access = create_access_token(identity=identity)
    refresh = create_refresh_token(identity=identity)
    return {"access": access, "refresh": refresh}
