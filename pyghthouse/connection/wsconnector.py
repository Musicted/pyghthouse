from threading import Thread, Lock
from websocket import WebSocketApp, setdefaulttimeout, ABNF
from msgpack import packb, unpackb


class WSConnector:

    class REID:
        def __init__(self):
            self._next = 0

        def __next__(self):
            n = self._next
            self._next += 1
            return n

        def __iter__(self):
            return self

    def __init__(self, username: str, token: str, address: str, on_msg=None):
        self.username = username
        self.token = token
        self.address = address
        self.on_msg = on_msg
        self.ws = None
        self.lock = Lock()
        self.reid = self.REID()
        self.running = False
        setdefaulttimeout(60)

    def send(self, data):
        with self.lock:
            self.ws.send(packb(self.construct_package(data), use_bin_type=True), opcode=ABNF.OPCODE_BINARY)

    def start(self):
        self.stop()
        self.ws = WebSocketApp(self.address,
                               on_message=None if self.on_msg is None else self._handle_msg,
                               on_open=self._ready, on_error=self._fail)
        self.lock.acquire()
        Thread(target=self.ws.run_forever).start()

    def _fail(self, ws, err):
        self.lock.release()
        raise err

    def stop(self):
        if self.ws is not None:
            with self.lock:
                print("Closing the connection.")
                self.running = False
                self.ws.close()
                self.ws = None

    def _ready(self, ws):
        print(f"Connected to {self.address}.")
        self.running = True
        self.lock.release()

    def _handle_msg(self, ws, msg):
        if isinstance(msg, bytes):
            msg = unpackb(msg)
        self.on_msg(msg)

    def construct_package(self, payload_data):
        return {
            'REID': next(self.reid),
            'AUTH': {'USER': self.username, 'TOKEN': self.token},
            'VERB': 'PUT',
            'PATH': ['user', self.username, 'model'],
            'META': {},
            'PAYL': payload_data
        }