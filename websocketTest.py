import asyncio
import websockets

websocketServer = "ws://192.168.188.70:1880/ws/test"  # Die Adresse der Truhe. localhost kann im Netzwerk durch die IP-Adresse ausgetauscht werden

async def sendKeyToBox(uidString):
    async with websockets.connect(websocketServer) as websocket:
        await websocket.send(uidString)
        response = await websocket.recv()
        print(response)

#asyncio.run(sendKeyToBox('test nico'))
loop = asyncio.get_event_loop()
loop.run_until_complete(sendKeyToBox("Nico"))