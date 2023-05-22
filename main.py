import asyncio
import yaml
from telethon import TelegramClient, events
from telethon import functions, types


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

    async with TelegramClient('anon', **read_creds()) as client:
        # client.loop.run_until_complete(client.send_message('kekuev', 'Hello'))

        async with client:
            # msgs = await client.get_messages('cryptoboy1017', 10)

            # print(msgs)

            for id_ in await get_crypt_content(client):
                entity = await client.get_entity(id_)

                if entity.broadcast:

                    if entity.title in {'CryptoEarn Important', 'BlockSide'}:

                        msgs = await client.get_messages(entity.id, 3)

                        for msg in msgs:
                            print(entity.title)
                            # print(msgs[0].text)
                            print(msg.message)
                            print()




            # Do you have a conversation open with them? Get dialogs.
            # dgs = await client.get_dialogs()
            # for dg in dgs:
            #
            # if not dg.is_group and dg.is_channel:

            # print(dg.title)
            # print()
            # if dg.entity.broadcast:
            #     print(dg)


# TODO: get list of channels
# TODO: get data from this channels for the last day

if __name__ == '__main__':
    asyncio.run(run())
