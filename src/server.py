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

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://tourbot:tourbot123!@officelog.net/tourbot"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
import database
import telegram
import browser

try:
    import MeCab
    mecab = MeCab.Tagger('-d /home/chatbot/anaconda3/envs/chatbot/lib/mecab/dic/mecab-ko-dic')
except:
    pass


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
    chat_id, text = telegram.parse_input(message)

    # chatting을 실행한다.
    client_id, message_id, intent, data = do_chabot(chat_id, None, text)

    text = telegram.make_output(data)

    # send_message 함수에 두가지 변수를 전달
    telegram.send_output(chat_id, str(list(intent.items())))

    # 여기까지 오류가 없으면 서버상태 200 으로 반응
    return Response("Ok", status=200)


@app.route("/browser", methods=["POST"])
def post_browser():
    """
    브라우저 입력을 처리하는 함수
    """
    message = request.form["input"]
    logger.warning(f"recv from browser: {message}")

    # chatting을 실행한다.
    client_id, message_id, intent, data = do_chabot(None, None, message)

    text = browser.make_output(data)

    return jsonify({"output": text})


@app.route("/mecab", methods=["POST"])
def post_mecab():
    """
    mecab 형태소 분석
    """
    message = request.get_json()["input"]
    logger.warning(f"recv from mecab: {message}")

    morp = []
    node = mecab.parseToNode(message)
    while node:
        feature = node.feature.split(",")
        if feature[0] == "BOS/EOS":
            pass
        elif "+" not in feature[0]:
            value = dict()
            value[node.surface] = feature[0]
            morp.append(value)
        else:
            subs = feature[-1].split("+")
            for sub in subs:
                tokens = sub.split("/")
                value = dict()
                value[tokens[0]] = tokens[1]
                morp.append(value)
            pass
        node = node.next

    return jsonify({"output": morp})


def do_chabot(client_id, message_id, text):
    # entri api를 이용하여 entity를 조회 한다.
    dep, ner, morp, mecab = get_entity(text)
    logger.warning(f"recv from etri_dep: {dep}")
    logger.warning(f"recv from etri_ner: {ner}")
    logger.warning(f"recv from etri_morp: {morp}")
    logger.warning(f"recv from mecab: {mecab}")

    # entity를 이용해 intent 및 entity를 확정 한다.
    intent = get_intent(dep, ner, morp, mecab)

    # intent를 db를 조회한다
    output = database.get_cultural_event(intent)

    return client_id, message_id, intent, output


if __name__ == "__main__":
    logger.setLevel(logging.INFO)

    # log_handler = handlers.TimedRotatingFileHandler(filename="../log/tourbot.log", when="midnight", interval=1, encoding="utf-8")
    # log_handler.suffix = "%Y%m%d"
    # log_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s"))
    # logger.addHandler(log_handler)

    # logging.getLogger("werkzeug").setLevel(logging.WARNING)
    # logging.getLogger("urllib3").setLevel(logging.WARNING)
    # logging.getLogger("requests").setLevel(logging.WARNING)

    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run()

