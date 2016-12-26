from murfie.murfie import Murfie
from time import sleep
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
        print("Logging in to murfie")
        m.login()

        print("Building list of stale downloads")
        while True:
            download_ids = m.get_download_ids()
            downloads_total = len(download_ids)
            if downloads_total == 0: break
            download_current = 1
            print("Purging %s stale downloads" % len(download_ids))
            while len(download_ids) > 0:
                download_id = download_ids[0]
                print("Purging stale download id: %s [%s/%s]" % (
                    download_id,
                    download_current,
                    downloads_total
                ))
                try:
                    m.remove_download(download_id)
                except:
                    print("Download purge failed: Retrying in 5 seconds")
                    sleep(5)
                    pass
                download_ids.pop(0)
                download_current += 1

        print("Building list of discs to request downloads for")
        disc_ids = m.get_library_disc_ids()
        discs_total = len(disc_ids)
        disc_current = 1
        while len(disc_ids) > 0:
            disc_id = disc_ids[0]
            print("Requesting download for disc id: %s [%s/%s]" % (
                disc_id,
                disc_current,
                discs_total
            ))
            try:
                m.request_disc_download(disc_id)
            except:
                print("Download request failed: Retrying in 5 seconds")
                sleep(5)
                pass
            disc_ids.pop(0)
            disc_current += 1
            # Sleep required to avoid bug where murfie's third
            # party download service often generates empty zips
            # when > 1 download/min
            print("Sleeping 30 seconds to avoid overwhelming Murfie D/L api.")
            sleep(30)

        print("Building list of downloads")
        while True:
            download_ids = m.get_download_ids()
            downloads_total = len(download_ids)
            if downloads_total == 0: break
            download_current = 1
            while len(download_ids) > 0:
                download_id = download_ids[0]
                print("Starting download id: %s [%s/%s]" % (
                    download_id,
                    download_current,
                    downloads_total
                ))
                try:
                    print("\nStarting download id: %s\n" % download_id)
                    for complete, total in m.start_download(download_id):
                        status = r"%s.zip %s [%3.2f%%]" % (
                            download_id,
                            file_size(complete),
                            complete * 100. / total
                        )
                        status = status + chr(8)*(len(status)+1)
                        print("\r", status, end="")
                except:
                    print("Download failed: Retrying in 5 seconds")
                    sleep(5)
                    pass
                download_ids.pop(0)
                download_current += 1


def main():
    parser = create_parser()
    args = parser.parse_args()
    process_args(args)
