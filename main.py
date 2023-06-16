import asyncio
import yaml
from datetime import datetime as dt
from telethon import TelegramClient, functions


def read_creds():
    with open('creds.yaml') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


async def get_content(client):
    """
    get ids of entities in crypt telegram folder
    """

    telegram_dir = 'Crypt'.lower()

    result = await client(functions.messages.GetDialogFiltersRequest())

    ids = set()
    for df in result:
        if (df := df.to_dict())['_'] == 'DialogFilter' and df['title'].lower() == telegram_dir:

            for item in df['pinned_peers'] + df['include_peers']:
                if item['_'] == 'InputPeerChannel':
                    ids.add(item['channel_id'])

    return ids


async def run(since):
    forward = False

    async with TelegramClient('anon', **read_creds()) as client:

        async with client:

            my_chat = await client.get_me()

            for id_ in await get_content(client):
                entity = await client.get_entity(id_)

                if entity.broadcast:  # get only channels

                    if entity.title in {'CryptoEarn Important', 'BlockSide', 'Gagarin Crypto'}:  # filter some entities

                        msgs = await client.get_messages(entity.id, offset_date=since, reverse=True, limit=3)

                        for msg in msgs:
                            if forward:
                                await client.forward_messages(my_chat, msg)
                            print(entity.title, msg.date)
                            print(msg.message)
                            print('\n\n<=============================>\n\n')


if __name__ == '__main__':
    since_time = dt(2023, 6, 14)
    asyncio.run(run(since_time))
