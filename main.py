import surviv
import datetime


def Load(data):
    time = datetime.datetime.now()
    print(f'{time} first data')

    for d in data:
        print(f'mapName: {d["mapName_tr"]}({d["mapName"]}) Number of teams: {d["teamMode"]} ')


def ModeChange(data):
    print('change mode')
    time = datetime.datetime.now()
    for d in data:
        print(time, f'mapName: {d["mapName_tr"]}({d["mapName"]}) Number of teams: {d["teamMode"]} ')


def main():
    s = surviv.ModeNotification()
    s.onLoad = Load
    s.onChnage = ModeChange

    # lang list 'as' 'eu' 'kr' 'na' 'sa'
    if not s.setLanguage('ko'):
        print('Start without translation.')

    if not s.init():
        return False

    if not s.Start():
        print('err')
        return False


if __name__ == '__main__':
    # surviv.test('ko')
    main()

