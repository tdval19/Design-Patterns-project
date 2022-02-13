from dataclasses import dataclass

from app.core.interactors.auth import IKeyEncoder, UserCredentials


@dataclass
class SimpleKeyEncoder(IKeyEncoder):
    secret_key: str = "KEY"

    def decode_key(self, key: str) -> UserCredentials:
        user_id = int(key.replace(self.secret_key, ""))
        return UserCredentials(user_id)

    def encode_key(self, credentials: UserCredentials) -> str:
        return self.secret_key + str(credentials.user_id)
