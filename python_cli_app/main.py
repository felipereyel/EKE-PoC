import argparse, time, sys, json
from curses import wrapper

from node import P2P
from ui import ChatUI

f = open('public.json')
publicRegister = json.load(f)

parser = argparse.ArgumentParser()
parser.add_argument('--usuario', '-u', dest='user', help='Usuario', required=True)
parser.add_argument('--destinatario', '-d', dest='dest', help='Destinatario', required=True)
args = parser.parse_args()

if args.user == args.dest:
    sys.exit("Destinatario e usuario nao podem ser os mesmos")

dest, *_ = [n for n in publicRegister if n["user"] == args.dest]
if not dest:
    sys.exit("Destinatario nao achado")

user, *_ = [n for n in publicRegister if n["user"] == args.user]
if not user:
    sys.exit("Usuario nao achado")

############ Main

def main(stdscr):

    # Curses
    stdscr.clear()
    ui = ChatUI(stdscr)
    ui.userlist.append(user["user"])
    ui.userlist.append(dest["user"])
    ui.redraw_userlist()

    # Start
    node = P2P(user, chatPrint=ui.chatbuffer_add)

    # Connect
    for i in range(5):
        time.sleep(1)
        if node.connect_with_node(dest):
            break
        else:
            continue
    else:
        sys.exit(f'Nao conseguiu conectar com usuario {dest["user"]}')

    # Main exchange
    while True:
        msg = ui.wait_input()
        node.send_message(msg)

wrapper(main)
sys.exit("End Of Chat")