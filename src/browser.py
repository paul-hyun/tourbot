import os, sys, logging, json
logger = logging.getLogger()
import requests


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