from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import jwt


def generate_rsa_key_pair():
    # Generate an RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=4096, backend=default_backend()
    )

    # Extract the public key from the private key
    public_key = private_key.public_key()

    # Serialize the private key
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serialize the public key
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem_public_key.decode("utf-8"), pem_private_key.decode("utf-8")


def create_token_pair(payload, private_key, public_key):
    # Get the current time
    current_time = datetime.utcnow()

    # Create access token with expiration time of 2 days
    access_token = jwt.encode(
        {**payload, "exp": current_time + timedelta(days=2)},
        private_key,
        algorithm="RS256",
    )

    # Create refresh token with expiration time of 7 days
    refresh_token = jwt.encode(
        {**payload, "exp": current_time + timedelta(days=7)},
        private_key,
        algorithm="RS256",
    )

    return access_token, refresh_token
