from PIL import Image, ImageDraw
import math

WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = (255, 255, 255)  # White


array_triangles_coords = {}

for i in range(1, 14):
    angle = 2 * math.pi * i / 13
    radius = min(WIDTH, HEIGHT) / 3
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    x1 = center_x + radius * math.cos(angle - math.pi / 6)
    y1 = center_y + radius * math.sin(angle - math.pi / 6)
    x2 = center_x + radius * math.cos(angle + math.pi / 6)
    y2 = center_y + radius * math.sin(angle + math.pi / 6)
    x3 = center_x + radius * math.cos(angle + math.pi / 2)
    y3 = center_y + radius * math.sin(angle + math.pi / 2)

    array_triangles_coords[i] = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "x3": x3,
        "y3": y3
    }

counter_rotator = 0

alphabet_dict = {
    'a': [1, 0], 'b': [2, 1], 'c': [3, 0], 'd': [4, 1], 'e': [5, 0], 'f': [6, 1], 'g': [7, 0], 'h': [8, 1], 'i': [9, 0], 'j': [10, 1],
    'k': [11, 0], 'l': [12, 1], 'm': [13, 0], 'n': [14, 1], 'o': [15, 0], 'p': [16, 1], 'q': [17, 0], 'r': [18, 1], 's': [19, 0],
    't': [20, 1], 'u': [21, 0], 'v': [22, 1], 'w': [23, 0], 'x': [24, 1], 'y': [25, 0], 'z': [26, 1]
}

def map_input_to_output(input_range):
    mapping = {
        (1, 2): 'AB',
        (3, 4): 'CD',
        (5, 6): 'EF',
        (7, 8): 'GH',
        (9, 10): 'IJ',
        (11, 12): 'KL',
        (13, 14): 'MN',
        (15, 16): 'OP',
        (17, 18): 'QR',
        (19, 20): 'ST',
        (21, 22): 'UV',
        (23, 24): 'WX',
        (25, 26): 'YZ',
    }

    for key, value in mapping.items():
        if key[0] <= input_range <= key[1]:
            return value

    return None


def map_input_to_output_sections(input_range):
    mapping = {
        (1, 2): 1,
        (3, 4): 2,
        (5, 6): 3,
        (7, 8): 4,
        (9, 10): 5,
        (11, 12): 6,
        (13, 14): 7,
        (15, 16): 8,
        (17, 18): 9,
        (19, 20): 10,
        (21, 22): 11,
        (23, 24): 12,
        (25, 26): 13,
    }

    for key, value in mapping.items():
        if key[0] <= input_range <= key[1]:
            return value

    return None


black_or_white = 0

def transform_input(input_value):
    if input_value < 1 or input_value > 26:
        return None
    else:
        output_value = 101 - input_value * 3
        remainder = output_value % 13
        if remainder != 0:
            output_value -= remainder
        return output_value


def create_triangle(image, counter, char):
    global counter_rotator

    # result = (math.exp(char_value) + math.sin(char_value)) / (math.sqrt(char_value) + math.log10(char_value + 2))

    char_value = alphabet_dict[char][0]

    b_o_w = alphabet_dict[char][1]

    alphabet_char_value = char_value

    grouping_alphabet = map_input_to_output(char_value)

    exact_char = map_input_to_output(char_value)[b_o_w]

    section_org = map_input_to_output_sections(char_value)

    
    print(char_value, b_o_w, map_input_to_output(char_value), map_input_to_output(char_value)[b_o_w], section_org)

    # new_alphabet_value = {}

    # for el in alphabet_dict:
    #     new_alphabet_value[el] = int(alphabet_dict[el] + result)


    # print(new_alphabet_value)

    center_x, center_y = WIDTH // 2, HEIGHT // 2
    draw = ImageDraw.Draw(image)




    # Define the triangle parameters
    triangle_size = 50  # Length of each side
    triangle_height = int(triangle_size * (3 ** 0.5) / 2)  # Height of the equilateral triangle

    if counter > 0:
        previous_triangle = array_triangles_coords[f"triangle{counter-1}"]
        x1, y1 = previous_triangle['x2'], previous_triangle['y2']
        x2, y2 = previous_triangle['x3'], previous_triangle['y3']
    else:
        x1 = center_x - triangle_size // 2
        y1 = center_y + triangle_height // 2
        x2 = x1 + triangle_size
        y2 = y1

    
    x3 = x1 + triangle_size // 2
    y3 = y1 - triangle_height

    # Store the coordinates in a dictionary
    triangle_corners2 = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "x3": x3,
        "y3": y3
    }

    array_triangles_coords[f"triangle{counter}"] = triangle_corners2

    fill_color = (0, 0, 0) if b_o_w == 0 else (255, 255, 255)
    
    outline_color = (255, 255, 255) if b_o_w == 0 else (0, 0, 0)


    line_width = 2

    draw.text((x1, y1), exact_char, fill=(0, 0, 0))

    # Draw the triangle
    draw.polygon([(x1, y1), (x2, y2), (x3, y3)], outline=outline_color, width=line_width, fill=fill_color)

# Create a white background image
image = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)

# Text to be represented
text = "akepplerz"


# Create and display an image representing each character
for i, char in enumerate(text):
    create_triangle(image, i, char)

# Save the final image
image.save("logogram.png")
image.show()
