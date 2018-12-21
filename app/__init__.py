# coding=gbk
import re
import json
import pandas as pd
position = []

infos=[]
#到了11页面 还没解析
def parse(info):
    data = json.loads(info, strict=False)
    infos = data['result']["result"]
    for item in infos:
        content = {}
        a = item['id']
        b = re.sub(r'[0-9]', '', item['shortName'])
        content['url'] = 'https://www.icourse163.org/course/' + b + '-' + str(a)
        content['name'] = item['name']
        position.append(content)
for info in infos:
    parse(info)
data1 = pd.DataFrame(position)
data1.to_csv(r'url.txt', index=False, encoding='utf-8')
