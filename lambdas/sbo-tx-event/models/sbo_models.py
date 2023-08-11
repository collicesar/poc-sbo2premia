from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from models.eventbridge_models import EventbridgeEvent

class Transaction(BaseModel):
    card_transaction_id: str
    card_last_four_digits: int
    created_at: datetime = None
    amount: int
    member_id: str
    merchant_sponsor_id: str = None
    merchant_store_id: Optional[str] = None
    merchant_id: Optional[str] = None
    merchant_industry: Optional[str] = None
    arqc: Optional[str] = None
    medium_code: Optional[str] = None
    

    def to_dict(self) -> dict:
        result: dict = {
            "card_transaction_id" : self.card_transaction_id,
            "card_last_four_digits" : self.card_last_four_digits,
            "amount" : self.amount,
            "created_at" : self.created_at.isoformat(),
            "member_id" : self.member_id,
            "merchant_sponsor_id" : self.merchant_sponsor_id
        }
        if self.medium_code:
            result["medium_code"] = self.medium_code
        if self.merchant_id:
            result["merchant_id"] = self.merchant_id
        if self.merchant_industry:
            result["merchant_industry"] = self.merchant_industry
        if self.merchant_store_id:
            result["merchant_store_id"] = self.merchant_store_id
        if self.arqc:
            result["arqc"] = self.arqc
        return result
    
    @property
    def dd_tags(self) -> List[str] :
        tags = []
        if self.merchant_industry:
            tags.append(f'sbo.merchant_industry:{self.merchant_industry}')
        if self.merchant_sponsor_id:
            tags.append(f'sbo.merchant_sponsor_id:{self.merchant_sponsor_id}')
        if self.merchant_store_id:
            tags.append(f'sbo.merchant_store_id:{self.merchant_store_id}')


class SboEvent(EventbridgeEvent):
    detail: Transaction

    @property
    def dd_metric_name(self) -> str :
        return "sbo.transaction.received"
    
    @property
    def dd_metric_value(self) -> int :
        return self.detail.amount

    @property
    def dd_tags(self) -> List[str] :
        return self.detail.dd_tags

    def to_db_key(self) -> dict:
        result: dict = {
            "id" : self.detail.card_transaction_id,
        }
        return result
    
    def to_db_properties(self) -> dict:
        result: dict = {
            "id" : self.detail.card_transaction_id,
            "transaction" : self.detail.to_dict(),
            "tx_received_at" : self.time.timestamp()
        }
        return result