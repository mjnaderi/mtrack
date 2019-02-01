#!/usr/bin/env python3
import argparse
import logging
from mtrack.version import __version__
from mtrack.timer import MTrackTimer


def main():
    parser = argparse.ArgumentParser(description='mtrack')
    parser.add_argument('--version', action='version', version=f'MTrack %s' % __version__)
    parser.add_argument('project', help='project name')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('sh.command').setLevel(logging.WARNING)

    timer = MTrackTimer(args.project)
    timer.run()


if __name__ == "__main__":
    main()
