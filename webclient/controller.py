from jinja2 import Environment, FileSystemLoader
import frontmatter # to read markdown files with the yaml header format
import msvcrt
import sys

def main(current_song):
    # Load template.
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('template.html')
    black_template = env.get_template('black.html')

    # write default empty song to output.
    output = black_template.render()
    with open('index.html', 'w') as f:
        f.write(output)

    def get_slides(lyrics):
        return lyrics.split("\n\n")

    def is_special_char(char):
        return char in [b'\000', b'\xe0']

    slide_nr = 0
    black = True
    # Make sure to update from the latest file.
    song = frontmatter.load(current_song)
    slides = get_slides(song.content)
    slide = slides[slide_nr % len(slides)]

    while True:
        char = msvcrt.getch()
        key = char
        if is_special_char(char):
            char = msvcrt.getch()
            key_table = {
                b'M': 'right',
                b'K': 'left',
            }
            
            if char in key_table.keys():
                key = key_table[char]
            else:
                # ignore this input
                continue
        else:
            key = char.decode('utf-8')

        print(key)

        if key == 'q': break
        elif key in '0123456789':
            num = max(0, int(key) - 1)
            slide_nr = num
        elif key == 'b':
            black = not black # go black.
            if black:
                print('black ON')
            else:
                print('black OFF')

        elif key == 'right':
            slide_nr += 1
        elif key == 'left':
            slide_nr -= 1
        else:
            pass

        # Dont wrap around backwards
        if slide_nr < 0:
            slide_nr = 0
        if slide_nr >= len(slides):
            slide_nr = len(slides)

        # Make sure to update from the latest file.
        song = frontmatter.load(current_song)
        slides = get_slides(song.content)
        slide = slides[slide_nr % len(slides)]

        print(f"{slide_nr}/{len(slides)}")

        # Update the current slide
        if black:
            output = black_template.render()
        else:
            song.content = slide
            output = template.render(song=song)

        with open('index.html', 'w') as f:
            f.write(output)

if __name__ == '__main__':
    file = '../medley/current.md'
    if len(sys.argv) > 1:
        file = sys.argv[1]
    main(file)