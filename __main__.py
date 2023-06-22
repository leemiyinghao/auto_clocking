import argparse
import os
import csv
import sys

from dotenv import load_dotenv

from utils import dump_activities, log_activity, is_slack_exist
from models import Clock


def dump(args: argparse.Namespace) -> None:
    csv_writer = csv.writer(sys.stdout)
    for activity in dump_activities(args.d):
        csv_writer.writerow([activity[0], activity[1], activity[2]])


def log(args: argparse.Namespace):
    if is_slack_exist():
        log_activity()


if __name__ == "__main__":
    # read envs
    load_dotenv()

    # setup database
    Clock.setup_database(os.getenv("DB_PATH", "clocks.db"))

    # parse args
    arg_parser = argparse.ArgumentParser()
    sub_parsers = arg_parser.add_subparsers()

    log_parser = sub_parsers.add_parser("log", help="Log if Slack is operating.")
    log_parser.set_defaults(func=log)

    dump_parser = sub_parsers.add_parser("dump", help="Dump logs.")
    dump_parser.add_argument(
        "-d",
        help="Days before for dumping logs, default: now - 31 days",
        type=int,
        default=31,
    )
    dump_parser.set_defaults(func=dump)

    args = arg_parser.parse_args()
    args.func(args)
