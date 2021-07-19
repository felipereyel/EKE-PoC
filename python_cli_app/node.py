from p2pnetwork.node import Node

sysCTA = "sys > "

class P2P (Node):

    def __init__(self, nodeInfo, chatPrint=None):
        super(P2P, self).__init__(nodeInfo["host"], nodeInfo["port"], callback=None)
        self.debug = False
        self.chatPrint=chatPrint
        self.nodeInfo = nodeInfo
        self.connectedNodeInfo = None

        self.start()

    def connect_with_node(self, nodeInfo):
        self.connectedNodeInfo = nodeInfo
        return super().connect_with_node(nodeInfo["host"], nodeInfo["port"])

    @property
    def selfCTA(self):
        return f"{self.nodeInfo.get('user')} >> "

    @property
    def connectedCTA(self):
        return f"{self.connectedNodeInfo.get('user')} >> "

    # Init connection

    def outbound_node_connected(self, node):
        self.chatPrint(sysCTA + 'outbound_node_connected')
        
    def inbound_node_connected(self, node):
        self.chatPrint(sysCTA + 'inbound_node_connected')

    # Message handling

    def send_message(self, msg):
        self.chatPrint(self.selfCTA + str(msg))
        return self.send_to_nodes(msg)

    def node_message(self, node, data):
        self.chatPrint(self.connectedCTA + str(data))

    ## System prints

    def inbound_node_disconnected(self, node):
        self.chatPrint(sysCTA + 'inbound_node_disconnected')

    def outbound_node_disconnected(self, node):
        self.chatPrint(sysCTA + 'outbound_node_disconnected')
        
    def node_disconnect_with_outbound_node(self, node):
        self.chatPrint(sysCTA + 'node_disconnect_with_outbound_node')

    def node_request_to_stop(self):
        self.chatPrint(sysCTA + 'node_request_to_stop')