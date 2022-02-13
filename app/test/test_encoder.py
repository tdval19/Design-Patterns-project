import random

import pytest

from app.core.interactors.auth import UserCredentials, IKeyEncoder
from app.infra.encoder.dummy_encoder import SimpleKeyEncoder


@pytest.fixture
def encoder() -> IKeyEncoder:
    return SimpleKeyEncoder()


class TestEncoder:
    def test_encode_decode(self, encoder: IKeyEncoder) -> None:
        user_credentials = UserCredentials(1)
        decoded_key = encoder.decode_key(encoder.encode_key(user_credentials))
        assert decoded_key == user_credentials

    def test_with_random_id(self, encoder: IKeyEncoder) -> None:
        user_credentials = UserCredentials(random.randint(1, 99))
        decoded_key = encoder.decode_key(encoder.encode_key(user_credentials))
        assert decoded_key == user_credentials

    def test_chained_encode_decode(self, encoder: IKeyEncoder) -> None:
        user_credentials = UserCredentials(random.randint(1, 10))
        decoded_key = encoder.decode_key(encoder.encode_key(user_credentials))
        double_decoded_key = encoder.decode_key(encoder.encode_key(decoded_key))
        assert (
            decoded_key == user_credentials and double_decoded_key == user_credentials
        )
