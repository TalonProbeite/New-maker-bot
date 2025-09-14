from openai import OpenAI
import json 





def get_ready_new(API,path="parsers\data\\new.json"):

    with open(path,"r",encoding="UTF-8") as file:
        new_dict = json.load(file)
        raw_new = new_dict['raw_new']

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API,
    )
    completion = client.chat.completions.create(
        model="qwen/qwen3-max",
        messages=[
            {
                "role": "user",
                "content": f"Сократи текст и не используй markdown: {raw_new}"
            }
        ],
        max_tokens=700,  # Добавьте лимит токенов
        
    )
    ready_new = completion.choices[0].message.content
    new_dict['ready_new'] = ready_new
    with open(path,"w",encoding="utf-8") as file:
        json.dump(new_dict, file, indent=2, ensure_ascii=False)
    


