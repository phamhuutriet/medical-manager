from ..models import *
from ..utils.token_generator import *
from ..core.enums import *


def create_user(user_data):
    user = MedicalUser.objects.create(
        username=user_data["username"],
        password=user_data["password"],
        display_name=user_data["displayName"],
        email=user_data["email"]
    )

    user.save()
    token_payload = {"username": user.username, "id": str(user.pk)}

    # Generate tokens
    public_key, private_key = generate_rsa_key_pair()
    access_token, refresh_token = create_token_pair(
        token_payload,
        private_key,
        public_key,
    )

    # Save tokens and keys
    key_token = KeyToken()
    key_token.user = user
    key_token.public_key = public_key
    key_token.refresh_token = refresh_token
    key_token.save()

    return {
        "headers": {
            f"HTTP_{Header.CLIENT_ID.value}": str(user.pk),
            f"HTTP_{Header.AUTHORIZATION.value}": access_token,
        },
        "user": user,
    }