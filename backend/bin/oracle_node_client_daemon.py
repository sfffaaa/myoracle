#!/usr/bin/env python3

import sys
sys.path.append('src')
import argparse
from clients.oracle_node_client import OracleNodeClient
from utils.my_deployer import MyDeployer


def parse_arguement():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_path',
                        help='enter config path',
                        type=str,
                        required=True)

    parser.add_argument('-d', '--deploy',
                        help='deploy for brand new contracts',
                        action='store_true',
                        default=False)

    parser.add_argument('-w', '--wait_time',
                        help='enter wait time for daemon',
                        type=int,
                        default=2)

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_arguement()
    config_path = args.config_path
    wait_time = args.wait_time
    deploy = args.deploy

    if deploy:
        try:
            MyDeployer(config_path).undeploy()
        except IOError:
            pass
        else:
            raise
        MyDeployer(config_path).deploy()

    print('Start oracle node client')
    oracle_node_client = OracleNodeClient(config_path=config_path,
                                          wait_time=wait_time,
                                          deployed=False)
    oracle_node_client.start()
    oracle_node_client.join()
