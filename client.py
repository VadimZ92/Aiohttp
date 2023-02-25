import asyncio
from aiohttp import ClientSession

async def main():

    async with ClientSession() as session:
        response = await session.post('http://127.0.0.1:5000/advertising/',
                                 json={'header': 'adv23333', 'description': 'ertrt', 'user': 'user1'})
        print(response.status)
        print(await response.json())

        response = await session.get('http://127.0.0.1:5000/advertising/1/')
        print(response.status)
        print(await response.json())

        # response = await session.patch('http://127.0.0.1:5000/advertising/1/',
        #                   json={'header': 'adv23333', 'description': 'abcabc'})
        #
        # print(response.status)
        # print(await response.json())
        #
        # response = await session.get('http://127.0.0.1:5000/advertising/1/')
        # print(response.status)
        # print(await response.json())

        # response = await session.delete('http://127.0.0.1:5000/advertising/2/')
        #
        # print(response.status)
        # print(await response.json())
        #
        #
        # response = await session.get('http://127.0.0.1:5000/advertising/1/')
        # print(response.status)
        # print(await response.json())

asyncio.run(main())



