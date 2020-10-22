
class ZmqProxyRep2PubThread(ZmqProxyThread):
    def __init__(
            self,
            zmq_rep_bind_address=None,
            zmq_pub_bind_address=None,
            recreate_sockets_on_timeout_of_sec=600,
            username_rep=None,
            password_rep=None,
            username_pub=None,
            password_pub=None):
        ZmqProxyThread.__init__(self)
        self.proxy = ZmqProxyRep2Pub(
            zmq_rep_bind_address=zmq_rep_bind_address,
            zmq_pub_bind_address=zmq_pub_bind_address,
            recreate_sockets_on_timeout_of_sec=recreate_sockets_on_timeout_of_sec,
            username_rep=username_rep,
            password_rep=password_rep,
            username_pub=username_pub,
            password_pub=password_pub)
