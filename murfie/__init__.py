from murfie.murfie import Murfie
import time
from argparse import ArgumentParser
from math import log2


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
        help="Murfie.com email"
    )
    login_parser.add_argument(
        "password",
        metavar="password",
        type=str,
        help="Murfie.com password"
    )

    subparsers.add_parser(
        'sync',
        help='Sync Murfie.com library to current directory'
    )

    return parser


def file_size(size):
    unit = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    order = int(log2(size) / 10) if size else 0
    return '{:.4g} {}'.format(size / (1 << (order * 10)), unit[order])


def process_args(args):

    m = Murfie()

    if args.parser == 'login':
        m.login(args.email, args.password)
        pass

    if args.parser == 'sync':
        m.login()

        for download_id in m.get_download_ids():
            print("Purging stale download: %s" % download_id)
            m.remove_download(download_id)

        for disc_id in m.get_library_disc_ids():
            print("Requesting download for disc id: %s" % disc_id)
            m.request_disc_download(disc_id)

            # Sleep required to avoid bug where murfie's third
            # party download service often generates empty zips
            # when > 1 download/min
            print("Sleeping 60 seconds to avoid overwhelming Murfie D/L api.")
            time.sleep(60)

        for download_id in m.get_download_ids():
            print("\nStarting download id: %s\n" % download_id)
            for complete, total in m.start_download(download_id):
                status = r"%s.zip %s [%3.2f%%]" % \
                    (download_id, file_size(complete), complete * 100. / total)
                status = status + chr(8)*(len(status)+1)
                print("\r", status, end="")


def main():
    parser = create_parser()
    args = parser.parse_args()
    process_args(args)
