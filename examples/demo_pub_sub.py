

'''
Created on Apr 2014
Edited on Oct 2020

@author: Jan Verhoeven
@author: Bassem Girgis

@copyright: MIT license, see http://opensource.org/licenses/MIT
'''


import sys
import time
from typing import Optional, Tuple

from zmqrpc import ICommand, IService, ZmqRpcClient, ZmqRpcServerThread


class SimpleCommand(ICommand):

    def __init__(
            self,
            param1: Optional[str] = None,
            param2: Optional[str] = None):
        super().__init__()

        self.__param1 = param1 or ''
        self.__param2 = param2 or ''

    @property
    def param1(self) -> str:
        return self.__param1

    @property
    def param2(self) -> str:
        return self.__param2

    def set_command_state(self, state: dict) -> None:
        self.__param1 = state['param1']
        self.__param2 = state['param2']

    def get_command_state(self) -> dict:
        return dict(
            param1=self.param1,
            param2=self.param2,
        )


class SimpleService(IService):

    def __call__(self, command: SimpleCommand) -> Optional[object]:
        print(
            'SimpleCommand executed with params "{0}" and "{1}"'.format(
                command.param1,
                command.param2,
            )
        )
        return 'SimpleService response text for SimpleCommand is "%s"' % str(
            dict(
                param1=command.param1,
                param2=command.param2,
            )
        )


def main(args: Optional[Tuple[str]] = None) -> int:

    print('starting client ...')
    client = ZmqRpcClient(
        zmq_pub_endpoint='tcp://*:30000',
    )

    print('starting server ...')
    server = ZmqRpcServerThread(
        zmq_sub_connect_addresses=['tcp://localhost:30000'],    # Must be a list
    )
    server.register_service(
        command_class=SimpleCommand,
        service=SimpleService(),
    )
    server.start()

    # Wait a bit since sockets may not have been connected immediately
    time.sleep(2)

    response = client.execute_remote(
        command=SimpleCommand(param1='value1', param2='value2'),
    )

    print('response: {0}'.format(response))

    # Wait a bit to make sure message has been received
    time.sleep(2)

    # Clean up
    server.stop()
    server.join()

    client.destroy()

    return 0


if __name__ == '__main__':
    sys.exit(main())
