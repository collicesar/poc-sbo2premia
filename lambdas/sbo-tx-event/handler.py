import logging
from event_matchs import EventMatchs
from models.sbo_models import SboEvent
from helpers.datadog_helper import DatadogHelper
from helpers.lambda_helper import LambdaHelper

matcher = EventMatchs()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def function_handler(event, _):
    
    try:
        sbo_event = SboEvent(**event)
        
        # submit a custom metric
        DatadogHelper.send_event_metric(sbo_event)

        matches = matcher.match(sbo_event)

        if matcher.match_with_receipt(matches):
            transaction = matches.get("transaction")
            receipt = matches.get("receipt")
            
            # Execute pos accrual async
            LambdaHelper.execute_accrual_pos_async(transaction, receipt)
            logger.info("Accrual started")

        return {"status_code": 200}

    except Exception as ex:
        logger.error(repr(ex))




