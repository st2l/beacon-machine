import argparse
import shutil
import sys

from beacon_machine.core import launch_aps
from beacon_machine.ssid import random_ssids, single_ssid, ssid_from_file

SUPPORTED_CHANNELS = {1, 6, 11, 36, 40, 44, 48}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Beacon Flood via airbase-ng subprocess span")
    parser.add_argument("interface", help="Interface name")
    parser.add_argument("-c", "--count", type=int, default=15, help="Networks amount")
    parser.add_argument("-ch", "--channel", type=int, default=36, help="Channel (1, 6, 11, 36, 40, 44, 48)")

    ssid_group = parser.add_mutually_exclusive_group(required=True)
    ssid_group.add_argument("--ssid", help="Use one SSID for all APs (no prefix mode)")
    ssid_group.add_argument("--ssid-file", help="Read SSIDs from file, one per line")
    ssid_group.add_argument("--random-ssid", action="store_true", help="Generate random SSIDs")

    parser.add_argument("--random-length", type=int, default=10, help="Random SSID length (4..32)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible SSID generation")
    return parser


def resolve_ssids(args: argparse.Namespace) -> list[str]:
    if args.ssid:
        return single_ssid(args.ssid, args.count)
    if args.ssid_file:
        return ssid_from_file(args.ssid_file, args.count)
    return random_ssids(args.count, args.random_length, args.seed)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.count <= 0:
        parser.error("count must be greater than 0")
    if args.channel not in SUPPORTED_CHANNELS:
        parser.error("unsupported channel")
    if not args.random_ssid and (args.seed is not None or args.random_length != 10):
        parser.error("--seed and --random-length can be used only with --random-ssid")
    if shutil.which("airbase-ng") is None:
        parser.error("airbase-ng is not installed or not in PATH")

    if args.count > 50:
        print("[!] ATTENTION [!] U are playing risky. A lot of beacons can shut your os! Proceed with caution")
        confirm = input("[?] Yea or nope (y/n): ")
        if confirm.lower() != "y":
            sys.exit()

    try:
        ssids = resolve_ssids(args)
    except ValueError as err:
        parser.error(str(err))

    launch_aps(args.interface, ssids, args.channel)


if __name__ == "__main__":
    main()
