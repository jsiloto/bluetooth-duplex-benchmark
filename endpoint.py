import argparse
from bt import BTClient, BTServer


def get_argparser():
    argparser = argparse.ArgumentParser(description='Bluetooth endpoint')
    argparser.add_argument("-server", action="store_true", help="Act as a Server, Wait for data")
    argparser.add_argument("-client", action="store_true", help="Act as a Client, Send data")
    argparser.add_argument("--addr", type=str, help="If client, please specify target connection")
    argparser.add_argument('--kbytes', type=int, default=1, help='Send N bytes to server and recieve them back')
    return argparser


if __name__ == "__main__":
    args = get_argparser().parse_args()
    if args.server:
        server = BTServer()
        server.run()
        pass
    elif args.client:
        if not args.addr:
            raise(ValueError("No target server specified"))
        client = BTClient(args.addr)
        d = client.send(args.kbytes)


