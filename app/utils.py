from openai import OpenAI
import json

def use_gpt(system: str, user: str, api_key: str, base_url="https://api.proxyapi.ru/openai/v1", 
            model="gpt-4o-mini", mode="json"):
    """API для взамодействия с GPT."""
    
    params = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    if mode == "json":
        params["response_format"] = {"type": "json_object"}
        params["messages"][0]["content"] = (
            "You are a helpful assistant designed to output JSON. " + system
        )
    
    with OpenAI(
        api_key= api_key,
        base_url=base_url,
    ) as client:
        chat_completion = client.chat.completions.create(**params)
        if mode == "json":
            return json.loads(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content
        

def translate_word(word, language, prompt_file,
                    api_key, base_url, model):
    with open(prompt_file, "r") as f:
        prompts = json.load(f)

    prompt = prompts['translate_word'].replace("[LANGUAGE]", language)
    user = "The word to translate: " + word

    translate = use_gpt(prompt, user, api_key, base_url, model)
    return translate['translate']


def generate_sentence(word, language, prompt_file,
                    api_key, base_url, model):
    with open(prompt_file, "r") as f:
        prompts = json.load(f)

    prompt = prompts['generate_sentence'].replace("[LANGUAGE]", language)
    user = "Target word: " + word

    result = use_gpt(prompt, user, api_key, base_url, model)
    return result['sentence']


def check_testing_gpt(testing_item, prompt_file,
                    api_key, base_url, model):
    with open(prompt_file, "r") as f:
        prompts = json.load(f)

    prompt = prompts['check_testing']
    user = "Target word: " + testing_item.target + "Translation:" + testing_item.user_try

    result = use_gpt(prompt, user, api_key, base_url, model)
    return result['valid']