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

    def sysPrint(self, msg):
        self.chatPrint(sysCTA + msg)

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

    def outbound_node_connected(self, node):
        self.startKE()
        self.sysPrint('outbound_node_connected')

    def startKE(self, KE=None):
        x, y = self.ke.startExchange()
        if KE:
            self.send_to_nodes({ 
              "type": "end_KE", 
              "KE": { "x": x, "y": y }
            })
            self.endKE(KE)
        else:
            self.send_to_nodes({ 
              "type": "start_KE", 
              "KE": { "x": x, "y": y }
            })

    def endKE(self, KE):
        shared = self.ke.endExchange(KE["x"], KE["y"])
        self.sysPrint("Session Key: " + str(shared))

    # Message handling

    def node_message(self, node, data):
        if data.get("type") == "message":
            self.chatPrint(self.connectedCTA + data.get("content"))
        elif data.get("type") == "start_KE":
            self.startKE(data.get("KE"))
        elif data.get("type") == "end_KE":
            self.endKE(data.get("KE"))
        else:
            self.sysPrint('UNKNOWN MESSAGE TYPE')

    def send_message(self, msg):
        self.chatPrint(self.selfCTA + str(msg))
        return self.send_to_nodes({ 
          "type": "message", 
          "content": msg 
        })

    ## System Logs

    def inbound_node_connected(self, node):
        pass # self.sysPrint('inbound_node_connected')

    def inbound_node_disconnected(self, node):
        pass # self.sysPrint('inbound_node_disconnected')

    def outbound_node_disconnected(self, node):
        pass # self.sysPrint('outbound_node_disconnected')

    def node_disconnect_with_outbound_node(self, node):
        pass # self.sysPrint('node_disconnect_with_outbound_node')

    def node_request_to_stop(self):
        pass # self.sysPrint('node_request_to_stop')