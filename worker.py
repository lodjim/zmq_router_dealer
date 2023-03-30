import zmq
import threading
import time
import random
import uuid

def worker():
    ctx = zmq.Context()
    client_socket = ctx.socket(zmq.DEALER)
    client_socket.connect('ipc://backend.ipc')
    client_socket.identity = str(uuid.uuid4()).encode()
    client_socket.send_multipart([client_socket.identity,b'',b'!ready_to_work!'])
    keep_loop  = True
    while keep_loop:
        try:
            client_socket.recv_multipart()
            print(f'{client_socket.identity} is working')
            time.sleep(2)
            client_socket.send_multipart([client_socket.identity,b'',b'how are you doing'])
            client_socket.send_multipart([client_socket.identity,b'',b'!ready_to_work!'])
        except KeyboardInterrupt:
            client_socket.send_multipart([client_socket.identity,b'',b'!dead_worker!'])
            break
if __name__ =="__main__":

    for _ in range(5):
        th = threading.Thread(target=worker)
        th.start()
        
