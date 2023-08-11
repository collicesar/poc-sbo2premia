import boto3
import os
import json

lambda_async_name = os.environ["LAMBDA_PREMIA_ACCURAL_POS_ASYNC"]
client_lambda = boto3.client("lambda")

class LambdaHelper:

    @staticmethod
    def execute_accrual_pos_async(transaction : dict, receipt : dict):
        payload = {
            "transaction" : transaction,
            "receipt" : receipt
        }
        client_lambda.invoke(
            FunctionName=lambda_async_name,
            InvocationType="Event",
            LogType="Tail",
            Payload=json.dumps(payload),
        )
    
   