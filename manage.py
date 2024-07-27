from os import environ

from click import group

from bot.core import Myu


@group()
def main() -> None:
    """Initial entrypoint for the bot."""


@main.command()
def runbot() -> None:
    """Run the bot."""
    bot = Myu()
    token = environ["DISCORD_TOKEN"]

    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
