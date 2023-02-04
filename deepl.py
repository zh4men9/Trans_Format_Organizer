import requests
import json
import argparse

parser = argparse.ArgumentParser(description='Deepl API')
parser.add_argument('--auth_key', '-a', help='authKey', required=False, default='YOUR_AUTH_KEY')
parser.add_argument('--source_lang', '-s', help='source language, Default: Auto', required=False, default='')
parser.add_argument('--text', '-t', help='text to translate', required=True)
parser.add_argument('--target_lang', '-l', help='target language, Default: ZH', required=False, default='ZH')
args = parser.parse_args()

auth_key = args.auth_key
text = args.text
target_lang = args.target_lang
source_lang = args.source_lang

def check_usage(auth_key):
    url = "https://api-free.deepl.com/v2/usage"
    headers = {
        "Host": "api-free.deepl.com",   
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "DeepL-Auth-Key {}".format(auth_key)
    }
    response = requests.post(url = url, headers = headers).text
    json_response = json.loads(response)
    character_count = json_response["character_count"]
    return character_count

def translate(auth_key, text, source_lang, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang,
        "source_lang": source_lang
    }

    headers = {
        "Host": "api-free.deepl.com",   
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "DeepL-Auth-Key {}".format(auth_key)
    }
    response = requests.post(url = url, data = data, headers = headers).text
    json_response = json.loads(response)
    json_response["usage"] = check_usage(auth_key)
    json_response["author"] = "https://github.com/missuo"
    print(json_response)

translate(auth_key, text, source_lang, target_lang)

