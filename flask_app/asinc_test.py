import asyncio


async def get_message():
    await asyncio.sleep(2)  # имитация ожидания сообщения от клиента
    print('Привет сервер!')


async def listen_port():
    while True:
        await asyncio.sleep(
            5
        )  # имитация ожидания запроса на соединение от клиента
        print('Получен запрос на соединение, ждем сообщения')
        asyncio.create_task(get_message())


async def main():
    await asyncio.create_task(listen_port())


asyncio.run(main())
