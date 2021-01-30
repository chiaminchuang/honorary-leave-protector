import boto3
from botocore.exceptions import ClientError
from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY

def update_item(date, period, id, status):

    session = boto3.Session(
      aws_access_key_id=AWS_ACCESS_KEY,
      aws_secret_access_key=AWS_SECRET_KEY)

    dynamodb = session.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('status')

    table.put_item(Item={'id': f'{date}{period}-{id}', 'status': status})


# def get_one_item(id):

#     dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
#     table = dynamodb.Table('status')

#     try:
#         response = table.get_item(Key={'id': id})
#     except ClientError as e:
#         print(e.response['Error']['Message'])
#         return None
#     else:
#         return response.get('Item', None)

def get_batch_item(ids):

    dynamodb = boto3.client('dynamodb', region_name='us-east-2', 
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


# if __name__ == '__main__':
#     dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
#     table = dynamodb.Table('status')

#     table.put_item(Item={'id': '20210129-1100-096', 'status': '無發燒 無感冒 無飲酒 體溫36.1度', 'period': '20210129-1100'})
#     table.put_item(Item={'id': '20210129-1100-097', 'status': '無發燒 無感冒 無飲酒 體溫36.1度', 'period': '20210129-1100'})

#     get_item('20210129-1100')
