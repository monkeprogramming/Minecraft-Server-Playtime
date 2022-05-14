from mctools import RCONClient, PINGClient, QUERYClient
import os
import json
import time as time_module
import dotenv
from getpass import getpass

dotenv.load_dotenv()

HOST = os.getenv('RCON_HOST') or '185.208.204.244'
PORT = os.getenv('RCON_HOST') or 25575
PASW = os.getenv('RCON_PASSWORD') or getpass('rcon password: ')

rcon = RCONClient(HOST, port=PORT)
ping = PINGClient(HOST, proto_num=0)
time= time_module.localtime()
day = time[6] + 1
json_file = 'player_info.json'
testtext = 'test'

with open(json_file, mode='r') as read_file:
    data = json.load(read_file)


dict_of_players_with_time = {
    'time': time
}

stats = ping.get_stats()
config_players = stats.get('players')
players = config_players.get('sample')
if players:
    for player_info in players:
        player_id = player_info[1]
        if player_id in dict_of_players_with_time:
            print('seems to function')
        elif player_id is not dict_of_players_with_time:
            if day <= 5:
                dict_of_players_with_time[player_id]={
                    'time_left': 120
                }
            else:
                dict_of_players_with_time[player_id]={
                    'time_left': 240
                }
    print(dict_of_players_with_time)
else:
    dict_of_players_with_time['test']=testtext
    print(dict_of_players_with_time)

 



# if rcon.login(PASW):
#     resp = rcon.command('op spoderman&boman')
#     print(resp)
#     connected = rcon.is_connected
#     print(connected)