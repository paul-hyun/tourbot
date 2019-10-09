from server import db
from datetime import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


class CulInfo(db.Model):
    __tablename__ = 'seoul_cultural_event_info'
    __table_args__ = {'mysql_collate': 'utf8_general_ci', 'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    CODENAME = db.Column(db.String(64), nullable=False)
    TITLE = db.Column(db.String(256), nullable=False)
    DATE = db.Column(db.String(64), nullable=False)
    PLACE = db.Column(db.String(64), nullable=False)
    ORG_NAME = db.Column(db.String(64), nullable=False)
    USE_TRGT = db.Column(db.String(128), nullable=False)
    USE_FEE = db.Column(db.String(256), nullable=False)
    PLAYER = db.Column(db.Text, nullable=False)
    PROGRAM = db.Column(db.Text, nullable=False)
    ETC_DESC = db.Column(db.Text, nullable=False)
    ORG_LINK = db.Column(db.String(512), nullable=False)
    MAIN_IMG = db.Column(db.String(256), nullable=False)
    RGSTDATE = db.Column(db.DateTime, nullable=False)
    TICKET = db.Column(db.String(64), nullable=False)
    STRTDATE = db.Column(db.DateTime, nullable=False)
    END_DATE = db.Column(db.DateTime, nullable=False)
    THEMECODE = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)


def get_cultural_event(intent):
    """
    DB에서 관련 정보 조회
    """
    '''
    [('INTENT', '검색'), ('DT_DAY', '내일'), ('LCP_COUNTY', '강남구'), 
    ('FD_ART', '판소리')]    '''
    # engine = create_engine(db, echo=True)
    # session = sessionmaker(bind=engine)
    # Base = declarative_base()
    # # 날짜, 지역, 종류, 장소

    # for instance in session.query(info):
    #     for i in range(5):
    #         rtn_instance = instance[i]

    tmp = []
    if intent.get('INTENT') == '검색':
        if intent.get('분류1'):
            cat1 = intent.get('분류1')
            tmp = CulInfo.query.filter(CulInfo.CODENAME.like(f"%{cat1}%")).all()
        else:
            tmp = CulInfo.query.all()
    return tmp


