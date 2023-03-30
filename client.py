import zmq
import threading


def worker():
    ctx = zmq.Context()
    client_socket = ctx.socket(zmq.DEALER)
    client_socket.connect('ipc://frontend.ipc')
    client_socket.send_multipart([b'',b'hello world'])
    msg = client_socket.recv_multipart()
    print(msg)

if __name__ =="__main__":
    for _ in range(10):
        th = threading.Thread(target=worker)
        th.start()




