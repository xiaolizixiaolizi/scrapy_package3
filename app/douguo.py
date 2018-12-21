import requests
import json
from multiprocessing import Queue
from handle_mongo import mongo_info
from  concurrent.futures import  ThreadPoolExecutor


queue_list = Queue()


def handel_request(url, data):
    headers = {
        "client": "4",
        "version": "6922.2",
        "device": "MI 6",
        "sdk": "22,5.1.1",
        "imei": "863254010805629",
        "channel": "zhuzhan",
        # "mac": "80:56:F2:41:9A:F9",
        "resolution": "720*1280",
        "dpi": "1.5",
        # "android-id": "8056f2419af97665",
        # "pseudo-id": "2419af976658056f",
        "brand": "Xiaomi",
        "scale": "1.5",
        "timezone": "28800",
        "language": "zh",
        "cns": "3",
        "carrier": "CHINA+MOBILE",
        # "imsi": "460078056242411",
        "user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; MI 6  Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
        "reach": "1",
        "newbie": "1",
        # "lon": "105.566938",
        # "lat": "29.99831",
        # "cid": "512000",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        # "Cookie": "duid=57999236",
        "Host": "api.douguo.net",
        # "Content-Length": "68",

    }
    response = requests.post(url=url, headers=headers, data=data)
    return response


def handle_index():  # 请求首页
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    data = {
        "client": "4",
        # "_session": "1544110484571863254010805629",
        # "v": "1503650468",时间戳
        "_vs": "2305"
    }
    response = handel_request(url, data)
    data = json.loads(response.text)

    for item in data['result']['cs']:
        for item1 in item['cs']:
            for item2 in item1['cs']:
                data1 = {
                    "client": "4",
                    # "_session": "1544160030317863254010805629",
                    "keyword": item2['name'],
                    "order": "3",
                    "_vs": "400",
                }

                # print(data1)
                queue_list.put(data1)


# 处理每一种菜谱
def handle_caipu_list(data):
    print('处理当前食材:', data['keyword'])
    # caiqu_list_url = ['http://api.douguo.net/recipe/v2/search/{}/20' .format(20*i) for i in range(10)]
    caiqu_list_url = 'http://api.douguo.net/recipe/v2/search/0/20'
    caiqu_list_response = handel_request(caiqu_list_url, data)
    cai_pu = json.loads(caiqu_list_response.text)
    for item in cai_pu['result']['list']:
        # print(item)

        cai_info = {}
        cai_info['shicai'] = data['keyword']

        if item['type'] == 13:
            cai_info['username'] = item['r']['an']
            cai_info['shicai_id'] = item['r']['id']
            cai_info['desc'] = item['r']['cookstory'].replace(' ', '').replace('\n', '')
            cai_info['caipu_name'] = item['r']['n']
            cai_info['rate'] = item['r']['rate']
            cai_info['recommendation'] = item['r']['recommendation_tag'].replace('人做过', '')
            cai_info['zuoliao'] = item['r']['major']

            detail_url = 'http://api.douguo.net/recipe/detail/{}'.format(cai_info['shicai_id'])
            detail_data = {
                "client": "4",
                # "_session": "1544160030317863254010805629",
                "author_id": "0",
                "_vs": "2803",
                "_ext": '{"query":{"kw":' + data['keyword'] + ',"src":"2803","idx":"1","type":"13","id":' + str(
                    cai_info['shicai_id']) + '}}'

            }
            detail_response = handel_request(url=detail_url, data=detail_data)

            detail_text = json.loads(detail_response.text)
            cai_info['tips'] = detail_text['result']["recipe"]["tips"]
            cai_info['cook_step'] = detail_text['result']["recipe"]["cookstep"]
            # print(json.dumps(cai_info))
            print('当前入库的菜谱是：',cai_info['caipu_name'])
            mongo_info.insert_item(cai_info)


# 请求首页
handle_index()
pool=ThreadPoolExecutor(max_workers=20)
while queue_list.qsize()>0:
    pool.submit(handle_caipu_list,queue_list.get())
# print(queue_list.qsize()) #看首页的数据一共有563条
# handle_caipu_list(queue_list.get())
