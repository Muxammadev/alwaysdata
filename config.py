from environs import Env

env=Env()
env.read_env()

CHANNEL_ID=env.str("CHANNEL_ID")
BOT_TOKEN=env.str("BOT_TOKEN")
