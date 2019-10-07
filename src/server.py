import os, sys, logging, json
from io import StringIO
from logging import handlers
logger = logging.getLogger()

from data_utils import get_entity
from intent import get_intent

import requests
from flask import Flask, request, Response, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://tourbot:tourbot123!@localhost/tourbot"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
import database


API_KEY = "962492515:AAHrWqRx5lNl4t1oYGLg21-_ndpXnpG-tC8"


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/telegram", methods=["POST"])
def post_telegram():
    """
    텔레그램 입력을 처리하는 함수
    """
    message = request.get_json()
    logger.warning(f"recv from telegram: {message}")

    # parse_message 함수는 두가지 return 값을 가진다 (chat_id, text의)
    # 순서대로 chat_id, text의 변수로 받아준다.
    chat_id, text = parse_telegram(message)

    # chatting을 실행한다.
    client_id, message_id, text = do_chabot(chat_id, None, text)

    # send_message 함수에 두가지 변수를 전달
    send_telegram(chat_id, text)

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


@app.route("/browser", methods=["POST"])
def post_browser():
    """
    브라우저 입력을 처리하는 함수
    """
    message = request.form["input"]
    logger.warning(f"recv from browser: {message}")

    # chatting을 실행한다.
    client_id, message_id, text = do_chabot(None, None, message)

    return jsonify({"output": text})


def do_chabot(client_id, message_id, text):
    # entri api를 이용하여 entity를 조회 한다.
    dep, ner, morp, mecab = get_entity(text)
    logger.warning(f"recv from etri_dep: {dep}")
    logger.warning(f"recv from etri_ner: {ner}")
    logger.warning(f"recv from etri_morp: {morp}")
    logger.warning(f"recv from etri_mecab: {mecab}")

    send_str = StringIO()
    data = dict()
    for elm in dep:
        data[elm["label"]] = elm["text"]
    send_str.write(f"dep: {data}")
    data.clear()
    for elm in ner:
        data[elm["type"]] = elm["text"]
    send_str.write(f"\nner: {data}")
    data.clear()
    for elm in morp:
        data[elm["type"]] = elm["lemma"]
    send_str.write(f"\nmorp: {data}")
    data.clear()
    for elm in mecab:
        data[elm[1]] = elm[0]
    send_str.write(f"\nmecab: {data}")
    data.clear()

    # entity를 이용해 intent 및 entity를 확정 한다.
    get_intent(dep, ner, morp, mecab)

    return client_id, message_id, send_str.getvalue()


if __name__ == "__main__":
    logger.setLevel(logging.INFO)

    log_handler = handlers.TimedRotatingFileHandler(filename="../log/tourbot.log", when="midnight", interval=1, encoding="utf-8")
    log_handler.suffix = "%Y%m%d"
    log_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s"))
    logger.addHandler(log_handler)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run()

