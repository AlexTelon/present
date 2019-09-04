import curses
from curses import wrapper

def get_slides(file):
    content = ''
    with open(file, 'r') as f:
        content = f.readlines()

    slides = []
    slide = ''
    for line in content:
        if line.startswith('# '):
            slides.append(slide)

            # start a new slide
            slide = line
        else:
            slide += line

    return slides

def main(stdscr):
    stdscr.clear()
    # Disable cursor highlight
    curses.curs_set(0)

    slides = get_slides('presentation.md')
    for slide in slides:

        for i, line in enumerate(slide.splitlines()):
            format = curses.A_NORMAL
            if line.startswith('# '):
                line = line[2::]
                format = curses.A_STANDOUT
                # curses.A_BOLD is another option
            stdscr.addstr(i, 0, line, format)

        stdscr.refresh()
        stdscr.getkey()

        stdscr.clear()

    # Enable cursor highlight
    curses.curs_set(1)



wrapper(main)