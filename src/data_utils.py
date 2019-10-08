import os, sys, logging, json, urllib3, re
logger = logging.getLogger()

URL = "http://aiopen.etri.re.kr:8000/WiseNLU"
ACCESSKEY = "4ee51c5e-7d13-4f91-9516-5f68c4fe26f3"

def chk_entities(data):
    req_labels = []
    labels = ['VP', 'LC', 'DT', 'TI', 'NP_OBJ']
    for label in labels:
        if not label in data.keys():
            req_labels.append(label)
    
    return req_labels


def parse_ner(data):
    ner_data = data['return_object']['sentence'][0]['NE']
    ner_set = {}
    
    for i in range(len(ner_data)):
        ner = ner_data[i]['type'][:2]
        text = ner_data[i]['text']
        if ner in ner_set.keys():
            ner_set[ner].append(text)
        else:
            ner_set[ner] = [text]
        
    
    return ner_set


def parse_dep(data):
    dep_set = {}
    dep_data = data['return_object']['sentence'][0]['dependency']
    vp_ = re.compile('VP.*')
    for i in range(len(dep_data)):
        label = dep_data[i]['label']
        text = dep_data[i]['text']
        vp = vp_.match(label)
        if vp or label == 'NP_OBJ':
            if label in dep_set.keys():
                dep_set[label].append(text)
            else:
                dep_set[label] = [text]
    
    return dep_set
    

def get_entity(text):
    URL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    ACCESSKEY = "4ee51c5e-7d13-4f91-9516-5f68c4fe26f3"

    requestJson = {
        "access_key" : ACCESSKEY,
        'argument' : {
            "text" : text,
            "analysis_code" : code['4']
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
    data = json.loads(response.data.decode("utf-8"))
    
    # dep = parse_dep(data)
    dep = data["return_object"]["sentence"][0]["dependency"]
    # ner = parse_ner(data)
    ner = data["return_object"]["sentence"][0]["NE"]
    morp = data["return_object"]["sentence"][0]["morp"]

    response = http.request(
        "POST",
        "https://www.officelog.net/mecab",
        headers={
            "Content-Type":"application/json; charset=UTF-8"}, 
        body = json.dumps({"input": text})
        )
    mmm = json.loads(response.data.decode("utf-8"))["output"]
    # mmm = str(json.loads(response.data.decode("utf-8"))["output"])
    print(mmm)
    # mmm = []
    
    # return dict(dep, **ner)
    return dep, ner, morp, mmm


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
    text = "강남구나 성동구에 10월 9일날 7시에 진행하는 축제 알려줘"
    print(get_entity(text))                            
    # get_entity("영화표 1개 주세요")
    get_entity("주말에 갈 수 있는 관광지좀 알려줘")

