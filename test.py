import requests
import sys

class MyError(Exception):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return self.err


def test(lang):
    try:
        langpack = requests.get(f'https://surviv.io/l10n/{lang}.json')
        if not langpack.headers['content-type'].startswith('application/json'):
            print('language data is not exist')

        langData = langpack.json()

        res = requests.get('https://surviv.io/api/site_info')
        if not res.headers['content-type'].startswith('application/json'):
            raise MyError('language data is not exist')

        data = res.json()
        if 'modes' not in data:
            raise MyError('json data parser error')

        data = data['modes']
        # [{'mapName': 'main', 'teamMode': 1}, {'mapName': 'main', 'teamMode': 2}, {'mapName': 'main', 'teamMode': 4}, {'mapName': 'potato', 'teamMode': 1}]

        for d in data:
            if 'mapName' not in d:
                raise MyError('json data mapName not exist')

            keyName = 'index-play-mode-' + d['mapName']
            if keyName not in langData:
                raise MyError('translation error')

            d['mapName_tr'] = langData[keyName]

        print("test is sucessful")
        return True

    except MyError as e:
        print("Error")
        print(e.err)

    except:
        print("Error")
        print(sys.exc_info())

    return False