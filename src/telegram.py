import os, sys, logging, json
logger = logging.getLogger()
import requests


API_KEY = "key_of_telegram"


def parse_input(message):
    """
    telegram 에서 data 인자를 받아옴
    data 내부 구조를 이해해야 한다.
    Retuen :
    chat_id : 사용자 아이디 코드
    text : 사용자 대화 내용
    """
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]

    return chat_id, text


def send_output(chat_id, text):
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)

    params = {'chat_id': chat_id,
              'text': text,
              'parse_mode': 'HTML'}

    response = requests.post(url, json=params)

    print(response)
    return response

