import typer
from playtime.models import PlaytimeDatabase
from playtime.playtime import PlaytimeLoop
from playtime.logging import logger
import mctools
from pathlib import Path

app = typer.Typer()


@app.command()
def start(
    rcon_host: str = typer.Option(..., help='rcon fqdn or ip', envvar='RCON_HOST'),
    rcon_port: int = typer.Option(..., help='rcon port', envvar='RCON_PORT'),
    rcon_password: str = typer.Option(
        ..., help='RCON password', envvar='RCON_PASSWORD'
    ),
    refresh_time: int = typer.Option(60, help='refresh time in seconds'),
    weekday_playtime: int = typer.Option(120, help='weekday playtime in minutes'),
    player_json: Path = typer.Option(..., help="Path to the player json"),
):
    database = PlaytimeDatabase(player_json)
    ping = mctools.PINGClient(rcon_host, proto_num=0)
    rcon = mctools.RCONClient(rcon_host, port=rcon_port)

    logger.info(
        f'Logging into rcon {rcon_host}:{rcon_port} with password {rcon_password}'
    )
    if not rcon.login(rcon_password):
        raise SystemExit('RCON login failure')

    logger.info(f'Initializing PlaytimeLoop')
    loop = PlaytimeLoop(database, rcon, ping, refresh_time, weekday_playtime)
    loop.run()
