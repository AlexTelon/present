from curses import wrapper

def main(stdscr):
    WIDTH = 100

    # Clear screen
    stdscr.clear()

    for i in range(0, 11):
        v = i-10
        stdscr.addstr(i, int(WIDTH/2), '10 divided by {} is {}'.format(v, 2))
        stdscr.refresh()
        stdscr.getkey()

        # Clear screen
        stdscr.clear()

wrapper(main)