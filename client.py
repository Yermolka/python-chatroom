import socket
import asyncio
from aioconsole import ainput, aprint

async def run_client(s: socket.socket, uname: str, pwd: str, incoming_port: int):
    loop = asyncio.get_event_loop()

    # Handshake with server
    await loop.sock_sendall(s, f'{uname} {pwd} {incoming_port}'.encode())
    resp = (await loop.sock_recv(s, 255)).decode('utf8').split('\n')
    if resp[0] != 'OK':
        raise Exception(resp[0])

    await aprint('connected')
    for r in resp[1:]:
        await aprint(r)

    cmd = ''
    while cmd != 'quit':
        cmd = await ainput('>')
        await loop.sock_sendall(s, cmd.encode())
    s.close()

async def handle_incoming(s: socket.socket, uname: str, pwd: str):
    loop = asyncio.get_event_loop()

    await loop.sock_sendall(s, f'{uname} {pwd}'.encode())
    resp = (await loop.sock_recv(s, 255)).decode('utf8').split('\n')
    if resp[0] != 'OK':
        raise Exception(resp[0])

    try:
        while True:
            msg = (await loop.sock_recv(s, 255)).decode('utf8')
            if msg == '':
                await asyncio.sleep(0.5)
                continue
            elif msg == uname + '_quit_command':
                break
            await aprint(msg)
    except Exception:
        return
    s.close()

async def main(username: str, password: str):
    output = socket.create_connection(('localhost', 8000))
    incoming = socket.create_connection(('localhost', 8000))
    output.setblocking(False)
    incoming.setblocking(False)

    # print(output.getsockname(), incoming.getsockname())
    tasks = [run_client(output, username, password, incoming.getsockname()[1]), handle_incoming(incoming, username, password)]
    await asyncio.gather(*tasks)

def run(username: str, password: str):
    asyncio.run(main(username, password))