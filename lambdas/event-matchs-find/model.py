import logging
import boto3
import json
import time
from decimal import *
from dynamodb_json import json_util
from decimalencoder import DecimalEncoder
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()


class Model:

    def __init__(self, name):
        self.name = name
        self.table = dynamodb.Table(name)

    def save(self, item):
        modified_at = int(time.time())
        item['modified_at'] = modified_at
        dynamodb_item = json.loads(json.dumps(item, cls=DecimalEncoder), parse_float=Decimal)
        return self.table.put_item(Item=dynamodb_item)

    def update(self, key, items):
        modified_at = int(time.time())
        values = {":modified_at" : modified_at}
        names = {"#modified_at" : "modified_at"}

        items = json.loads(json.dumps(items, cls=DecimalEncoder), parse_float=Decimal)
        update_expression = 'SET #modified_at=:modified_at'
        for key_item, value in items.items():
            if key_item in key:
                continue
            key_value = ':{}'.format(key_item)
            key_name = '#{}'.format(key_item)
            names[key_name] = key_item
            if len(update_expression) > 0:
                update_expression = '{}, {}={}'.format(update_expression, key_name, key_value)
            else:
                update_expression = 'SET {}={}'.format(key_name, key_value)
            values[key_value] = value
        item = self.table.update_item(Key=key, UpdateExpression=update_expression,
                                      ExpressionAttributeNames=names,
                                      ExpressionAttributeValues=values,
                                      ReturnValues="ALL_NEW")
        
        if item is not None and 'Attributes' in item:
            return json_util.loads(item['Attributes'])
        
        return None

    
    def delete(self, key):
        self.table.delete_item(Key=key)
        return True

    def query(self, key,  filters : dict = None, limit=100):
        condition = None

        for k,v in key.items():
            if not condition:
                condition = Key(k).eq(v)
            else:
                condition = condition & Key(k).eq(v)
        
        if filters:
            filter_condition = None

            for k,v in filters.items():
                if not filter_condition:
                    filter_condition = Attr(k).eq(v)
                else:
                    filter_condition = filter_condition & Attr(k).eq(v)

            response = self.table.query(
                KeyConditionExpression=condition,
                FilterExpression=filter_condition,
                Limit=limit
            )
        else:
            response = self.table.query(
                KeyConditionExpression=condition,
                Limit=limit
            )

        if response is not None and 'Items' in response:
            return json_util.loads(response['Items'])

        return []

    def get(self, key):
        item = self.table.get_item(Key=key)

        if item is not None and 'Item' in item:
            return json_util.loads(item['Item'])


    @staticmethod
    def convert_result(result):
        return json.loads(json.dumps(result, cls=DecimalEncoder), parse_float=Decimal)
