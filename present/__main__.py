import curses
import logging
import sys

from pathlib import Path    
from curses import wrapper

def get_slides(file):
    with open(file, 'r') as f:
        # content = [x.strip() + '\n' for x in f.readlines()]
        content = f.read()

    return content.split("\n\n")

def print_slide(stdscr, slide, lines_to_print=-1):
    try:
        _print_slide_without_error_check(stdscr, slide, lines_to_print)
    except curses.error:
        stdscr.clear()
        _print_slide_without_error_check(stdscr, "Text does not fit!", lines_to_print=-1)

def _print_slide_without_error_check(stdscr, slide, lines_to_print=-1):
    num_rows, num_cols = stdscr.getmaxyx()

    # want to split into 5 parts, and display our text in the middle 3 like so:
    #        heading          (always centered)
    # ╔═══╦═══════════╦═══╗
    # ║ 1 ║     3     ║ 1 ║   (text occupies the middle part)
    # ╚═══╩═══════════╩═══╝
    content_start_x = int(num_cols / 5)
    x_position = content_start_x

    whitespace_count = 0
    for i, line in enumerate(slide.splitlines()):
        format = curses.A_NORMAL
        if line.startswith('# '):
            line = line[2::]
            format = curses.A_STANDOUT
            # curses.A_BOLD is another option

            # Calculate center column, and then adjust starting position based
            # on the length of the message
            half_length_of_message = int(len(line) / 2)
            middle_column = int(num_cols / 2)
            x_position = middle_column - half_length_of_message
        else:
            x_position = content_start_x

        stdscr.addstr(i, x_position, line, format)

        if line.strip() == '':
            whitespace_count += 1

        # We always are interested in printing non-whitespace stuff so dont count whitespace lines
        if i - whitespace_count == lines_to_print:
            break

    # debug
    # stdscr.addstr(15, 0, "_:" + str(lines_to_print))
    stdscr.refresh()

def _main(stdscr, file):
    stdscr.clear()
    # Disable cursor highlight
    curses.curs_set(0)

    slides = get_slides(file)

    slide_nr, animate = load_context()
    while True:
        slide = slides[slide_nr % len(slides)]

        # if we were to animate the parts of the slide line by line, how many steps would we have
        slide_animation_length = len([x for x in slide.splitlines() if x.strip() != ''])

        print_slide(stdscr, slide, animate)

        char = stdscr.getch()
        if char == 113: break  # qk
        elif char == curses.KEY_RIGHT:
            slide_nr += 1
            # reset animation so we show the full slide
            animate = -1

        elif char == curses.KEY_LEFT:
            slide_nr -= 1
            # reset animation so we show the full slide
            animate = -1

        elif char == curses.KEY_DOWN:
            # If we are pressing down on an already fully shown slide, go to next
            if animate == -1:
                animate = 0
                slide_nr += 1
            else:
                animate += 1

            # If we go past the end of the slide go the beginning of the next one without showing contents
            if animate >= slide_animation_length:
                animate = 0
                slide_nr += 1

        elif char == curses.KEY_UP:
            animate -= 1

            # If we go past 0 then we want to the previous slide and show the whole thing
            if animate < 0:
                animate = -1
                slide_nr -= 1
        else:
            pass

        # Dont wrap around backwards
        if slide_nr < 0:
            slide_nr = 0
        if slide_nr >= len(slides):
            slide_nr = len(slides)

        stdscr.clear()

    # Enable cursor highlight
    curses.curs_set(1)

    save_context(slide_nr, animate)


def save_context(slide=0, animation=-1):
    with open(get_context_file_name(), 'w') as f:
            f.write(f'slide={slide}\n')
            f.write(f'animation={animation}\n')

def load_context():
    # The actual performing is done in the other function, here we only make sure to handle exceptions
    try:
        return _load_context_without_error_check()
    except FileNotFoundError:
        # File did not exists, write a new emtpy one.
        save_context()
        return load_context()

def _load_context_without_error_check():
    content = ''
    with open(get_context_file_name(), 'r') as f:
        content = f.readlines()
    slide = 0
    animation = -1

    for line in content:
        if line.startswith('slide='):
            slide = int(line[6::])
        if line.startswith('animation='):
            animation = int(line[10::])

    return (slide, animation)

# A context that is saved per-file. This will help us get back to our previous location in the presentation.
# That way we can get back to where we were even if we exit the application and edit something in the presentation and get back.
def get_context_file_name():
    return '.presentation_slide_' + PRESENTATION_NAME

logger = logging.getLogger(__file__)
hdlr = logging.FileHandler(__file__ + ".log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

# Just the name of the current presentation file
PRESENTATION_NAME = ''

def main():
    file = 'presentation.md'
    logger.debug('===== main ======')
    if len(sys.argv) > 1:

        # first loop over all args to see if we specify which file to open. Do this before checking other options.
        for arg in sys.argv[1::]:
            # import pdb; pdb.set_trace()
            if not arg.startswith('-'):
                # If the argument does not start with a dash then assume it is a file we want to start
                file = arg
                PRESENTATION_NAME = Path(file).name

        for arg in sys.argv[1::]:
            if arg == '--clean' or arg == '-c':
                # Overwrite the previous context.
                save_context()

    # start the application
    wrapper(_main, file)



if __name__ == '__main__':
    main()
