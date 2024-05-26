import uuid
from abc import ABC, abstractmethod
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from boto3_type_annotations.dynamodb import ServiceResource, Table


class Repository(ABC):

    @property
    @abstractmethod
    def table_name(self) -> str:
        raise NotImplementedError()

    @property
    def dynamodb(self) -> ServiceResource:
        return boto3.resource('dynamodb')

    @property
    def table(self) -> Table:
        return self.dynamodb.Table(self.table_name)

    def list_items(self) -> List[dict]:
        return self.table.scan().get('Items', [])

    def find_by_id(self, pk: str) -> list:
        query = self.table.query(
            KeyConditionExpression=Key('id').eq(pk)
        )
        return query.get('Items', [])

    def create_item(self, pk: str, item: dict) -> dict:
        item.update({'id': pk})
        self.table.put_item(Item=item)

        return item

    def update_item(self, pk: str, **fields) -> dict:
        expression_fields = [f'{key} = :{key}' for key, _ in fields.items()]
        update_expression = 'SET ' + ', '.join(expression_fields)
        print(update_expression)

        expression_attribute_values = {f':{key}': value for key, value in fields.items()}

        return self.table.update_item(
            Key={'id': pk},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'
        )

    def delete_item(self, pk: str) -> dict:
        return self.table.delete_item(Key={'id': pk})
