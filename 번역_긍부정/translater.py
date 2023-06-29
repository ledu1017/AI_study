from langdetect import detect
from translate import Translator
from textblob import TextBlob
import json

def translate(text):
    language = detect(text)
    if language != 'en':
        translator = Translator(to_lang='en', from_lang=language)
        translated_text = translator.translate(text)
    else:
        translated_text = text

    sentiment = TextBlob(translated_text).sentiment.polarity

    full_sent = "이 문장은 : " + language + " 영어로 번역하면 : " + translated_text
    if sentiment > 0:   
        full_sent += " 긍정 문장입니다."
        score = 1
    elif sentiment < 0:
        full_sent += " 부정 문장입니다."
        score = -1
    else:
        full_sent += " 중립 문장입니다."
        score = 0
    
    json_data = {"sentence": full_sent, "score": score}
    return json_data
