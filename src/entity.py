import os, sys, logging, json, urllib3, re
logger = logging.getLogger()

URL = "http://aiopen.etri.re.kr:8000/WiseNLU"
ACCESSKEY = "4ee51c5e-7d13-4f91-9516-5f68c4fe26f3"

def chk_keys(data):
    req_labels = []
    labels = ['VP', 'LC', 'DT', 'TI', 'NP_OBJ']
    for label in labels:
        if not label in data.keys():
            req_labels.append(label)
    
    return req_labels


def parse_ner(data):
    ner_data = json.loads(data)['return_object']['sentence'][0]['NE']
    ner_set = {}
    
    for i in range(len(ner_data)):
        ner = ner_data[i]['type'][:2]
        text = ner_data[i]['text']
        ner_set[ner] = text
    
    return ner_set


def parse_dep(data):
    dep_set = {}
    dep_data = json.loads(data)['return_object']['sentence'][0]['dependency']
    vp_ = re.compile('VP.*')
    for i in range(len(dep_data)):
        label = dep_data[i]['label']
        vp = vp_.match(label)
        if vp or label == 'NP_OBJ':
            dep_set[label] = dep_data[i]['text']
    
    return dep_set
    

def get_entity(text, code):
    URL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    ACCESSKEY = "4ee51c5e-7d13-4f91-9516-5f68c4fe26f3"

    requestJson = {
        "access_key" : ACCESSKEY,
        'argument' : {
            "text" : text,
            "analysis_code" : code['4]
            }
        }
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        URL,
        headers={
            "Content-Type":"application/json; charset=UTF-8"}, 
        body = json.dumps(requestJson)
        )
    # 함수로 Data를 다루면 함수 내에서 json.load() 필수
    data = str(response.data, "utf-8")
    
    dep = parse_dep(data)
    ner = parse_ner(data)
                                     
    return dict(dep, **ner)

code = {
    '0':'morp',     # 형태소 분석
    '1':'wsd',      # 어휘의미(동음이의어) 분석
    '2':'wsd_poly', # 어휘의미(다의어) 분석
    '3':'ner',      # 개체명 인식
    '4':'dparse',   # 의존 구문 분석
    '5':'srl'       # 의미역
}


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    text = "강남구에 9일날 7시에 진행하는 축제 알려줘"
    get_entity(text)                               
    # get_entity("영화표 1개 주세요")
    get_entity("주말에 갈 수 있는 관광지좀 알려줘")

