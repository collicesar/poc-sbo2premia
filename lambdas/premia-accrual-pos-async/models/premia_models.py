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

class PremiaAccrualRequest(BaseModel):
    member_id : str
    medium_code : Optional[str]
    payment_details: List[PaymentDetail]
    receipt: List[ReceiptLine]
    source: Source
    ticket_id: str
    total_imp: int
    
    def to_dict(self) -> dict:
        result: dict = {}
        result["payment_details"] = [x.to_dict() for x in self.payment_details]
        result["receipt"] = [x.to_dict() for x in self.receipt]
        result["source"] = self.source.to_dict()
        result["ticket_id"] = self.ticket_id
        result["total_imp"] = self.total_imp
        result["member_id"] = self.member_id
        result["medium_code"] = self.medium_code
        return result
    
    @property
    def dd_tags(self) -> List[str] :
        return [
            f'premia.accrual_type:accrual_receipt',
            f'premia.member_identification_type:sbo_member_dentification',
            f'premia.source_type:sbo',
            f'premia.source_type:pos',
            f'premia.source_type:premia_integration',
            f'pos.pos_id:{self.source.pos_id}',
            f'pos.store_id:{self.source.store_id}',
            f'pos.channel_id:{self.source.channel_id}',
            f'pos.partner_id:{self.source.partner_id}'
        ]


