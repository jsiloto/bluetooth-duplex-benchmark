# Bits and pieces copied from
# https://github.com/pybluez/pybluez/blob/master/examples/simple/
from bluetooth import *
import lorem

class BTClient(object):

    def __init__(self, addr):
        self.addr = addr
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((addr, 1))

    def __del__(self):
        self.sock.close()

    def query(self):
        d = b""
        t = lorem.text()
        print(t)

        while len(d) != 130:
            # Send request to USB meter
            self.sock.send((0xF0).to_bytes(1, byteorder="big"))
            d += self.sock.recv(130)
        data = self.processdata(d)
        return data



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
                while True:
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    print("Received", data)
            except OSError:
                pass

            print("Disconnected.")

            client_sock.close()
        self.server_sock.close()
        print("All done.")

    def __del__(self):
        self.server_sock.close()
