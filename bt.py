# Bits and pieces copied from
# https://github.com/pybluez/pybluez/blob/master/examples/simple/
import random
import string
import time

from bluetooth import *

uuid = "94f39d29-7d6d-437d-973b-fba3de49d4ee"
end_token = "#!#!#!"

class BTClient(object):

    def __init__(self, addr):
        self.addr = addr

        # search for the SampleServer service
        addresses = discover_devices(lookup_names=False)
        print(addresses)
        service_matches = find_service(uuid=uuid, address=addr)
        print(service_matches)

        if len(service_matches) == 0:
            print("couldn't find the SampleServer service =(")
            sys.exit(0)

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        print("connecting to \"%s\" on %s, port %s" % (name, host, port))

        # Create the client socket
        self.sock = BluetoothSocket(RFCOMM)
        # self.sock.settimeout(5)
        self.sock.connect((host, port))

        print("Connection Up")

    def __del__(self):
        self.sock.close()

    def send(self, kbytes):

        chunk = 2 # %kb chuncks
        num_chunks = kbytes//chunk
        t = ''.join(random.choices(string.ascii_uppercase +
                                   string.digits, k=1024 * chunk))
        tt = t.encode()

        start = time.time()
        for i in range(num_chunks):
            self.sock.send(tt)

        self.sock.send(end_token.encode())
        d = ""
        while end_token not in d:
            d += self.sock.recv(96).decode()
        end = time.time()
        print(end - start)
        return d

class BTServer(object):

    def __init__(self):
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)

        self.port = self.server_sock.getsockname()[1]

        self.uuid = uuid


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
                    start = time.time()
                    d = ""
                    while end_token not in d:
                        d += client_sock.recv(2056).decode()

                    total += len(d)
                    end = time.time()
                    print("Time", end - start)
                    t = ''.join(random.choices(string.ascii_uppercase +
                                               string.digits, k=50)) + end_token
                    client_sock.send(t.encode())

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
