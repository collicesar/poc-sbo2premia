from datadog_lambda.metric import lambda_metric
from models.eventbridge_models import EventbridgeEvent

class DatadogHelper:

    @staticmethod
    def send_event_metric(event : EventbridgeEvent):
        lambda_metric(
            metric_name=event.dd_metric_name,
            value=event.dd_metric_value,
            tags=event.dd_tags
        )
