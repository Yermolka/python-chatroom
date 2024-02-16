from typing import List
import socket
import asyncio

sample_db = [
    {
        'username': 'admin',
        'password': 'admin'
    },
    {
        'username': 'somecoolguy',
        'password': '123456'
    }
]

class User:
    def __init__(self, username: str, socket: socket.socket, recv_port: int) -> None:
        self.username = username
        self.client = socket
        self.recv_port = recv_port
        self.recv = None

    # for User in List
    def __eq__(self, __value: object) -> bool:
        if __value is not User:
            return False
        
        return self.username == __value.username
    
connected_users: List[User] = []

async def login_user(username: str, password: str) -> bool:
    for u in sample_db:
        if u['username'] != username:
            continue
        if u['password'] == password:
            return True
        else:
            break

    return False

async def handle_connect(client: socket.socket) -> User | None:
    loop = asyncio.get_event_loop()

    request = (await loop.sock_recv(client, 255)).decode('utf8').split(' ')

    # Check if it's output client socket
    # %username% %password% %port_incoming%
    if len(request) == 3:
        username = request[0]
        password = request[1]
        port_incoming = int(request[2])

        user = User(username, client, port_incoming)
        if user not in connected_users:
            if not await login_user(username, password):
                await loop.sock_sendall(client, 'Wrong credentials\n'.encode())
                return None
            connected_users.append(user)
            print(username, 'connected!')
            await loop.sock_sendall(client, 'OK\n'.encode())
        return user
    
    # Check if it's incoming client socket
    # %username% %password%
    elif len(request) == 2:
        username = request[0]
        password = request[1]

        # TODO: Auth
        while True:
            for u in connected_users:
                if u.username == username:
                    if not await login_user(username, password):
                        await loop.sock_sendall(client, 'Wrong credentials\n'.encode())
                        return None
                    u.recv = client
                    print(username, 'incoming connected!')
                    await loop.sock_sendall(client, 'OK\n'.encode())
                    return u
            await asyncio.sleep(0.5)

async def handle_client(client: socket.socket):
    """
    Async function to handle incoming messages from clients AND send them to all other clients
    """

    user = await handle_connect(client)
    if user is None:
        client.close()
        return
    loop = asyncio.get_event_loop()
    request = None

    await loop.sock_sendall(user.client, f'Hello, {user.username}'.encode())
    print('Sent hello')
    while request != 'quit':
        try:
            # Get a message from user
            request = (await loop.sock_recv(client, 255)).decode('utf8')
            response = f'{user.username}: {request}'
            
            # Send this message to all connected
            for u in connected_users:
                if u.username == user.username:
                    continue
                await loop.sock_sendall(u.recv, response.encode())
                print(response, 'to', u.username)
        except Exception:
            break
    
    if user.recv:
        await loop.sock_sendall(u.recv, f'{user.username}_quit_command'.encode())
        user.recv.close()
    try:
        connected_users.remove(user)
    except ValueError:
        pass
    client.close()     
    print(f'Closed socket for {user.username}')   

async def run_server():
    """
    
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        # Wait for client to connect
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))

def run():
    asyncio.run(run_server())