import zmq
import time
ctx = zmq.Context()

frontend= ctx.socket(zmq.ROUTER)
backend = ctx.socket(zmq.DEALER)

frontend.bind("ipc://frontend.ipc")
backend.bind("ipc://backend.ipc")

poller = zmq.Poller()

poller.register(frontend,zmq.POLLIN)
poller.register(backend,zmq.POLLIN)
worker_client_connection = {

}
queue = []

available_workers = []

while True:
    poller_dict  = dict(poller.poll())
    if backend in poller_dict:
        msg = backend.recv_multipart()
        if msg[2] == b'!ready_to_work!':
            available_workers.append(msg[0])
            print(f"worker {msg[0]} is connected and ready to work")
        elif msg[2]== b'!dead_worker!': 
            available_workers.remove(msg[0])
        else:
            client_id = worker_client_connection.pop(msg[0])
            frontend.send_multipart([client_id,b'',msg[2]])
    if frontend in poller_dict:
        msg = frontend.recv_multipart()
        queue.append(msg)

    if len(queue)==0:
        time.sleep(0.1)
    else:
        if len(available_workers)!=0:
            ready_worker = available_workers[0]
            following_client = queue[0]
            available_workers.remove(ready_worker)
            queue.remove(following_client)
            worker_client_connection[ready_worker]=following_client[0]
            backend.send_multipart([ready_worker,b'',following_client[2]])
        

    



