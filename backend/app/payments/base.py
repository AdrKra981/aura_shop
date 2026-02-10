from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class PaymentResult:
    def __init__(self, success: bool, transaction_id: str | None = None):
        self.success = success
        self.transaction_id = transaction_id


class PaymentProvider(ABC):
    @abstractmethod
    async def charge(
        self,
        user_id: UUID,
        amount: Decimal,
        currency: str = "USD",
    ) -> PaymentResult:
        pass
