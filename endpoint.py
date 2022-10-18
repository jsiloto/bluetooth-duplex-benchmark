import argparse
from bt import BTClient, BTServer


def get_argparser():
    argparser = argparse.ArgumentParser(description='Bluetooth endpoint')
    argparser.add_argument("-server", action="store_true", help="Act as a Server, Wait for data")
    argparser.add_argument("-client", action="store_true", help="Act as a Client, Send data")
    argparser.add_argument("--target", type=str, help="If client, please specify target connection")
    argparser.add_argument('--bytes', type=int, default=256, help='Send N bytes to server and recieve them back')
    return argparser


if __name__ == "__main__":
    args = get_argparser().parse_args()
    if args.server:
        server = BTServer()
        server.run()
        pass
    elif args.client:
        if not args.target:
            raise(ValueError("No target server specified"))
        BTClient(args.target)

