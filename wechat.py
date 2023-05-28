import json
import requests
from bs4 import BeautifulSoup,element
import re
import os

def sanitize_filename(s):
    """
    Remove invalid characters and leading/trailing whitespace from filename.
    """
    s = s.strip()  # Remove leading/trailing whitespace
    s=re.sub(r'(?u)[^-\w.]', '', s) 
    s= "".join(c for c in s if c not in '/\\:*?"<>|')
    return s # Remove non-alphanumeric characters

def have_section(content_class):
    for child in content_class.children :
        if isinstance(child, element.Tag) and (child.name == 'section'):
            return True
    return False

def extend_section(content_class):
    article_sections = []
    if have_section(content_class)==True:
        for child in content_class.children :
            if isinstance(child, element.Tag) and (child.name == 'section'or child.name == 'p'):
                article_sections.extend(extend_section(child))
    else:
        if isinstance(content_class, element.Tag) and (content_class.name == 'p' or content_class.name == 'section'):
            article_sections.append(content_class)
    return article_sections

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # if the article has been deteled,return directly
    if soup.find('div',{'class':'weui-msg__title warn'}) is not None:
        print(f'{url} has been deleted')
        return

    # Find the title of the webpage from the h1 element
    title = sanitize_filename(soup.find('h1',{'id':'activity-name'}).text)

    # Find all sections with data-role="paragraph" within the 'page content' (you may need to adjust this based on actual webpage structure)
    # article_sections = soup.find('div', {'id': 'page-content'}).find_all('section', {'data-role': 'paragraph'})
    content_class = soup.find(class_='rich_media_content')
    article_sections = extend_section(content_class)

    # Extract the text from each section and join them together with newline characters
    article_content = '\n'.join([section.text for section in article_sections if section.text.strip()])
    # article_content = content_class.text

    if not os.path.exists('context'):
        os.makedirs('context')


    # Save the content to a .txt file named after the webpage title
    with open(f'context/{title}.txt', 'w', encoding='utf-8') as f:
        print(f'Saving {title}')
        f.write(article_content)
        f.close()

    # save json to wx_json folder, with keys:"url","title","content"
    with open(f'wx_json/{title}.json', 'w', encoding='utf-8') as f:
        print(f'Saving {title}')
        json.dump({"url":url,"title":title,"content":article_content},f,ensure_ascii=False,indent=4)
        f.close()

# Execute the function with the desired URL

def run():
    with open('input.txt', 'r', encoding='utf-8') as f:
        urls= f.readlines()

    # Remove any trailing newlines or spaces
    urls = [url.strip().split(" | ")[0] for url in urls]

    # Call the function for each URL
    for url in urls:
        scrape_website(url)

# scrape_website("https://mp.weixin.qq.com/s/TFaQzEkAk_vkaHGb1MGPmg")

run()

# extend section from ./test.html
# with open('test.html', 'r', encoding='utf-8') as f:
#     content_class = BeautifulSoup(f.read(), 'lxml')
#     article_sections = extend_section(content_class)
#     for section in article_sections:
#         print(section)
#         print('------------------')