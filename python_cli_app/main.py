import argparse, time, sys
from curses import wrapper
from p2pnetwork.node import Node
from ui import ChatUI

# public record of nodes
nodes = [
  {
    "user": "alice",
    "ip": "127.0.0.1",
    "port": 8001,
    "pub": {
      "x": 29016894970713380142110735341146241600257795843898471949279458281735225218900,
      "y": 114810713348536474503903989630355288985903011280222776558551373638242126566422
    }
  },
  {
    "user": "bob",
    "ip": "127.0.0.1",
    "port": 8002,
    "pub": {
      "x": 82403776476681359056660111244613705032124351367959293881539920730553597232906,
      "y": 67797542364675516629303695318386492492895603032769922931549187353942222671068
    }
  }
]


# read sys arguments
parser = argparse.ArgumentParser()
parser.add_argument('--usuario', '-u', dest='user', help='Usuario', required=True)
parser.add_argument('--destinatario', '-d', dest='dest', help='Destinatario', required=True)
args = parser.parse_args()

if args.user == args.dest:
    sys.exit("Destinatario e usuario nao podem ser os mesmos")

dest, *_ = [node for node in nodes if node["user"] == args.dest]
if not dest:
    sys.exit("Destinatario nao achado")

user, *_ = [node for node in nodes if node["user"] == args.user]
if not user:
    sys.exit("Usuario nao achado")

def main(stdscr):
    userCTA = f"{user['user']} >> "
    destCTA = f"{dest['user']} >> "
    sysCTA = "sys > "

    # helpers
    def node_callback(event, main_node, connected_node, data):
        try:
            if event == 'node_request_to_stop':
                pass
            elif event == 'node_message':
                ui.chatbuffer_add(destCTA + data)
            else:
                ui.chatbuffer_add(sysCTA + event)
        except Exception as e:
            ui.chatbuffer_add(sysCTA + str(e))

    node = Node(user['ip'], user['port'], callback=node_callback)
    node.debug = False
    node.start()

    stdscr.clear()
    ui = ChatUI(stdscr)
    ui.userlist.append(user["user"])
    ui.userlist.append(dest["user"])
    ui.redraw_userlist()

    for i in range(5):
        time.sleep(1)
        if node.connect_with_node(dest['ip'], dest['port']):
            break
        else:
            continue
    else:
      sys.exit(f'Nao conseguiu conectar com usuario {dest["user"]}')

    while True:
        msg = ui.wait_input()
        ui.chatbuffer_add(userCTA + msg)
        node.send_to_nodes(msg)

wrapper(main)
sys.exit("End Of Chat")