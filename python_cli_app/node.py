import time, sys
from p2pnetwork.node import Node
from eke import EKE

sysCTA = "sys > "

class P2P (Node):
    def __init__(self, nodeInfo, destInfo, chatPrint):
        super(P2P, self).__init__(nodeInfo["host"], nodeInfo["port"], callback=None)
        self.debug = False
        self.chatPrint=chatPrint

        self.nodeInfo = nodeInfo
        self.destInfo = destInfo
        self.ke = EKE(nodeInfo["private"], destInfo["pub"])

        self.start()

    @property
    def selfCTA(self):
        return f"{self.nodeInfo.get('user')} >> "

    @property
    def connectedCTA(self):
        return f"{self.destInfo.get('user')} >> "

    # Init connection

    def connect(self):
        for i in range(10):
            time.sleep(0.5)
            if self.connect_with_node(self.destInfo["host"], self.destInfo["port"]):
                break
            else:
                continue
        else:
            sys.exit(f'Nao conseguiu conectar com usuario {self.destInfo["user"]}')
        time.sleep(1)
        # self.startCrypt()

    def startCrypt(self, answer=False):
        pass

    # Message handling

    def send_message(self, msg):
        self.chatPrint(self.selfCTA + str(msg))
        return self.send_to_nodes({ "type": "message", "content": msg })

    def node_message(self, node, data):
        if data.get("type") == "message":
            self.chatPrint(self.connectedCTA + data.get("content"))
        elif data.get("type") == "config":
            pass
        else:
            self.chatPrint(sysCTA + 'UNKNOWN MESSAGE TYPE')

    ## System prints

    def outbound_node_connected(self, node):
        self.chatPrint(sysCTA + 'outbound_node_connected')

    def inbound_node_connected(self, node):
        self.chatPrint(sysCTA + 'inbound_node_connected')

    def inbound_node_disconnected(self, node):
        self.chatPrint(sysCTA + 'inbound_node_disconnected')

    def outbound_node_disconnected(self, node):
        self.chatPrint(sysCTA + 'outbound_node_disconnected')

    def node_disconnect_with_outbound_node(self, node):
        self.chatPrint(sysCTA + 'node_disconnect_with_outbound_node')

    def node_request_to_stop(self):
        self.chatPrint(sysCTA + 'node_request_to_stop')