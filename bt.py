# Bits and pieces copied from
# https://github.com/pybluez/pybluez/blob/master/examples/simple/
import random
import string
import time

from bluetooth import *
import lorem

class BTClient(object):

    def __init__(self, addr):
        self.addr = addr
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((addr, 1))

    def __del__(self):
        self.sock.close()

    def send(self, kbytes):

        message_size=27
        chunk = 3 # %kb chuncks
        num_chunks = kbytes//chunk
        t = ''.join(random.choices(string.ascii_uppercase +
                                   string.digits, k=1024 * chunk))
        tt = t.encode()

        start = time.time()
        for j in range(kbytes//message_size):
            print("Message", j)
            for i in range(message_size//chunk):
                self.sock.send(tt)

            d = b""
            while len(d) <= 1000:
                # Send request to USB meter
                d += self.sock.recv(256)
            print(d)
        end = time.time()
        print(end - start)
        return

class BTServer(object):

    def __init__(self, uuid):
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)

        self.port = self.server_sock.getsockname()[1]

        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    def run(self):

        advertise_service(self.server_sock, "SampleServer", service_id=self.uuid,
                                        service_classes=[self.uuid, SERIAL_PORT_CLASS],
                                        profiles=[SERIAL_PORT_PROFILE],
                                        # protocols=[bluetooth.OBEX_UUID]
                                        )

        print("Waiting for connection on RFCOMM channel", self.port)
        while (True):
            client_sock, client_info = self.server_sock.accept()
            print("Accepted connection from", client_info)

            try:
                total = 0
                while True:
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    total += len(data)
                    print("Received", total)
                    if total >= 27e3:
                        t = ''.join(random.choices(string.ascii_uppercase +
                                                   string.digits, k=1024))
                        client_sock.send(t.encode())
                        total = 0
            except OSError:
                pass
            except KeyboardInterrupt:
                exit()

            print("Disconnected.")
            client_sock.close()

        self.server_sock.close()
        print("All done.")

    def __del__(self):
        self.server_sock.close()
