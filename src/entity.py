def get_entity(text):
    """
    entri api를 이용하여 entity를 조회하고 반환한다.
    """
    URL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    ACCESSKEY = "4ee51c5e-7d13-4f91-9516-5f68c4fe26f3"
    CODE = "ner"
    '''
    형태소 분석 : “morp”,
    어휘의미 분석 (동음이의어 분석) : “wsd”
    어휘의미 분석 (다의어 분석) : “wsd_poly”
    개체명 인식 : “ner”
    의존 구문 분석 : “dparse”
    의미역 인식 : “srl”
    '''

    requestJson = {
    "access_key" : ACCESSKEY,
    'argument' : {
      "text" : text,
      "analysis_code" : CODE
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

    data = json.loads(str(response.data, "utf-8"))['return_object']['sentence'][0]['NE']
    print(data)
    ner_data = {}
    for i in range(len(data)):
    ner = data[i]['type'][:2]
    text = data[i]['text']
    ner_data[ner] = text

    return ner_data
    # entity = None
    # return entity
