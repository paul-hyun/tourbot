import os, sys, logging, json
logger = logging.getLogger()
import requests


API_KEY = "962492515:AAHrWqRx5lNl4t1oYGLg21-_ndpXnpG-tC8"


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
    """
    chat_id : 사용자 아이디 코드
    text : 사용자에게 보낼 메시지
    사용자에게 메세지를 보내는 내용의 함수
    """
    url = "https://api.telegram.org/bot{token}/sendMessage".format(token=API_KEY)
    # 변수들을 딕셔너리 형식으로 묶음
    params = {"chat_id": chat_id, "text": text}

    # Url 에 params 를 json 형식으로 변환하여 전송
    # 메세지를 전송하는 부분
    logger.warning(f"send to telegram: {params}")
    response = requests.post(url, json=params)
    return response


def make_output(data):
    """
    텔레그렘에 보낼 메시지 생성
    """
    return str(data)