import requests, datetime

T_TOKEN = #telegram bot token
X_TOKEN = #exchange rate api token
URL = 'https://api.telegram.org/bot%s/' % T_TOKEN
AMOUNT = 1

class update:
    def __init__(self):
        response = requests.get(URL + 'getUpdates')
        j = response.json()
        self.success = j['ok']
        result = j['result'][-1]
        self.update_id = int(result['update_id'])

        if 'message' not in result.keys():
            self.isMessage = False
        else:
            self.isMessage = True
            messageInfo = result['message']
            self.chat_id = messageInfo['chat']['id']
            self.text = messageInfo['text']

class message:
    def __init__(self, chat):
        self.chat_id = chat
        self.link = URL + 'sendMessage'

    def this(self, text):
        requests.post(url=self.link, data={'chat_id': self.chat_id, 'text': text}).json()

def reset(offset):
    requests.post(url=URL + 'getUpdates' + '?offset=%s' % str(offset + 1)).json()

def convert(give, get):
    url = 'https://openexchangerates.org/api/latest.json?app_id=%s&symbols=%s,%s' % (X_TOKEN, give, get)
    response = requests.get(url)
    j = response.json()
    data = j['rates']
    f = data[give]
    t = data[get]
    time = j['timestamp']
    now = (datetime.datetime.fromtimestamp(time).strftime('%H:%M'))
    xrate = t/f
    return '%.5f\nUpdated at %s' % (xrate, now)

def action():
    get = update()
    if not get.isMessage:
        reset(get.update_id)
        return

    command = get.text.startswith('/x')
    if command == False:
        reset(get.update_id)
        return

    reply = message(get.chat_id)
    arr = get.text.split()
    if len(arr) != 3:
        reply.this('the correct command is:\n/x FROM TO\ne.g. /x SGD AUD ')
    else:
        try:
            reply.this(convert(arr[1].upper(), arr[2].upper()))
        except KeyError:
            reply.this('pls input a valid currency')
    reset(get.update_id)

while (True):
    print('\nbot is running...')
    url = URL + 'getUpdates'
    while (True):
        result = requests.get(url)
        j = result.json()
        if j['result'] == []:
            continue
        break
    action()
