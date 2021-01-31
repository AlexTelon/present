from jinja2 import Environment, FileSystemLoader
import frontmatter
import msvcrt

# Load template.
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
template = env.get_template('template.html')

# Get current song.
# print(song['title'])
# print(song['author'])
# print(song['ccli'])
# print(song.content)

def get_slides(lyrics):
    return lyrics.split("\n\n")

def is_special_char(char):
    return char in [b'\000', b'\xe0']

slide_nr = 0
black = False
slides = []
while True:
    char = msvcrt.getch()
    key = char
    if is_special_char(char):
        char = msvcrt.getch()
        key_table = {
            b'M': 'right',
            b'K': 'left',
            b'H': 'up',
            b'P': 'down',
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
    song = frontmatter.load('current.md')
    slides = get_slides(song.content)
    slide = slides[slide_nr % len(slides)]

    # Update the current slide
    print("update!")
    song.content = slide
    output = template.render(song=song)
    f = open('index.html', 'w')
    f.write(output)