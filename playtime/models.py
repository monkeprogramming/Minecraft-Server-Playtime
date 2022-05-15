from playtime.logging import logger
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict
from datetime import datetime
import json


@dataclass
class Player:
    uid: str
    name: str


class TimeTrackDay(TypedDict):
    seconds_played: int


class PlayerTimeTrack(TypedDict):
    saved_hours: int
    days: dict[str, TimeTrackDay]


class PlaytimeDatabase:
    data: dict[str, PlayerTimeTrack] = {}
    datetime_format: str = '%m.%d.%Y'

    def __init__(self, path: Path):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        logger.debug('Loading database')
        self._check_database_file_exists()
        with open(self.path, 'r+') as f:
            data = json.load(f)
        return data

    def _check_database_file_exists(self):
        if not self.path.exists():
            with open(self.path, 'w+') as f:
                json.dump({}, f)

    def commit(self):
        logger.debug('Commiting database')
        with open(self.path, 'w+') as f:
            json.dump(self.data, f)

    def _ensure_date_exists_for_player_in_database(
        self, player: Player, date: datetime
    ):
        self._ensure_player_exists_in_database(player)
        if not date.strftime(self.datetime_format) in self.data[player.name]['days']:
            self.data[player.name]['days'][
                date.strftime((self.datetime_format))
            ] = TimeTrackDay(seconds_played=0)

    def _ensure_player_exists_in_database(self, player: Player):
        if player.name not in self.data:
            self._add_player_to_database(player)

    def _check_player_in_database(self, player: Player) -> bool:
        if player.name in self.data:
            return True
        return False

    def _add_player_to_database(self, player: Player):
        logger.debug(f'Adding player {player.name} to database')
        self.data[player.name] = PlayerTimeTrack(saved_hours=0, days={})
        self.commit()

    def add_playtime(self, player: Player, seconds: int, date: datetime):
        logger.debug(f'Adding {seconds} seconds of playtime for {player.name}')
        self._ensure_date_exists_for_player_in_database(player, date)
        current_time = self.get_playtime(player, date)
        self.data[player.name]['days'][date.strftime(self.datetime_format)][
            'seconds_played'
        ] = (current_time + seconds)
        self.commit()

    def get_playtime(self, player: Player, date: datetime) -> int:
        logger.debug(f'Getting playtime for {player.name}')
        self._ensure_date_exists_for_player_in_database(player, date)
        return self.data[player.name]['days'][date.strftime(self.datetime_format)][
            'seconds_played'
        ]
