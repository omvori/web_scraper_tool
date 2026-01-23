import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from itertools import groupby
import json


## Implementazione web scraping

def scrape_web(website):
    
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("page loaded")
        time.sleep(5)

        html= driver.page_source

        return html
    
    finally:
        driver.quit()

def extract_body_content(html_content):
   
    soup = BeautifulSoup(html_content, "html.parser")

    body_content = soup.body

    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    
    soup = BeautifulSoup(body_content,"html.parser")

    for script_or_style in soup(["script","style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content


def split_dom_content(dom_contet,max_length = 6000):
    return [
        dom_contet[i:i + max_length] for i in range(0,len(dom_contet),max_length)
        
    ]


## Implementazione JSON
def sorted_id_content(input_data):
 
    if hasattr(input_data, 'to_dict'):
 
        data_list = input_data.to_dict(orient='records')
    elif isinstance(input_data, str):
        data_list = json.loads(input_data)
    else:
        data_list = input_data

    
    data_list.sort(key=lambda x: str(x['idRistorante']))

    grouped_reviews = {}
    
    
    for key, group in groupby(data_list, key=lambda x: str(x['idRistorante'])):
        grouped_reviews[key] = list(group)

    return grouped_reviews

def split_id_content(json_content, max_length=1000):
    if isinstance(json_content, dict):
        chunks = []
        for id_rist, reviews in json_content.items():
            single_chunk = json.dumps(
                {id_rist: reviews}, 
                ensure_ascii=False, 
                indent=2
            )
            
            if len(single_chunk) > max_length:
                reviews_limited = reviews[:5] 
                single_chunk = json.dumps(
                    {id_rist: reviews_limited}, 
                    ensure_ascii=False, 
                    indent=2
                )
            
            chunks.append(single_chunk)
        return chunks
    
    return []