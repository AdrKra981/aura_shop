import uuid
from decimal import Decimal
from uuid import UUID
from app.payments.base import PaymentProvider, PaymentResult


class FakePaymentProvider(PaymentProvider):
    async def charge(
        self,
        user_id: UUID,
        amount: Decimal,
        currency: str = "USD",
    ) -> PaymentResult:
        return PaymentResult(
            success=True,
            transaction_id=str(uuid.uuid4()),
        )
