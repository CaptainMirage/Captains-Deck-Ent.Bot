import requests
import json
import inspect
from discord import app_commands, Intents, Client, Interaction
from colorama import Fore, Style, just_fix_windows_console
just_fix_windows_console()

logo = f"""
{Fore.LIGHTBLUE_EX}       {Fore.GREEN}cclloooooooooooooo.
{Fore.LIGHTBLUE_EX},;;;:{Fore.GREEN}oooooooooooooooooooooo.
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}oooooo{Fore.WHITE}kKXK{Fore.GREEN}ooo{Fore.WHITE}NMMWx{Fore.GREEN}ooooo:..
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}oooooo{Fore.WHITE}XMMN{Fore.GREEN}oooo{Fore.WHITE}XNK0x{Fore.GREEN}dddddoo
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}looo{Fore.WHITE}kNMMWx{Fore.GREEN}ooood{Fore.BLUE}xxxxxxxxxxxxxo
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}ld{Fore.WHITE}kXXXXK{Fore.GREEN}ddddd{Fore.BLUE}xxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.BLUE}ldxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx{Fore.RESET}
"""

print(logo + inspect.cleandoc(f"""
    Hey, welcome to the active developer badge bot.
    Please enter your bot's token below to continue.

    {Style.DIM}Don't close this application after entering the token
    You may close it after the bot has been invited and the command has been run{Style.RESET_ALL}
"""))

try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

while True:
    token = config.get("token")
    
    try:
        r = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": f"Bot {token}"}
        )
        data = r.json()
    except requests.exceptions.RequestException as e:
        if e.__class__ == requests.exceptions.ConnectionError:
            exit(
                f"{Fore.RED}ConnectionError{Fore.RESET}: "
                "Discord is commonly blocked on public networks, "
                "please make sure discord.com is reachable!"
            )

        elif e.__class__ == requests.exceptions.Timeout:
            exit(
                f"{Fore.RED}Timeout{Fore.RESET}: "
                "Connection to Discord's API has timed out "
                "(possibly being rate limited?)"
            )

        exit(f"Unknown error has occurred! Additional info:\n{e}")

    if data.get("id", None):
        break

    print(
        f"\nSeems like you entered an {Fore.RED}invalid token{Fore.RESET}. "
        "Please enter a valid token (see Github repo for help)."
    )

    config.clear()

with open("config.json", "w") as f:
    config["token"] = token
    json.dump(config, f, indent=2)

class FunnyBadge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """ This is called when the bot boots, to setup the global commands """
        await self.tree.sync()

client = FunnyBadge(intents=Intents.none())

@client.event
async def on_ready():
    """
    This is called when the bot is ready and has a connection with Discord
    It also prints out the bot's invite URL that automatically uses your
    Client ID to make sure you invite the correct bot with correct scopes.
    """
    if not client.user:
        raise RuntimeError("on_ready() somehow got called before Client.user was set!")

    print(inspect.cleandoc(f"""
        Logged in as {client.user} (ID: {client.user.id})

        Use this URL to invite {client.user} to your server:
        {Fore.LIGHTBLUE_EX}https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot{Fore.RESET}
    """), end="\n\n")

@client.tree.command()
async def yourwelcome(interaction: Interaction):
    """ Says hello or something """
    print(f"> {Style.BRIGHT}{interaction.user}{Style.RESET_ALL} used the command.")
    await interaction.response.send_message(inspect.cleandoc(f"""
        Hi **{interaction.user.display_name}**, thank you for saying hello to me.

        > __**Where's my badge?**__
        > Eligibility for the badge is checked by Discord in intervals,
        > at this moment in time, 24 hours is the recommended time to wait before trying.

        > __**It's been 24 hours, now how do I get the badge?**__
        > If it's already been 24 hours, you can head to
        > https://discord.com/developers/active-developer and fill out the 'form' there.
    """))

client.run(token)
