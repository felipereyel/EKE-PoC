from curses import wrapper

from init import init
from node import P2P
from ui import ChatUI

dest, self = init()

def main(stdscr):
    # Curses
    stdscr.clear()
    ui = ChatUI(stdscr)
    ui.userlist.append(self["user"])
    ui.userlist.append(dest["user"])
    ui.redraw_userlist()

    # Start
    node = P2P(self, dest, chatPrint=ui.chatbuffer_add)
    node.connect()

    # Main exchange
    while True:
        msg = ui.wait_input()
        node.send_message(msg)

wrapper(main)
