from langchain.document_loaders.base import BaseLoader
from langchain.docstore.document import Document
import json
class json_loader(BaseLoader):

    def __init__(self) -> None:
        super().__init__()
    def load(self):
        docs = []
        for i in range(5):
            f = open('json_data/new_json_{}.json'.format(str(i)), 'r',encoding='utf-8')
            content = f.read()
            content = json.loads(content)
            for item in content:
                doc = Document(page_content=item['kinfoName']+'\n\n'+item['kinfoContent'],metadata={'url':"https://www.jingmen.gov.cn/col/col18658/index.html?kinfoGuid="+item['kinfoGuid']})
                docs.append(doc)
        return docs
loader = json_loader()
data = loader.load()
print(data[0])
print(len(data))