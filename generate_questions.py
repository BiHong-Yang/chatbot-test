import json
import time
import openai
import os
import re

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.docstore.document import Document

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = "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"


# Andrew mentioned that the prompt/ completion paradigm is preferable for this class
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def extract_json(text):
    try:
        # 从文本中提取 JSON 列表
        result_match = re.search(r"<result>(.*?)</result>", text, re.DOTALL)
        try:
            return result_match.group(1)   
        except:
            print("解析 JSON 失败。")
            return []             

    except json.JSONDecodeError:
        print("解析 JSON 失败。")
        return []


# # for each txt in ./context, open the file, read the content, and generate questions
# def run():
#     for filename in os.listdir('./contexts'):
#         if filename.split('.')[0]+'.json' in os.listdir('./questions'):
#             continue
#         print(f"Generating questions for {filename}")
#         with open(f'./contexts/{filename}', 'r', encoding='utf-8') as f:
#             textName=filename.split('.')[0]
#             content = f.read()

#             messages =  [  
# {'role':'user', 'content':f"""针对<article></article>中的这篇文章按下面的步骤进行操作：
# 1. 分点提取出能从文中获得的信息。
# 2. 对每个信息，设计一个针对该信息的问题
# 3. 把问题放入一个json格式的列表中，json放入<result></result>标签中；每个json对象有2个key:“information”代表提取的信息，“question”代表与之对应的问题

# 下面是文章：
# <article>
# {content}
# </article>"""},]

#     #         prompt = f"""
#     # 针对三引号中的这篇文章进行如下操作：
#     # 1. 分点提取出能从文中获得的信息。
#     # 2. 对每个信息，设计一个针对该信息的问题
#     # 3. 把问题放入一个json格式的列表中,每个json对象如下有2个key:“information”代表提取的信息,“question”代表与之对应的问题
#     # 文章: ```{content}```
#     #         """
#             # extract the json between the <result><\result> tags


#             response = get_completion_from_messages(messages=messages, temperature=0) 
#             # extract the json between the first and last square brackets
#             json_str = extract_json(response)
#             print(json_str)
#             json_res=json.loads(json_str)
#             result={
#                 "title":textName,
#                 "questions":json_res
#             }
#             # add "filename" key to each json object
#             # write the json to a file ./questions/filename.json
#             with open(f'./questions/{textName}.json', 'w', encoding='utf-8') as f:
#                 print(f"Writing to {textName}.json")
#                 json.dump(result, f, ensure_ascii=False, indent=4)
#                 f.close()

# dump the questions to a file
def dump_question(file,textName,result):
    # if questions file does not exist, create it
    if not os.path.exists(f'{file}/questions'):
        os.makedirs(f'{file}/questions')

    with open(f'{file}/questions/{textName}.json', 'w', encoding='utf-8') as f:
        print(f"Writing to {textName}.json")
        json.dump(result, f, ensure_ascii=False, indent=4)
        f.close()

def query_questions(content):
    # TODO deal with long content
    if len(content)>1000:
        return []
    messages =  [   
    {'role':'user', 'content':f"""针对<article></article>中的这篇文章按下面的步骤进行操作：
    1. 分点提取出能从文中获得的信息。
    2. 对每个信息，设计一个针对该信息的问题
    3. 把问题放入一个json格式的列表中，json放入<result></result>标签中；每个json对象有2个key:“information”代表提取的信息，“question”代表与之对应的问题

    下面是文章：
    <article>
    {content}
    </article>"""},]


    response = get_completion_from_messages(messages=messages, temperature=0) 
    # extract the json between the first and last square brackets
    print("response", response)
    json_str = extract_json(response)
    print(json_str)
    if len(json_str)==0:
        return []
    try:
        json_res=json.loads(json_str)
    except:
        json_res=json.loads(f"[{json_str}]")
    return json_res

def generate_questions(file):
    for filename in os.listdir(file):
        if not os.path.exists(f'{file}/questions'):
            os.makedirs(f'{file}/questions')

        if filename.split('.')[0]+'.json' in os.listdir(f'{file}/questions'):
            print(f"Skipping {filename}")
            continue
        # if is a folder,skip it
        if os.path.isdir(f'{file}/{filename}'):
            print(f"Skipping folder {filename}")
            continue

        print(f"Generating questions for {filename}")
        textName=filename.split('.')[0]
        result={"title":textName,"questions":[]}
            # for json_data
        if file=="json_data":
            with open(f'{file}/{filename}', 'r', encoding='utf-8') as f:
            #load json from f
                json_data=json.load(f)
                info=json_data['custom']['infoList']
                
                for i in info:
                    result["questions"].append({"information":i["kinfoContent"],"question":i["kinfoName"]})

                dump_question(file,textName,result)
                continue
        elif file=="wx_json":
            with open(f'{file}/{filename}', 'r', encoding='utf-8') as f:
            #load json from f
                json_data=json.load(f)
                qq=query_questions(json_data["title"]+"\n\n"+json_data["content"])
                result["questions"].extend(qq)
                dump_question(file,textName,result)
                continue
        # for other files like docs and pdfs
        else:
            if filename.split('.')[1]=="txt":
                continue
            if filename.split('.')[1]=="docx" or filename.split('.')[1]=="doc":
                # load from file using loader, then read the page_content from Document list
                loader = Docx2txtLoader(os.path.join(file, filename))
                pages = loader.load()
                print("doc loading" ,pages)
            elif filename.split('.')[1]=="pdf":
                # load from file using loader, then read the page_content from Document list
                loader = PyPDFLoader(os.path.join(file, filename))
                pages = loader.load()
                print("pdf loading" ,pages)
            for page in pages:
                qq=query_questions(page.page_content)
                result["questions"].extend(qq)
                # add "filename" key to each json object
                # write the json to a file ./questions/filename.json
            dump_question(file,textName,result)

def test():    
    text="""
{
    "information": "荆门市发布枯水蓝色预警",
    "question": "为什么荆门市发布了枯水蓝色预警？"
},
{
    "information": "漳河水库库水位已达蓝色预警标准",
    "question": "漳河水库的库水位达到了什么预警标准？"
},
{
    "information": "建议各地加强蓄水保水，科学调配水源，加强节水，广辟水源",
    "question": "荆门市水文水资源勘测局建议采取哪些措施来应对枯水蓝色预警？"
},
{
    "information": "地球上有72%的面积被水覆盖，可供人使用的淡水资源仅有不到2%",
    "question": "地球上的水资源分布情况如何？"
},
{
    "information": "家庭中有哪些水可以一水多用？",
    "question": "在家庭中，哪些水可以进行一水多用？"
},
{
    "information": "家庭节水小窍门有哪些？",
    "question": "在家庭中，有哪些节水的小窍门？"
},
{
    "information": "洗衣服时如何节水？",
    "question": "在洗衣服时，有哪些节水的方法？"
},
{
    "information": "使用厕所时如何节水？",
    "question": "在使用厕所时，有哪些节水的方法？"
},
{
    "information": "如何评价节水马桶？",
    "question": "根据什么标准来评价节水马桶？"
},
{
    "information": "洗车如何节水？",
    "question": "在洗车时，有哪些节水的方法？"
}
"""
    json_res=json.loads(text)
    print(json_res)

def run_generate():
    generate_questions("json_data")
    generate_questions("wx_json")
    generate_questions("context")

# for 20 times, each time sleep for 30 sec
# for i in range(10):
#     try:
#         run_generate()
#     except:
#         time.sleep(30)
#         continue

run_generate()
# test()