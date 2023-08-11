import logging
import os
import json
from model import Model

db_tx = Model(os.environ["TABLE_POC_EVENT_MATCHS"])
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def function_handler(event, _):
    print(event)
    try:
        logger.info(json.dumps(event))
        params   = event.get("queryStringParameters", {}) or {}
        key = {"id": params.get("id")}
        item = db_tx.get(key)

        if not item:
            return {
                "statusCode": 404,
                'body': json.dumps({}),
                'isBase64Encoded': False,
            }
        
        return {
            "statusCode": 200,
            'body': json.dumps(item),
            'isBase64Encoded': False,
        }

    except Exception as ex:
        logger.error(repr(ex))

    return {
            "statusCode": 500,
            'body': json.dumps({"message": "Server error"}),
            'isBase64Encoded': False,
        }
