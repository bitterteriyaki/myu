from click import group


@group()
def main() -> None:
    """Initial entrypoint for the bot."""


@main.command()
def runbot() -> None:
    """Run the bot."""
    print("Running the bot.")


if __name__ == "__main__":
    main()
