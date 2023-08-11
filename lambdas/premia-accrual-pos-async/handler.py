import logging
import os
import json
from model import Model
from models.premia_models import PremiaAccrualRequest
from helpers.datadog_helper import DatadogHelper

db_tx = Model(os.environ["TABLE_POC_EVENT_MATCHS"])
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def function_handler(event, _):
    print(event)
    try:
        logger.info(json.dumps(event))
        
        if 'receipt' in event and 'transaction' in event:
            receipt = event["receipt"]
            tx = event["transaction"]

            receipt["member_id"] = tx.get("member_id")
            receipt["medium_code"] = tx.get("medium_code")

            accrual_request = PremiaAccrualRequest(**receipt)

            id = tx["card_transaction_id"]
            data = {"accrual_receipt" : accrual_request.to_dict()}
            item = db_tx.update(key={"id":id}, properties=data)
            points = int(accrual_request.total_imp * .05)

            DatadogHelper.lambda_metric(
                metric_name='premia.accrual.created',
                value=points,
                tags=accrual.dd_tags
            )

        return {"status_code": 200}

    except Exception as ex:
        logger.error(repr(ex))
