from pprint import pprint
import json
import requests
url = 'https://12345.jingmen.gov.cn/cns-bmfw-webrest/rest/mobileKinfo/getKnowInfoListOld'

data = {"token":"jm12345","params":{"kinfoName":"","sortType":"desc","currentPageIndex":1,"pageSize":20,"categoryCode":""}}
for i in range(305):
    print(i)
    data = {"token":"jm12345","params":{"kinfoName":"","sortType":"desc","currentPageIndex":i,"pageSize":20,"categoryCode":""}}
    # print(data)
    r = requests.post(url=url, json=data).json()
    # r = r["custom"]["infoList"]
    # print(r)
    # pprint(r)
    # r = json.dumps(r)
    # print(type(r))
    f2 =  open('json_data_raw/new_json_{}.json'.format(str(i)),'w',encoding='utf-8')
    json.dump(r, f2, ensure_ascii=False, indent=4)
    f2.close()
