import asyncio

class Timer:
    def __init__(self, timeout, callback, beforeCallback):
        self._timeout = timeout
        self._callback = callback
        self._beforeCallback = beforeCallback

    async def _job(self):
        await self._beforeCallback()
        while True:
            await self._callback()
            await asyncio.sleep(self._timeout)


    def start(self):
        self._task = asyncio.ensure_future(self._job())

    async def asyncStart(self):
        await self._job()

    def cancel(self):
        self._task.cancel()