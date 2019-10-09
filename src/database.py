from server import db
from datetime import datetime


class SeoulCulturalEventInfo(db.Model):
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
    
    return intent

