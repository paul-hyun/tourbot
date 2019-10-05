import os, sys, logging, json
from io import StringIO
from logging import handlers
logger = logging.getLogger()

from entity import get_entity
from intent import get_intent

import requests
from flask import Flask, request, Response
app = Flask(__name__)


API_KEY = "962492515:AAHrWqRx5lNl4t1oYGLg21-_ndpXnpG-tC8"


@app.route("/", methods=["GET"])
def home():
    return "Welcome Tour Chatbot"


@app.route("/telegram", methods=["POST"])
def post_telegram():
    """
    텔레그램 입력을 처리하는 함수
    """
    message = request.get_json()
    logger.warning(f"recv from telegram: {message}")

    # parse_message 함수는 두가지 return 값을 가진다 (chat_id, msg)
    # 순서대로 chat_id, text의 변수로 받아준다.
    chat_id, text = parse_telegram(message)

    # entri api를 이용하여 entity를 조회 한다.
    entity = get_entity(text, "ner")
    send_str = StringIO()
    send_str.write(str(entity))

    # send_message 함수에 두가지 변수를 전달
    send_telegram(chat_id, send_str.getvalue())

    # 여기까지 오류가 없으면 서버상태 200 으로 반응
    return Response("Ok", status=200)


def parse_telegram(message):
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


def send_telegram(chat_id, text):
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


if __name__ == "__main__":
    logger.setLevel(logging.INFO)

    log_handler = handlers.TimedRotatingFileHandler(filename='../log/tourbot.log', when='midnight', interval=1, encoding='utf-8')
    log_handler.suffix = "%Y%m%d"
    log_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s"))
    logger.addHandler(log_handler)

    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("requests").setLevel(logging.ERROR)

    app.run()

