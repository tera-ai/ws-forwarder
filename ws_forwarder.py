# ws_forwarder.py
#   pip install websockets
import asyncio, sys, json, websockets, signal

PORT = 8765

async def producer():
    """Yield each complete line that the wrapped program prints."""
    loop = asyncio.get_running_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    while True:
        line = await reader.readline()
        if not line:                 # EOF  →  exit
            break
        yield line.decode().strip()

async def handler(websocket, _):
    async for msg in producer():
        # expect each line to be JSON already, otherwise wrap it here
        await websocket.send(msg)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"WS server on ws://localhost:{PORT}")
        await asyncio.Future()       # run forever

signal.signal(signal.SIGINT, lambda *_: asyncio.get_event_loop().stop())
asyncio.run(main())