from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from models.eventbridge_models import EventbridgeEvent

class PaymentDetail(BaseModel):
    payment_method: str
    amount: int

    def to_dict(self) -> dict:
        result: dict = {
            "payment_method" : self.payment_method,
            "amount": self.amount
        }
        return result

class ReceiptLine(BaseModel):
    price: int
    product_id: str
    quantity: int
    category: str
    subcategory: str

    def to_dict(self) -> dict:
        result: dict = {
            "price": self.price,
            "product_id": self.product_id,
            "quantity" : self.quantity,
            "category" : self.category,
            "subcategory" : self.subcategory
        }
        return result

class Source(BaseModel):
    pos_id: str
    cashier_id: str
    store_id: str
    channel_id: str
    partner_id: int

    def to_dict(self) -> dict:
        result: dict = {
            "pos_id" : self.pos_id,
            "cashier_id" : self.cashier_id,
            "store_id" : self.store_id,
            "channel_id" : self.channel_id,
            "partner_id" : self.partner_id
        }
        return result

class SpinTransaction(BaseModel):
    card_transaction_id: str
    card_last_four_digits: str
    amount: int
    created_at: datetime

    def to_dict(self) -> dict:
        result: dict = {
            "card_transaction_id" : self.card_transaction_id,
            "card_last_four_digits" : self.card_last_four_digits,
            "amount" : self.amount,
            "created_at" : self.created_at
        }
        return result

class PosReceipt(BaseModel):
    payment_details: List[PaymentDetail]
    receipt: List[ReceiptLine]
    source: Source
    ticket_id: str
    total_imp: int
    spin_transaction: SpinTransaction
    
    def to_dict(self) -> dict:
        result: dict = {}
        result["payment_details"] = [x.to_dict() for x in self.payment_details]
        result["receipt"] = [x.to_dict() for x in self.receipt]
        result["source"] = self.source.to_dict()
        result["ticket_id"] = self.ticket_id
        result["total_imp"] = self.total_imp
        result["spin_transaction"] = self.spin_transaction.to_dict()
        return result
    
    @property
    def dd_tags(self) -> List[str] :
        return [
            f'pos.pos_id:{self.source.pos_id}',
            f'pos.store_id:{self.source.store_id}',
            f'pos.channel_id:{self.source.channel_id}',
            f'pos.partner_id:{self.source.partner_id}'
        ]


class PosReceiptEvent(EventbridgeEvent):
    detail: PosReceipt

    @property
    def dd_metric_name(self) -> str :
        return "pos.receipt.received"
    
    @property
    def dd_metric_value(self) -> int :
        return self.detail.total_imp

    @property
    def dd_tags(self) -> List[str] :
        return self.detail.dd_tags

    def to_db_key(self) -> dict:
        result: dict = {
            "id" : self.detail.spin_transaction.card_transaction_id,
        }
        return result
    
    def to_db_properties(self) -> dict:
        result: dict = {
            "id" : self.detail.spin_transaction.card_transaction_id,
            "receipt" : self.detail.to_dict(),
            "receipt_received_at" : self.time.timestamp()
        }
        return result