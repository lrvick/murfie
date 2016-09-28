from murfie.murfie import Murfie
import time
from argparse import ArgumentParser


def create_parser():

    parser = ArgumentParser(description="""
        Tool to interface with murfie. Provides methods to download library
        and hopefully more in the future.
    """)

    subparsers = parser.add_subparsers(help='sub-command help', dest='parser')

    login_parser = subparsers.add_parser(
        'login',
        help='Login to Murfie.com and store credentials'
    )
    login_parser.add_argument(
        "email",
        metavar="email",
        type=str,
        help="Murphie.com email"
    )
    login_parser.add_argument(
        "password",
        metavar="password",
        type=str,
        help="Murphie.com password"
    )

    subparsers.add_parser(
        'sync',
        help='Sync Murfie.com library to current directory'
    )

    return parser


def process_args(args):

    m = Murfie()

    if args.parser == 'login':
        m.login(args.email, args.password)
        pass

    if args.parser == 'sync':
        m.login()
        for disc_id in m.get_library_disc_ids():

            print("Requesting download for disc id: %s" % disc_id)
            m.request_disc_download(disc_id)

            # Sleep required to avoid bug where murfie's third
            # party download service often generates empty zips
            # when > 1 download/min
            print("Sleeping 60 seconds to avoid overwhelming murphie D/L api.")
            time.sleep(60)
        pass


def main():
    parser = create_parser()
    args = parser.parse_args()
    process_args(args)
