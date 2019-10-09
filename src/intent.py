import json, collections, copy
from openpyxl import load_workbook


tag_list = None

def load_tag():
    """
    tag를 로딩 함
    """
    wb = load_workbook("../doc/config.xlsx")
    ws = wb["tag"]

    tag_idx = dict()
    tag_dic = dict()
    for _, row in enumerate(ws.rows, start=1):
        for c_idx, cell in enumerate(row, start=1):
            if cell.value is not None:
                tag_idx[c_idx] = cell.value.strip()
                tag_dic[cell.value.strip()] = ""
        break

    tag_list = []
    for r_idx, row in enumerate(ws.rows, start=1):
        if r_idx < 2: continue
        tag_ok = False
        tag_row = copy.deepcopy(tag_dic)
        for c_idx, cell in enumerate(row, start=1):
            if cell.value is not None and c_idx in tag_idx:
                tag = tag_idx[c_idx]
                tag_row[tag] = cell.value.strip()
                tag_ok = True
        if tag_ok:
            tag_list.append(tag_row)
    
    return tag_list


def get_intent(dep, ner, morp, mecab):
    """
    tag를 match 하여 intent를 파악 함
    """
    global tag_list
    if tag_list is None:
        tag_list = load_tag()

    intents = collections.OrderedDict()
    for tag_row in tag_list:
        match = dict()
        for tag_0, val_0 in tag_row.items():
            if tag_0 == "INTENT" or tag_0 == "VALUE" or val_0 == "": continue
            if tag_0 in match and match[tag_0]: continue
            match[tag_0] = ""
            for mmm in mecab:
                for val_1, tag_1 in mmm.items():
                    if not match[tag_0] and tag_0 == tag_1:
                        if val_0 == val_1: match[tag_0] = val_1
                        else: match[tag_0] = ""
        result = True
        value = None
        for tag_0, mat_0 in match.items():
            if not mat_0:
                result = False
                break
            else:
                value = mat_0
        if result and value:
            if tag_row["VALUE"] == "O":
                intents[tag_row["INTENT"]] = value
            else:
                intents["INTENT"] = tag_row["INTENT"]
    
    if "INTENT" in intents:
        for ne in ner:
            intents[ne["type"]] = ne["text"]
    return intents
