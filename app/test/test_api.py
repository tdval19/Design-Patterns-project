import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.runner.setup import setup_test_api


@pytest.fixture(scope="module")
def api() -> FastAPI:
    return setup_test_api()


@pytest.fixture(scope="module")
def client(api: FastAPI) -> TestClient:
    client = TestClient(api)
    return client


class TestUser:
    def test_should_create_user(self, client: TestClient) -> None:
        response = client.post("/users")
        assert response.status_code == 200
        assert response.json() == {"key": "KEY1"}
        response = client.post("/users")
        assert response.status_code == 200
        assert response.json() == {"key": "KEY2"}


@pytest.fixture(scope="module")
def client_with_two_users(api: FastAPI) -> TestClient:
    client = TestClient(api)
    client.post("/users")
    client.post("/users")
    return client


class TestWallet:
    def test_should_raise_not_authorized(
        self, client_with_two_users: TestClient
    ) -> None:
        response = client_with_two_users.post("/wallets")
        assert response.status_code == 401
        response = client_with_two_users.post(
            "/wallets", headers={"key": "invalid_key"}
        )
        assert response.status_code == 401

    def test_should_create_wallets(self, client_with_two_users: TestClient) -> None:
        response = client_with_two_users.post("/wallets", headers={"key": "KEY1"})
        assert response.status_code == 200
        assert response.json()["address"] == 1
        response = client_with_two_users.post("/wallets", headers={"key": "KEY1"})
        assert response.status_code == 200
        response = client_with_two_users.post("/wallets", headers={"key": "KEY1"})
        assert response.status_code == 200

    def test_should_raise_bad_request(self, client_with_two_users: TestClient) -> None:
        response = client_with_two_users.post("/wallets", headers={"key": "KEY1"})
        assert response.status_code == 400

    def test_should_get_wallet(self, client_with_two_users: TestClient) -> None:
        response = client_with_two_users.get("/wallets/1", headers={"key": "KEY1"})
        assert response.status_code == 200
        assert response.json()["address"] == 1

    def test_should_raise_forbidden(self, client_with_two_users: TestClient) -> None:
        response = client_with_two_users.get("/wallets/1", headers={"key": "KEY2"})
        assert response.status_code == 403


@pytest.fixture(scope="module")
def client_with_two_wallets(api: FastAPI) -> TestClient:
    client = TestClient(api)
    client.post("/users")
    client.post("/users")
    client.post("/wallets", headers={"key": "KEY1"})
    client.post("/wallets", headers={"key": "KEY2"})
    return client


class TestTransaction:
    def test_should_raise_validation_error(
        self, client_with_two_wallets: TestClient
    ) -> None:
        response = client_with_two_wallets.post(
            "/transactions",
            headers={"key": "KEY1"},
            json={"wallet_address_from": 0, "wallet_address_to": 0, "amount_btc": 0},
        )
        assert response.status_code == 422

    def test_should_raise_forbidden(self, client_with_two_wallets: TestClient) -> None:
        response = client_with_two_wallets.post(
            "/transactions",
            headers={"key": "KEY1"},
            json={"wallet_address_from": 2, "wallet_address_to": 1, "amount_btc": 0.1},
        )
        assert response.status_code == 403

    def test_should_bad_request(self, client_with_two_wallets: TestClient) -> None:
        response = client_with_two_wallets.post(
            "/transactions",
            headers={"key": "KEY1"},
            json={"wallet_address_from": 1, "wallet_address_to": 2, "amount_btc": 1.1},
        )
        assert response.status_code == 400

    def test_should_raise_unauthorized(
        self, client_with_two_wallets: TestClient
    ) -> None:
        response = client_with_two_wallets.post(
            "/transactions",
            headers={"key": "invalid_key"},
            json={"wallet_address_from": 1, "wallet_address_to": 2, "amount_btc": 1.1},
        )
        assert response.status_code == 401

    def test_should_make_transaction(self, client_with_two_wallets: TestClient) -> None:
        response = client_with_two_wallets.post(
            "/transactions",
            headers={"key": "KEY1"},
            json={"wallet_address_from": 1, "wallet_address_to": 2, "amount_btc": 0.8},
        )
        assert response.status_code == 200


class TestStatistics:
    def test_should_raise_unauthorized(
        self, client_with_two_wallets: TestClient
    ) -> None:
        response = client_with_two_wallets.get(
            "/statistics", headers={"admin_key": "invalid_key"}
        )
        assert response.status_code == 401

    def test_should_return_zero_statistics(
        self, client_with_two_wallets: TestClient
    ) -> None:
        response = client_with_two_wallets.get(
            "/statistics", headers={"admin-key": "ADMIN_KEY"}
        )
        assert response.status_code == 200
        assert response.json() == {"num_of_transactions": 0, "total_profit": 0}

    def test_should_return_non_zero_statistics(
        self, client_with_two_wallets: TestClient
    ) -> None:
        client_with_two_wallets.post(
            "/transactions",
            headers={"key": "KEY1"},
            json={"wallet_address_from": 1, "wallet_address_to": 2, "amount_btc": 0.8},
        )
        response = client_with_two_wallets.get(
            "/statistics", headers={"admin-key": "ADMIN_KEY"}
        )
        assert response.status_code == 200
        assert response.json()["num_of_transactions"] == 1
        assert response.json()["total_profit"] != 0
