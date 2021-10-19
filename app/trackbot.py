import getopt
from config import API_SECRET, VK_TOKEN
import vk_api
import sys
from datetime import datetime as dt
import time
import requests

authkey = API_SECRET
api_session = vk_api.VkApi(token=VK_TOKEN)
vk = api_session.get_api()

def detect(argv):
    try:
        optlist, args = getopt.getopt(argv, 'x', ['target=', 'id='])
    except:
        print('error')
        sys.exit(2)
    print(optlist)
    first_iter( optlist[0][1], optlist[1][1] )

def first_iter(targetvk, id):
    info = vk.users.get(user_ids=targetvk, fields='online, last_seen', name_case='Nom', v=5.126)
    online = 1 if info[0]['online']==1 else 0
    last_seen = info[0]['last_seen']
    requests.post(f'http://127.0.0.1/test/{ last_seen["time"] }')
    if not online:
        requests.post(f'http://127.0.0.1/botapi/change?last_seen={last_seen["time"]}', data={
        'vkid':targetvk , 
        'id' : id, 
        'status': online, 
        'botkey': authkey
        }
    )
    track(targetvk, id)

def track(targetvk, id):
    last_state = None
    print(id)

    while True:
        try:
            status = requests.post('http://127.0.0.1/botapi/status', data={'vkid': targetvk, 'botkey':authkey}).json()['status']

            if status == 0:
                time.sleep(60)
                continue
            elif status == 1:
                pass

            current_time = str(dt.now().time().strftime('%H:%M:%S'))
            info = vk.users.get(user_ids=targetvk, fields='online', name_case='Nom', v=5.126)
            online = 1 if info[0]['online']==1 else 0
            
            if last_state == online:
                pass
            elif last_state != online:
                last_state = online
                requests.post('http://127.0.0.1/botapi/change', data={'vkid':targetvk ,'id' : id, 'status': online, 'botkey': authkey})
                
            print(f'Current Time: {current_time} Status: {"Online" if online==1 else "Offline"}')
        except Exception as e:
            pass
        time.sleep(60)


if __name__ == '__main__':
    detect(sys.argv[1:])
 