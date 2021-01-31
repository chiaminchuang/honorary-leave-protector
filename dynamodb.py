import boto3
from botocore.exceptions import ClientError
from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY

def update_item(date, period, id, status):

    dynamodb = boto3.client('dynamodb', 
      region_name='us-east-2', 
      aws_access_key_id=AWS_ACCESS_KEY,
      aws_secret_access_key=AWS_SECRET_KEY)

    dynamodb.put_item(TableName='status', Item={'id': {'S': f'{date}{period}-{id}'}, 'status': {'S': status}})


def get_batch_item(ids):

    dynamodb = boto3.client('dynamodb', 
      region_name='us-east-2', 
      aws_access_key_id=AWS_ACCESS_KEY,
      aws_secret_access_key=AWS_SECRET_KEY)    

    keys = [{'id': {'S': id}} for id in ids]
    try:
        response = dynamodb.batch_get_item(RequestItems={'status': {"Keys": keys}})
    except ClientError as e:
        print(e.response['Error']['Message'])
        return []
    else:
        return response['Responses'].get('status', [])
