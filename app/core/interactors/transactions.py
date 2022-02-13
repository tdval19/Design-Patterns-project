from dataclasses import dataclass, field
from typing import List
from app.core.models.transaction import Transaction
from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import (
    ITransactionRepository,
    IWalletRepository,
)
from app.core.fee_strategy import IFeeStrategy, StandardFeeStrategy


@dataclass
class TransactionsInteractor:
    transaction_repository: ITransactionRepository
    wallet_repository: IWalletRepository
    fee_strategy: IFeeStrategy = field(default_factory=StandardFeeStrategy)

    def get_wallet_transactions(self, address: int) -> List[Transaction]:
        return self.transaction_repository.get_transactions_by_wallet_address(address)

    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        return self.transaction_repository.get_transactions_by_user_id(user_id)

    def make_transaction(
        self, transaction: Transaction, from_wallet: Wallet, to_wallet: Wallet
    ) -> None:
        fee = self.fee_strategy.get_fee(
            from_wallet.user_id, to_wallet.user_id, transaction.amount
        )
        if from_wallet.balance_btc < transaction.amount + fee:
            raise NotEnoughBitcoinsException(from_wallet.wallet_address)
        self.wallet_repository.update_wallet_balance(
            from_wallet.wallet_address,
            from_wallet.balance_btc - fee - transaction.amount,
        )
        self.wallet_repository.update_wallet_balance(
            to_wallet.wallet_address, to_wallet.balance_btc + transaction.amount
        )
        transaction.fee = fee
        self.transaction_repository.add(transaction)


class NotEnoughBitcoinsException(Exception):
    def __init__(self, wallet_address: int):
        self.message = "wallet with address: {} doesn't have enough bitcoins".format(
            wallet_address
        )
