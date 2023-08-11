from typing import List
from datadog_lambda.metric import lambda_metric
from models.eventbridge_models import EventbridgeEvent

class DatadogHelper:

    @staticmethod
    def send_event_metric(metric_name : str, value : int, tags : List[str] ):
        lambda_metric(
            metric_name=metric_name,
            value=value,
            tags=tags
        )
