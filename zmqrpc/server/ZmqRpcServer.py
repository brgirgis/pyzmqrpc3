

'''
Created on Apr 8, 2014
Edited on Oct 22, 2020

@author: Jan Verhoeven
@author: Bassem Girgis

@copyright: MIT license, see http://opensource.org/licenses/MIT
'''


import json

from ..heartbeat import zmq_sub_heartbeat
from ..logger import logger
from ..receiver import ZmqReceiver


class ZmqRpcServer(ZmqReceiver):
    '''
    The ZmqRpcServer implements a ZmqReceiver and extends it with the ability
    to host one or more methods that can be invoked by a ZmqRpcClient.
    In case a PUB/SUB connection is used, no response is provided.
    In case a REQ/REQ connection is used a response must be provided in
    order for the system to know the call was successful.
    The ZmqRpcServer constructor takes a collection of either REP or SUB
    addresses for the ZMQ layer.
    The rpc_functions are dict structures mapping a string value to a
    real method implementation.
    A username/password may be used for REQ/REP pairs (does not seem to be
    working for PUB/SUB sockets
    '''

    def __init__(
            self,
            zmq_rep_bind_address=None,
            zmq_sub_connect_addresses=None,
            rpc_functions=None,
            recreate_timeout=600,
            username=None,
            password=None):
        super().__init__(
            zmq_rep_bind_address,
            zmq_sub_connect_addresses,
            recreate_timeout,
            username,
            password,
        )
        self.rpc_functions = rpc_functions

    def handle_incoming_message(self, message):
        if message == zmq_sub_heartbeat:
            return None

        status_code = 200
        status_message = "OK"
        response_message = None
        try:
            incoming_message = json.loads(message)
        except Exception as e:
            status_code = 400
            status_message = "Incorrectly marshalled function. Incoming message is no proper json formatted string. Exception: {0}".format(
                e)
            logger.warninging(status_message)
        else:
            if "function" not in incoming_message:
                status_code = 450
                status_message = "Incorrectly marshalled function. No function name provided."
                logger.warninging(status_message)
            else:
                function_name = incoming_message["function"]
                parameters = None
                if "parameters" in incoming_message:
                    parameters = incoming_message["parameters"]
                if function_name not in self.rpc_functions:
                    status_code = 451
                    status_message = "Function '{0}' is not implemented on server. Check rpc_functions on server if it contains the function name".format(
                        function_name)
                    logger.warninging(status_message)
                else:
                    try:
                        if parameters is None:
                            response_message = self.rpc_functions[function_name](
                            )
                        else:
                            response_message = self.rpc_functions[function_name](
                                **parameters)
                    except Exception as e:
                        status_code = 463
                        status_message = "Exception raised when calling function {0}. Exception: {1} ".format(
                            function_name, e)
                        logger.warninging(status_message)
                        logger.exception(e)

        return self.create_response_message(
            status_code, status_message, response_message)
