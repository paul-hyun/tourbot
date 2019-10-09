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


# def send_output(chat_id, text):
#     """
#     chat_id : 사용자 아이디 코드
#     text : 사용자에게 보낼 메시지
#     사용자에게 메세지를 보내는 내용의 함수
#     """
#     url = "https://api.telegram.org/bot{token}/sendMessage".format(token=API_KEY)
#     # 변수들을 딕셔너리 형식으로 묶음
#     params = {"chat_id": chat_id, "text": text}
#
#     # Url 에 params 를 json 형식으로 변환하여 전송
#     # 메세지를 전송하는 부분
#     logger.warning(f"send to telegram: {params}")
#     response = requests.post(url, json=params)
#     return response


def send_output(chat_id, text):
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)

    params = {'chat_id': chat_id,
              'text': text,
              'parse_mode': 'HTML'}

    response = requests.post(url, json=params)

    print(response)
    return response


def make_output(data):
    '''
    데이터 파싱하여 아래 변수에 할당해야 됨
    '''

    CODENAME = '클래식'
    TITLE = "브람스 독일진혼곡"
    DATE = "2019-10-20~2019-10-20"
    PLACE = "콘서트홀"
    ORG_NAME = "서초구청"
    USE_TRGT = "8세 이상 관람"
    USE_FEE = "R석 10만원 / S석 7만원 / A석 5만원 / B석 3만원 / C석 2만원"
    PLAYER = ''
    PROGRAM = "브람스 독일진혼곡"
    ETC_DESC = ''
    ORG_LINK = "http://www.sac.or.kr/SacHome/perform/detail?searchSeq=37337#"
    MAIN_IMG = "http://culture.seoul.go.kr/data/ci/20190927141011.jpg"

    text = {'text': f'{CODENAME}' + '\n' +
                    f'{TITLE}' + '\n' +
                    f'{DATE}' + '\n' +
                    f'{PLACE}' + '\n' +
                    f'{ORG_NAME}' + '\n' +
                    f'{USE_TRGT}' + '\n' +
                    f'{USE_FEE}' + '\n' +
                    f'{PROGRAM}' + '\n' +
                    f'<a href="{ORG_LINK}">사이트</a>' + '\n' +
                    f'<a href="{MAIN_IMG}">Download</a>'}

    print(text['text'])
    return text['text']