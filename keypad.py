#!/bin/python3

import os
import time
import asyncio
import websockets
import json
import typing

from websockets.asyncio.client import connect, ClientConnection
from dotenv import load_dotenv

load_dotenv()

haHost = os.environ['HA_HOST']
haPort = os.environ['HA_PORT']
haToken = os.environ['HA_TOKEN']

haUrl = 'ws://' + haHost + ':' + haPort + '/api/websocket'

async def authenticate(ws: ClientConnection):
    await ws.send(json.dumps({'type':'auth','access_token':haToken}))

async def events_subscribe(ws: ClientConnection):
    await ws.send(json.dumps({
        'id': 18,
        'type': 'subscribe_events',
        'event_type': 'state_changed'
    }))

    while True:
        print(await ws.recv())

async def main():
    async with connect(haUrl) as ws:
        await authenticate(ws)
        await events_subscribe(ws)
        await asyncio.get_running_loop().create_future() # run forever

asyncio.run(main())