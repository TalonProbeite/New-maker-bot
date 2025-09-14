import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, date
from parsers.auxiliary_functions import clear_new , clear_saved_articles , get_image_name , is_article_not_published , clear_all



def get_raw_data_aoutomail() -> None:
    n = 1
    run = True
    while run:
        if n > 3:
            run = False
        response = requests.get(f"https://auto.mail.ru/news/?ajax=1&page={n}")
        if response.status_code == 200:
            result = response.json()
            results = result['results']
            current_date = datetime.now().strftime('%y-%m-%d')
            for article in results:
                if is_article_not_published(article['title']) and current_date == article['published']['rfc3339'][2:10]:
                    response = requests.get(article['href'])
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text,"lxml")
                        text = soup.find("div", "_04c969a8fb e7acc1d1ba _825a2995df").text 
                        paragraphs = soup.find_all("div", class_="ef94e532d1 _9cd6066c36",limit=5)
                        for paragraph in paragraphs:
                            text += paragraph.text
                        img_src = soup.find("img", class_="_4717005337 lazy")
                        if img_src is not None:
                            img_src = img_src.get("src")
                        else:
                            img_src = soup.find("img", class_="_4717005337 lazy _9663dffd6b").get("src")
                        response_img = requests.get(img_src)
                        image_name = get_image_name()
                        with open(f"parsers\data\\article_arts\{image_name}", 'wb') as file:
                            file.write(response_img.content)
                        with open("parsers\data\\new.json",'w',encoding='UTF-8') as file:
                           json.dump({"title":f"{article['title']}","raw_new":f"{text}", "img":f"{image_name}", "href":f"{article['href']}","ready_new":""},file ,indent=2, ensure_ascii=False)
                        run = False
                        break
        n += 1

    
def get_raw_data_tarantas()->None:
    n = 1
    run = True
    while run:
        if n> 3:
            run = False
        response = requests.get(f"https://tarantas.news/news?page={n}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            cart_list = soup.find_all("div",class_="listItemsWrapper")
            for cart in cart_list:
                title = cart.find("div",class_="listItemsName").text
                date = (cart.find("div",class_="listItemsDate").text)[0:10]
                current_date = datetime.now().strftime('%d.%m.%Y')
                if date == current_date and is_article_not_published(title=title):
                    href = cart.find("div",class_="listItemsVideoImg").find('a').get("href")
                    response_cart = requests.get(href)
                    if response_cart.status_code == 200:
                        soup_cart = BeautifulSoup(response_cart.text, "lxml")
                        text = soup_cart.find("p",class_="descr").text 
                        for  paragraph in soup_cart.find("div",class_="articleBody").find_all("p"):
                            text += paragraph.text
                        img_name = get_image_name()
                        img_src =  soup_cart.find("div",class_= "headBlock").find("img").get("srcset").split(",")[1].replace("1200w","").strip()
                        response_img = requests.get(img_src)
                        with open(f"parsers\data\\article_arts\{img_name}", 'wb') as file:
                            file.write(response_img.content)
                        with open("parsers\data\\new.json",'w',encoding='UTF-8') as file:
                           json.dump({"title":f"{title}","raw_new":f"{text}", "img":f"{img_name}", "href":f"{href}","ready_new":""},file ,indent=2, ensure_ascii=False)
                        run = False
                        break    
        n += 1

