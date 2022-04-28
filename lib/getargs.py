#!/usr/bin/env python
import argparse

def getargs():
    parser = get_arg_parser()
    args = parser.parse_args()
    if args.refresh_token is None and args.password is None:
        raise parser.error("Either username + password or refresh_token must be provided")
    return args


def get_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-n', '--nsx_host', type=str, required=True,
                            help='NSX host to connect to')
    arg_parser.add_argument('-t', '--tcp_port', type=int, default=443,
                            help='TCP port for NSX server')
    arg_parser.add_argument('-u', '--user', type=str, default="admin", required=False,
                            help='User to authenticate as (using basic authenticatio)')
    arg_parser.add_argument('-p', '--password', type=str, required=False,
                            help='Password (using basic authentication)')
    arg_parser.add_argument('-r', '--refresh_token', type=str, required=False,
                            help='Refresh token (using VMC authentication)')

    return arg_parser