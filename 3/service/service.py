import argparse
import os
import pathlib
import signal
import subprocess
import sys

PID_FILE = pathlib.Path('program.pid')
LOG_FILE = pathlib.Path('program.log')
ERR_FILE = pathlib.Path('program.error.log')


def start_service():
    if PID_FILE.exists():
        pid = PID_FILE.read_text()
        # check if it is running
        print('Service is already running')
        return

    process = subprocess.Popen(
        [
            sys.executable,
            'wrapper.py',
            str(PID_FILE.absolute()),
            str(LOG_FILE.absolute()),
            str(ERR_FILE.absolute()),
            sys.executable,
            str(pathlib.Path('program.py').absolute()),
        ],
        stdin=subprocess.DEVNULL,
    )


def stop_service():
    if not PID_FILE.exists():
        print('Service is not running')
        return
    pid = int(PID_FILE.read_text())
    try:
        os.kill(pid, signal.SIGTERM)
    finally:
        PID_FILE.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['start', 'stop', 'restart'])
    args = parser.parse_args()

    match args.command:
        case 'start':
            start_service()
        case 'stop':
            stop_service()
        case 'restart':
            stop_service()
            start_service()


if __name__ == '__main__':
    main()
