from playtime.models import PlaytimeDatabase
from playtime.models import Player
from mctools import RCONClient, PINGClient
from time import sleep
from datetime import datetime
from playtime.logging import logger


class PlaytimeLoop:
    def __init__(
        self,
        database: PlaytimeDatabase,
        rcon: RCONClient,
        ping: PINGClient,
        refresh_time: int,
        weekday_playtime: int,
    ):
        self.database = database
        self.rcon = rcon
        self.ping = ping
        self.refresh_time = refresh_time
        self.weekday_playtime = weekday_playtime

    def get_connected_players(self) -> list[Player]:
        playerlist: list[Player] = []

        logger.info(f'Getting server stats')
        try:
            stats = self.ping.get_stats()
        except IndexError as e:
            logger.warning(e)
            return playerlist

        logger.info(f'Getting player info')
        config_players = stats.get('players')
        if config_players:
            logger.info(f'Getting players on server')
            players = config_players.get('sample')
            if players:
                for player_info in players:
                    if len(player_info) >= 2:
                        new_player = Player(uid=player_info[1], name=player_info[0])
                        playerlist.append(new_player)
        return playerlist

    def kick_player(self, player: Player, msg: str):
        self.rcon.command(f'kick {player.name} {msg}')

    def add_time_to_player(self, seconds: int, player: Player):
        self.database

    def run(self):
        logger.info(f'Starting playtime loop')
        while True:
            players = self.get_connected_players()
            for player in players:
                self.database.add_playtime(player, self.refresh_time, datetime.now())
                if (
                    self.database.get_playtime(player, datetime.now())
                    > self.weekday_playtime * 60
                ):
                    logger.info(f'Playtime reached for player {player.name}')

            sleep(self.refresh_time)
            logger.info(f'Refreshing')
