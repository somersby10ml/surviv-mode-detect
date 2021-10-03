import requests
import schedule
import copy
import sys
import time

class MyError(Exception):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return self.err


class ModeNotification:
    def __init__(self):
        # private
        self.langData = {}
        self.oldData = []
        self.minutes = 30

        # public
        self.onLoad = None
        self.onChnage = None

    def setCycle(self, minutes) -> bool:
        """
        Set the frequency of data retrieval. (minute)
        Set it to 10 minutes or longer.
        default: 30 minutes
        :param minutes: Cycle time (minutes)
        :return: if success return true
        """
        if minutes < 10:
            print('Set it to 10 minutes or longer.')
            return False

        self.minutes = minutes
        return True

    def setLanguage(self, lang) -> bool:
        """
        Set the language to translate.
        :param lang: 'as'|'eu'|'kr'|'na'|'sa'
        :return: Whether the language is applicable
        """
        langpack = requests.get(f'https://surviv.io/l10n/{lang}.json')

        if not langpack.headers['content-type'].startswith('application/json'):
            print('language data is not exist')
            return False

        self.langData = langpack.json()
        return True

    def getData(self):
        """
        get mode data
        :return:
        """
        res = requests.get('https://surviv.io/api/site_info')
        if not res.headers['content-type'].startswith('application/json'):
            raise MyError('data parser error')

        data = res.json()
        if 'modes' not in data:
            raise MyError('json data parser error')

        data = data['modes']
        for d in data:
            if 'mapName' not in d:
                raise MyError('json data mapName not exist')

            if len(self.langData):
                keyName = 'index-play-mode-' + d['mapName']
                if keyName not in self.langData:
                    raise MyError('translation error')
                d['mapName_tr'] = self.langData[keyName]

            else:
                d['mapName_tr'] = ''

        return data

    def init(self):
        try:
            self.oldData = self.getData()

            if not callable(self.onChnage):
                print('please set onChange event')
                return False

            schedule.every(self.minutes).minutes.do(self.check)

            return True

        except MyError as e:
            print("Error")
            print(e.err)
        except:
            print("Error")
            print(sys.exc_info())
        return False

    def find(self, obj, data) -> bool:
        """
        A function that finds the same data in an array
        :param obj: array
        :param data: element in array
        :return: Returns true if found.
        """
        for i in obj:
            if i['mapName'] == data['mapName'] and i['teamMode'] == data['teamMode']:
                return True
        return False

    def check(self):
        newData = self.getData()
        diff = []
        for new in newData:
            if not self.find(self.oldData, new):
                diff.append(new)

        if callable(self.onChnage):
            if len(diff):
                self.onChnage(copy.deepcopy(diff))
        else:
            print('please set onChange event')

        self.oldData = newData

    def Start(self):
        if callable(self.onLoad):
            self.onLoad(copy.deepcopy(self.oldData))

        while True:
            schedule.run_pending()
            time.sleep(1)

