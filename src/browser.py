import os, sys, logging, json
logger = logging.getLogger()
import requests


def make_list(data, start=0):
    text = ""
    for item in data[start:start+5]:
        text += f'<p><a href="#" onclick="list_click({item.id})"><b>[ {item.CODENAME} ] [ {item.TITLE} ]</b></a></p>'
    return text


def make_detail(data):
    text = {'text': f'<b>[ {data[0].CODENAME} ] [ {data[0].TITLE} ]</b>' + '<br>' +
                    f'날짜 : {data[0].DATE}' + '<br>' +
                    f'장소 : {data[0].ORG_NAME} {data[0].PLACE}' + '<br>' +
                    f'연령 : {data[0].USE_TRGT}' + '<br>' +
                    f'요금 : {data[0].USE_FEE}' + '<br>' + '<br>' +
                    f'<a href="{data[0].ORG_LINK}" target = "_blank"><img src="{data[0].MAIN_IMG}" style="max-height: 360px; max-width: 360px; object-fit: contain" /></a>'
            }
    return text['text']

