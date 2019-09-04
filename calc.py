import curses
from curses import wrapper

def get_slides(file):
    content = ''
    with open(file, 'r') as f:
        content = f.readlines()

    slides = []
    slide = ''
    for line in content:

        # Don't include linebreaks.
        if line.strip() == '---':
            continue

        if line.startswith('# '):
            slides.append(slide)

            # start a new slide
            slide = line
        else:
            slide += line

    return slides

# def print_center(stdscr, line):


def print_slide(stdscr, slide, lines_to_print=-1):
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


def main(stdscr):
    stdscr.clear()
    # Disable cursor highlight
    curses.curs_set(0)

    slides = get_slides('presentation.md')

    slide_nr = 0
    animate = -1
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
            slide_nr += 1

        # Dont wrap around backwards
        if slide_nr < 0:
            slide_nr = 0
        if slide_nr >= len(slides):
            slide_nr = len(slides)

        stdscr.clear()

    # Enable cursor highlight
    curses.curs_set(1)



wrapper(main)