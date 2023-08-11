import os
from model import Model
from models.eventbridge_models import EventbridgeEvent

class EventMatchs(Model):
    def __init__(self):
        super(EventMatchs, self).__init__(os.environ["TABLE_POC_EVENT_MATCHS"])
    
    def match(self, event : EventbridgeEvent) -> dict :
        return self.update(key=event.to_db_key(), properties=event.to_db_properties())

    def match_with_receipt(self, item : dict) -> bool :
        return 'transaction' in item and 'receipt' in item and (not 'accrual_receipt' in item)