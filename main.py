import asyncio
import yaml
from telethon import TelegramClient, events
from telethon import functions, types
from datetime import datetime as dt


def read_creds():
    with open('creds.yaml') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


# @client.on(events.NewMessage(chats='cardboty'))
# async def my_event_handler(event):
#     print(event.message.message)


# client.start()
# client.run_until_disconnected()

async def get_crypt_content(client):
    """
    get ids of entities in crypt telegram folder
    """

    folder_name = 'Crypt'.lower()

    result = await client(functions.messages.GetDialogFiltersRequest())

    ids = set()
    for df in result:
        if (df := df.to_dict())['_'] == 'DialogFilter' and df['title'].lower() == folder_name:

            for item in df['pinned_peers'] + df['include_peers']:
                if item['_'] == 'InputPeerChannel':
                    ids.add(item['channel_id'])

    return ids


async def run():
    test_user = 'kekuev'

    forward = False
    since_time = dt(2023, 5, 22)

    async with TelegramClient('anon', **read_creds()) as client:
        # client.loop.run_until_complete(client.send_message('kekuev', 'Hello'))

        async with client:
            # msgs = await client.get_messages('cryptoboy1017', 10)

            my_chat = await client.get_me()

            # print(msgs)

            for id_ in await get_crypt_content(client):
                entity = await client.get_entity(id_)

                if entity.broadcast:

                    if entity.title in {'CryptoEarn Important', 'BlockSide', 'Gagarin Crypto'}:

                        msgs = await client.get_messages(entity.id, offset_date=since_time, reverse=True, limit=3)

                        for msg in msgs:
                            if forward:
                                await client.forward_messages(my_chat, msg)
                            print(entity.title, msg.date)
                            # print(msgs[0].text)
                            print(msg.message)
                            print('\n\n<=============================>\n\n')

            # Do you have a conversation open with them? Get dialogs.
            # dgs = await client.get_dialogs()
            # for dg in dgs:
            #
            # if not dg.is_group and dg.is_channel:

            # print(dg.title)
            # print()
            # if dg.entity.broadcast:
            #     print(dg)




if __name__ == '__main__':
    asyncio.run(run())
