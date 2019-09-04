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

    slides = get_slides('presentation.md')
    for slide in slides:
        stdscr.addstr(0, 0, slide)

        stdscr.refresh()
        stdscr.getkey()

        stdscr.clear()

wrapper(main)