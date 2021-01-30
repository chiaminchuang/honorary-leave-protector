import json
import pytz
import random
from datetime import datetime
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from dynamodb import get_batch_item, update_item

from settings import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, id_to_name

timezone_tw = pytz.timezone('Asia/Taipei')



def get_time_period():

    period0, period1, period2 = 11, 15, 20

    hour = int(datetime.now(timezone_tw).strftime('%H'))

    # 提早 2 小時回報
    if hour >= (period0 - 2) and hour < (period1 - 2):
        # 9 ~ 13
        return '11:00'
    elif hour >= (period1 - 2) and hour < (period2 - 2):
        # 13 ~ 18
        return '15:00'
    elif hour >= (period2 - 2) and hour <= 24:
        # 18 ~ 24
        return '20:00'
    else:
        # 0 ~ 9
        return 'oo:oo'


def get_title():
      period = get_time_period()
      date = datetime.now(timezone_tw).strftime('%m/%d')

      # 01/30 11:00 回報
      return f'{date} {period} 回報'


# def init_messages():

#     print('init messages')

#     global messages
#     start = 93
#     end = 107
#     messages = []
#     for id in range(start, end + 1):
#         id = str(id).zfill(3)  # 96 -> 096
#         messages.append([id])
    
def update(msg, use_default=True):

    # **096 在家 無發燒 體溫36.1度
    # *096 在家
    # *096

    msg = msg.strip().split(' ', 1)
    cmd = msg[0]
    
    date = datetime.now(timezone_tw).strftime('%Y%m%d')
    period = get_time_period().replace(':', '')
    id = str(cmd.strip('*')).zfill(3)

    if len(id) != 3 or not id.isdigit() or (id < '093' or id > '107'):
        # invalid id
        return False

    reset = len(msg) == 1
    if cmd.startswith('**'):
        status = msg[1] if not reset else ''
    elif cmd.startswith('*'):
        default = f' 無發燒 無感冒 無飲酒 體溫{random.uniform(36.1, 36.7):.1f}度'
        status = msg[1] + default if not reset else ''
    else:
      return False

    update_item(date, period, id, status)
    return True

def get_all():

    date = datetime.now(timezone_tw).strftime('%Y%m%d')
    period = get_time_period().replace(':', '')
    
    ids = [f'{date}{period}-{str(idx).zfill(3)}' for idx in range(93, 108)]
    items = get_batch_item(ids)

    messages = [str(idx).zfill(3) for idx in range(93, 108)]
    for item in items:
        id = item['id']['S'].split('-')[1]
        idx = messages.index(id)

        if item['status']['S']:
            messages[idx] = f"{id} {id_to_name[id]} {item['status']['S']}" 
    
    return messages
    


# def update_messages(new_msg, use_default=True):

#     update_item(period, status)

#     global messages
#     global to_send

#     new_msg[0] = new_msg[0].zfill(3)
#     # msg -> [id, name, status]
#     for idx, msg in enumerate(messages):
#         if msg[0] == new_msg[0]:
#             default = ['無發燒', '無感冒', '無飲酒', f'體溫{random.uniform(36.1, 36.7):.1f}度']
            
#             messages[idx] = new_msg + default if use_default and len(new_msg) > 1 else new_msg
#             to_send = True
#             break
    

# id name status
# 096 xxx 在家 無發燒
# to_send = False
# messages = []
# curr_period = get_time_period()
# init_messages()

def webhook(event, context):
    # global messages
    # global curr_period
    # global to_send

    to_send = False
    # period = get_time_period()
    # if curr_period != period:
    #     curr_period = period
    #     init_messages()

    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(CHANNEL_SECRET)


    events = json.loads(event['body'])['events']
    for e in events:
        reply_token = e['replyToken']
        # groupId = e['source']['groupId']
        text = e['message']['text'].strip()

        # if text.startswith('**'):
        #     # 使用自訂
        #     # **096 在家 無發燒 體溫36.1度
        #     msg = text[2:].strip().split(' ', 2)
        #     update_messages(msg, False)
        # elif text.startswith('*'):
        #     # 使用預設
        #     # *096 在家
        #     msg = text[1:].strip().split(' ', 2)
        #     update_messages(msg, True)

        to_send = to_send or update(text)
    # to_send = to_send or update('*096 出去玩')

    # text = '\n'.join([' '.join(msg) for msg in messages])
    text = '\n'.join(msg for msg in get_all())
    text = f'{get_title()}\n{text}'

    if to_send:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=text)
        )
    # line_bot_api.push_message(groupId, TextSendMessage(text=text))

    response = {
        "statusCode": 200,
        "body": json.dumps({"message": 'ok'})
    }

    return response

# if __name__ == '__main__':
#     webhook(None, None)