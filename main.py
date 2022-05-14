from mctools import RCONClient, PINGClient
from dataclasses import dataclass
from getpass import getpass
from time import sleep
import dotenv
import json
import os

dotenv.load_dotenv()

HOST = os.getenv('RCON_HOST') or '185.208.204.244'
PORT = os.getenv('RCON_HOST') or 25575
RCON_PASSWORD = os.getenv('RCON_PASSWORD') or getpass('rcon password: ')
REFRESH_TIME = 5
WEEKDAY_PLAYTIME = 60


@dataclass
class Player:
    uid: str
    name: str


def load_json(path: str) -> dict:
    with open(path, mode='r+') as f:
        data = json.load(f)
    return data


def dump_json(path: str, data):
    with open(path, mode='w+') as f:
        json.dump(obj=data, fp=f)


def kick_player(rcon: RCONClient, player: Player):
    print(f'kicking player{player.name}')
    rcon.command(f'kick {player.name}')


def connected_players(ping: PINGClient) -> list[Player]:
    playerlist = []
    stats = ping.get_stats()
    config_players = stats.get('players')
    players = config_players.get('sample')
    if players:
        for player_info in players:
            new_player = Player(uid=player_info[1], name=player_info[0])
            playerlist.append(new_player)
    return playerlist


while True:
    ping = PINGClient(HOST, proto_num=0)
    rcon = RCONClient(HOST, port=PORT)
    if not rcon.login(RCON_PASSWORD):
        raise ValueError('rcon login geht nicht')
    json_path = 'data/player_info.json'

    loaded_file = load_json(json_path)
    for player in connected_players(ping):
        if player.uid in loaded_file.keys():
            if loaded_file[player.uid] < WEEKDAY_PLAYTIME:
                old_time = loaded_file[player.uid]
                loaded_file[player.uid] = old_time + REFRESH_TIME
                dump_json(json_path, loaded_file)
            else:
                kick_player(rcon, player)
        else:
            loaded_file[player.uid] = REFRESH_TIME
            dump_json(json_path, loaded_file)

    sleep(REFRESH_TIME)
