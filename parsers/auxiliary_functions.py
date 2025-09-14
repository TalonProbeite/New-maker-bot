import json



def is_article_not_published(title:str,path='parsers\data\saved_articles.json') -> bool:
    with open(path, 'r',encoding='utf-8') as file:
        saved_articles = json.load(file)
    for  artical in saved_articles:
        if title == artical:
            return False
    saved_articles.append(title)
    with open(path, 'w',encoding='utf-8') as file:
        json.dump(saved_articles, file, indent=2, ensure_ascii=False)
    return True


def clear_saved_articles(path='parsers\data\saved_articles.json') -> None:
    with open(path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=2, ensure_ascii=False)


def clear_new(path="parsers\data\\new.json"):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump({"title": "", "raw_new": "", "img":"","href":"","ready_new": ""}, file, indent=2, ensure_ascii=False)


def get_image_name(path="parsers\data\\new.json") -> str:
    with open(path,"r",encoding='UTF-8') as file:
        last_img = json.load(file)["img"]
    if last_img == "":
        return "1.jpg"
    else:
        return str(int(last_img.replace(".jpg",""))+1) + ".jpg"


def clear_all():
    clear_saved_articles()
    clear_new()


# def get_ready_new_text(path="parsers\data\\new.json")->str:
#     with open(path,"r",encoding="utf-8") as file:
#         new = json.load(file)["ready_new"]
#     return new


