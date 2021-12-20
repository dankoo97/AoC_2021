from advent import read_file, timer


def adj(x, y):
    # Be very careful to make sure this is the right order
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            yield x+j, y+i


def light_pixels(algo, image, edge):
    enhanced = set()

    # We only really care about our initial image, infinity be damned
    min_x, max_x = min(image)[0], max(image)[0]
    min_y, max_y = min(image, key=lambda k: k[1])[1], max(image, key=lambda k: k[1])[1]

    # Make sure to get the frame of the image too
    for i in range(min_y-1, max_y + 2):
        for j in range(min_x-1, max_x + 2):
            b = ''
            for dx, dy in adj(j, i):

                # If a pixel is out of frame, make sure to use the infinite edge
                if dx < min_x or dx > max_x or dy < min_y or dy > max_y:
                    b += str(int(edge == '#'))
                else:
                    b += str(int((dx, dy) in image))

            if algo[int(b, 2)]:
                enhanced.add((j, i))

    # Check if the infinite output is flashing... (because it is)
    if algo[0] and edge == '.':
        edge = '#'
    elif not algo[-1] and edge == '#':
        edge = '.'

    return enhanced, edge


def print_image(image):
    min_x, max_x = min(image)[0], max(image)[0]
    min_y, max_y = min(image, key=lambda k: k[1])[1], max(image, key=lambda k: k[1])[1]

    print(min_x, max_x)
    print(min_y, max_y)

    for i in range(min_y, max_y+1):
        for j in range(min_x, max_x+1):
            print('#' if (j, i) in image else '.', end='')
        print()

    print('\n')


@timer
def p1(algo, image):
    edge = '.'
    for i in range(2):
        image, edge = light_pixels(algo, image, edge)

    return len(image)


@timer
def p2(algo, image):
    edge = '.'
    for i in range(50):
        image, edge = light_pixels(algo, image, edge)

    return len(image)


f = read_file("./Input/Input20").split('\n\n')
algo = [c == '#' for c in f[0]]
image = set()

for i, row in enumerate(f[1].split('\n')):
    for j, c in enumerate(row):
        if c == '#':
            image.add((j, i))

p1(algo, image)
p2(algo, image)
