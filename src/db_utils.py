import os, sys, logging, json, urllib3, re
logger = logging.getLogger()
from datetime import datetime

import database
from database import db


def init_all():
    db.drop_all()
    db.create_all()

    items = set()
    http = urllib3.PoolManager()
    response = http.request("GET", "http://openapi.seoul.go.kr:8088/4f46587844616c733435657053446a/json/culturalEventInfo/0/999/")
    data = json.loads(response.data.decode("utf-8"))
    for row in data["culturalEventInfo"]["row"]:
        info = database.SeoulCulturalEventInfo()
        info.CODENAME = row["CODENAME"]
        info.TITLE = row["TITLE"]
        info.DATE = row["DATE"]
        info.PLACE = row["PLACE"]
        info.ORG_NAME = row["ORG_NAME"]
        info.USE_TRGT = row["USE_TRGT"]
        info.USE_FEE = row["USE_FEE"]
        info.PLAYER = row["PLAYER"]
        info.PROGRAM = row["PROGRAM"]
        info.ETC_DESC = row["ETC_DESC"]
        info.ORG_LINK = row["ORG_LINK"]
        info.MAIN_IMG = row["MAIN_IMG"]
        info.RGSTDATE = datetime.strptime(row["RGSTDATE"], "%Y-%m-%d")
        info.TICKET = row["TICKET"]
        info.STRTDATE = datetime.strptime(row["STRTDATE"], "%Y-%m-%d %H:%M:%S.%f")
        info.END_DATE = datetime.strptime(row["END_DATE"], "%Y-%m-%d %H:%M:%S.%f")
        info.THEMECODE = row["THEMECODE"]
        info.created = datetime.now()
        info.updated = datetime.now()
        db.session.add(info)
        db.session.flush()
    db.session.commit()
    
def get_cultural_event(intent):
    """
    DB에서 관련 정보 조회    """
    '''
    [('INTENT', '검색'), ('DT_DAY', '내일'), ('LCP_COUNTY', '강남구'), 
    ('FD_ART', '판소리')]    '''
    db_id = 'mysql+pymysql://tourbot:tourbot123!@localhost/tourbot'
    engine = create_engine(db_id, echo=True)
    session = sessionmaker(bind=engine)
    Base = declarative_base()
    # 날짜, 지역, 종류, 장소

    for instance in session.query(info):
        for i in range(5):
            rtn_instance = instance[i]
    '''
    for row in session.query(info, info.name).all():
        print(row.User, row.name)    '''

    return rtn_instance


if __name__ == "__main__":
    init_all()

