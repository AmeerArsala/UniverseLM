import asyncio
import anyio
import time

async def my_task():
    print("Task started")
    await asyncio.sleep(5)
    print("Task completed")

async def main():
    task = asyncio.create_task(my_task())
    print("Task created")

asyncio.run(main())

for i in range(10000000):
    print('0', end='')