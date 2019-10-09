import os, sys, logging, json, urllib3, re
logger = logging.getLogger()
from datetime import datetime

from flask import Flask, request, Response, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from server import db
import database


def init_all():
    db.drop_all()
    db.create_all()

    items = set()
    http = urllib3.PoolManager()
    response = http.request("GET", "http://openapi.seoul.go.kr:8088/4f46587844616c733435657053446a/json/culturalEventInfo/0/999/")
    data = json.loads(response.data.decode("utf-8"))
    for row in data["culturalEventInfo"]["row"]:
        info = database.CulInfo()
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

if __name__ == "__main__":
    init_all()


