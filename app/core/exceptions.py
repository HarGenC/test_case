class WalletNotFoundError(Exception):
    """Wallet not found"""
    def __init__(self, wallet_uuid: str):
        self.wallet_id = wallet_uuid
        super().__init__(f"Wallet {wallet_uuid} not found")

class InvalidBalanceError(Exception):
    """Invalid initial balance"""
    def __init__(self, balance):
        self.balance = balance
        super().__init__(f"Invalid balance: {balance}")

class InsufficientFundsError(Exception):
    """Insufficient funds"""
    def __init__(self, balance: int, amount: int):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds: balance={balance}, amount={amount}")