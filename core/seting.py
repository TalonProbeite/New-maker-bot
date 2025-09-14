from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token : str
    admin_id : int 
    channel_id : int
    status : str
    openai_api : str


@dataclass
class Settings:
    bots : Bots


def get_settings(path:str):
    env = Env()
    env.read_env(path=path)


    return Settings(bots=Bots(
        bot_token=env.str("TOKEN"), 
        admin_id=env.int("ADMIN_ID"), 
        channel_id=env.int("CHANNEL_ID"),
        status=env.str("STATUS"),
        openai_api=env.str("OPENAI_API")))


settings = get_settings("core\input.env")
