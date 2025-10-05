from datetime import datetime, timedelta
from io import BytesIO
import json
import os
import traceback

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from utils import translate_word, generate_sentence, check_testing_gpt
from shemas import WordItem, Settings, Testing
    
CONFIG_FILE = "config.json"
PROMPT_FILE = "prompts.json"
DATASET_NAME = 'data.csv'


LAST_ATTEMPT = 10
ATTEMPT_TIME = 0
LAST_ATTEMPT_TIME = 48 


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],    
)     


if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
            API_KEY = config_data.get("api_key", "")
            MODEL = config_data.get("model", "")
            BASE_URL = config_data.get("base_url", "")
            LANGUAGE = config_data.get("language", "")
    except (json.JSONDecodeError, IOError):
        config_data = {
            "api_key": "",
            "model": "gpt-4o-mini",
            "base_url": "https://api.proxyapi.ru/openai/v1",
            "language": "Russian"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
else:
    config_data = {
        "api_key": "",
        "model": "gpt-4o-mini",
        "base_url": "https://api.proxyapi.ru/openai/v1",
        "language": "Russian"
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)


if not os.path.exists(DATASET_NAME):
    df = pd.DataFrame(columns=['word', 'translate', 'count', 'sentence', 
                               'attempt', 'create_at', 'last_added_time',
                               'last_attempt_time', 'studied']).to_csv("data.csv", index=False)


@app.get("/")
def read_root():
    return {"Word Store"}


@app.post("/api/set-settings")
def set_settings(settings: Settings) -> dict:
    api_key, model, base_url, language = settings.api_key, settings.model, settings.base_url, settings.language
    if not api_key or len(api_key) > 40:
        raise HTTPException(status_code=400, detail="Invalid API key")
        
    if not model:
        raise HTTPException(status_code=400, detail="Invalid model name")
    
    if not base_url:
        raise HTTPException(status_code=400, detail="Invalid Base url")
    
    if not language:
        raise HTTPException(status_code=400, detail="Invalid language")
    
    try:
        global API_KEY, MODEL, BASE_URL, LANGUAGE
        API_KEY = api_key
        MODEL = model
        BASE_URL = base_url
        LANGUAGE = language

        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)

        config_data["api_key"] = API_KEY
        config_data["model"] = MODEL 
        config_data["base_url"] = BASE_URL
        config_data["language"] = LANGUAGE
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

        return {
            "msg": "Settings have been successfully set.",
            "model": model,
            "api_key_length": len(api_key),
            "base_url": base_url,
            "language": language
        }
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to set settings: {str(e)}")
    

@app.post("/api/add-word")
def add_word(word_item: WordItem) -> dict:
    word = word_item.word.lower()
    
    if not word or len(word) > 25:
        raise HTTPException(status_code=400, detail="Invalid word")
    
    if not all(c.isalpha() or c in ['-', ' '] for c in word):
        raise HTTPException(status_code=400, detail="Invalid word")
    
    words = word.split()
    if len(words) > 2:
        raise HTTPException(status_code=400, detail="Maximum 2 words allowed")
    
    for w in words:
        if not all(c.isalpha() or c == '-' for c in w):
            raise HTTPException(status_code=400, detail="Invalid word format")
    try:
        df = pd.read_csv(DATASET_NAME)
        if word not in df['word'].values:
            sentence = generate_sentence(word, LANGUAGE, PROMPT_FILE, API_KEY, BASE_URL, MODEL)
            translate = translate_word(word, LANGUAGE, PROMPT_FILE, API_KEY, BASE_URL, MODEL)
            new_row = {
                'word': word,
                'translate': translate,
                'count': 1,
                'sentence': sentence,
                'attempt': 0,
                'create_at': datetime.now(),
                'last_added_time': datetime.now(),
                'last_attempt_time': datetime.now()
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            df = df.sort_values('count', ascending=False)
            df.to_csv("data.csv", index=False)
            return {
                    "msg": "Word successfully set",
                    "word": word,
                    "translate": translate
                   }
        else:
            #TODO:studied
            df.loc[df['word'] == word, 'count'] += 1
            df.loc[df['word'] == word, 'last_added_time'] = datetime.now()

            df = df.sort_values('count', ascending=False)
            df.to_csv("data.csv", index=False)

            return {
                "msg": "Word successfully updated"
            }
        
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to add word: {str(e)}")
    

@app.get("/api/get-dataframe")
def get_dataframe():
    try:
        df = pd.read_csv(DATASET_NAME)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=data.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch DataFrame: {str(e)}")
    

@app.get("/api/get-settings")
def get_settings():
    try:
        return{
            "api_key": API_KEY,
            "model": MODEL,
            "base_url": BASE_URL,
            "language": LANGUAGE
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch DataFrame: {str(e)}")
    

@app.get("/api/get-most-frequent-words")
def get_most_frequent_words(count: int):
    if count < 0:
        raise HTTPException(status_code=400, detail="Invalid count")

    try:
        df = pd.read_csv(DATASET_NAME)

        df = df.sort_values('count', ascending=False).head(count)

        result = [{"word": row['word'],
                   "count": row['count'], 
                   "translate": row['translate']} 
                  for _, row in df.iterrows()]

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch words: {str(e)}")
    

@app.get("/api/get-testing")
def get_testing(count: int):
    try:
        df = pd.read_csv(DATASET_NAME)

        df = df.sort_values('count', ascending=False).head(count)

        testing_words = [{
            "word": row['word'],
            "translate": row['translate'],
            "attempt": row['attempt'],
            "last_attempt_time": row['last_attempt_time']
        }for _, row in df.iterrows()]

        result = []

        for testing_word in testing_words:
            last_attempt = testing_word['last_attempt_time']
    
            if isinstance(last_attempt, (int, float)):
                last_attempt = datetime.fromtimestamp(last_attempt)
            elif isinstance(last_attempt, str):
                last_attempt = datetime.fromisoformat(last_attempt.replace('Z', '+00:00'))

            if int(testing_word['attempt']) == LAST_ATTEMPT:
                if datetime.now() - last_attempt > timedelta(hours=LAST_ATTEMPT_TIME):
                    result.append(testing_word)

            if datetime.now() - last_attempt > timedelta(hours=ATTEMPT_TIME):
                result.append(testing_word)
        
        return result
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to fetch words: {str(e)}")
    

@app.post("/api/check-testing")
def check_testing(testing_items: Testing):
    if not testing_items:
        raise HTTPException(status_code=400, detail= "Invalid testingItems")
    
    try:
        results = []
        df = pd.read_csv(DATASET_NAME)
        for testing_item in testing_items.testing_array:
            result = check_testing_gpt(testing_item, PROMPT_FILE, API_KEY, BASE_URL, MODEL)

            mask = df['word'] == testing_item.target 
            
            if mask.any():
                if result == True:
                    df.loc[mask, 'attempt'] = df.loc[mask, 'attempt'] + 1
                else:
                    df.loc[mask, 'attempt'] = 0
                
                df.loc[mask, 'last_attempt_time'] = datetime.now()

            result_item = {"word": testing_item.target, "result": result}
            results.append(result_item)

        df.to_csv(DATASET_NAME, index=False)
        return {"message": "Testing checked successfully", "results": results}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to check testing: {str(e)}")
    
