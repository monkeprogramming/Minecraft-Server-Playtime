import dotenv
from playtime.cli import app


def main() -> int:
    dotenv.load_dotenv()
    app()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
