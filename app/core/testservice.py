from dataclasses import dataclass


@dataclass
class TestService:
    def hello(self) -> str:
        return "hello"
