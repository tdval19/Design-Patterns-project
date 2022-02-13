import random

from app.core.interactors.auth import UserCredentials
from app.infra.encoder.dummy_encoder import SimpleKeyEncoder


class TestEncoder:
    def test_encode_decode(self) -> None:
        user_credentials = UserCredentials(1)
        encoder = SimpleKeyEncoder()
        decoded_key = encoder.decode_key(encoder.encode_key(user_credentials))
        assert decoded_key == user_credentials

    def test_with_random_id(self) -> None:
        user_credentials = UserCredentials(random.randint(1, 99))
        encoder = SimpleKeyEncoder()
        decoded_key = encoder.decode_key(encoder.encode_key(user_credentials))
        assert decoded_key == user_credentials

    def test_chained_encode_decode(self) -> None:
        user_credentials = UserCredentials(random.randint(1, 10))
        encoder = SimpleKeyEncoder()
        decoded_key = encoder.decode_key(encoder.encode_key(user_credentials))
        double_decoded_key = encoder.decode_key(encoder.encode_key(decoded_key))
        assert decoded_key == user_credentials and double_decoded_key == user_credentials
