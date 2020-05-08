import asyncio
import json
import websockets
from room import Room
from amazons import Amazons

get_mesg = lambda x: bytes(str(json.dumps(x)), 'utf-8')

class Server():
    def __init__(self):
        self.__ip = '0.0.0.0'
        self.__port = 5434
        self.__server = websockets.serve(self.handler, self.__ip, self.__port)

        self.rooms = []
        self.clients = []
    
    def start(self):
        print('Starting server')
        asyncio.get_event_loop().run_until_complete(self.__server)
        asyncio.get_event_loop().run_forever()

    async def handler(self, socket, path):
        self.clients.append(socket)
        print('Client connected')
        await socket.send(get_mesg({'mesg': 'room_list', 'room_list': [{'id': i.roomId, 'type': i.type} for i in self.rooms]}))

        data = await socket.recv()
        data = json.loads(data)
        print(data)

        if data['mesg'] == 'add_room':
            room = Room(data['type'], data['args'], data['time'], len(self.rooms) + 1)
            self.rooms.append(room)
            order = data['order']
            for i, c in enumerate(self.clients):
                if c != socket:
                    try:
                        await c.send(get_mesg({'mesg': 'room_list', 'room_list': [{'id': i.roomId, 'type': i.type} for i in self.rooms]}))
                    except websockets.exceptions.ConnectionClosedOK:
                        self.clients.remove(c)

        elif data['mesg'] == 'join':
            room = self.rooms[int(data['room_id']) - 1]
            order = room.getOrder()
        playerId = room.addPlayer(socket, order)
        await socket.send(get_mesg({'mesg': data['mesg'], 'playerId': playerId, 'type': room.type, 'order': order}))

        while True:
            data = await socket.recv()
            data = json.loads(data)
            print(data)

            if (data['mesg'] == 'start'):
                await room.start(playerId)
            elif (data['mesg'] == 'move'):
                location = data['location']
                if data.get('kw') != None:
                    await room.move(playerId, location, data['kw'])
                else:
                    await room.move(playerId, location)
            elif (data['mesg'] == 'rollback'):
                await room.rollback()

if __name__ == '__main__':
    server = Server()
    server.start()
