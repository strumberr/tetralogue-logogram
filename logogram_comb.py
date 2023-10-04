from PIL import Image, ImageDraw
import math

WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = (255, 255, 255)  # White





triangle_size = 50  # Length of each side
triangle_height = int(triangle_size * (3 ** 0.5) / 2)  # Height of the equilateral triangle

num_triangles = 13  # Number of triangles to create

# Calculate the total width occupied by the triangles
total_width = num_triangles * triangle_size

# Calculate the total height occupied by the triangles
total_height = triangle_height

# Calculate the starting position to center the triangles both horizontally and vertically
start_x = (WIDTH - total_width) // 2
start_y = (HEIGHT - total_height) // 2

# Create a blank image
image = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(image)

array_triangles_coords = {}  # Dictionary to store triangle coordinates

# Calculate the horizontal spacing as a fraction of total width
horizontal_spacing = triangle_size

# Loop to create and place the triangles with spacing
for i in range(num_triangles):
    x1 = start_x + i * horizontal_spacing
    y1 = start_y
    x2 = x1 + triangle_size
    y2 = start_y
    x3 = x1 + (triangle_size // 2)
    y3 = start_y + triangle_height

    # Draw the triangle on the image
    draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], outline="black")

    # Store the triangle coordinates in the dictionary
    array_triangles_coords[i] = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "x3": x3,
        "y3": y3,
    }




print(array_triangles_coords)









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

    section_org = (map_input_to_output_sections(char_value)) - 1

    
    print(char_value, b_o_w, map_input_to_output(char_value), map_input_to_output(char_value)[b_o_w], section_org)

    # new_alphabet_value = {}

    # for el in alphabet_dict:
    #     new_alphabet_value[el] = int(alphabet_dict[el] + result)


    # print(new_alphabet_value)

    center_x, center_y = WIDTH // 2, HEIGHT // 2
    draw = ImageDraw.Draw(image)





    triangle_size = 50
    triangle_height = int(triangle_size * (3 ** 0.5) / 2)

    if counter > 0:
        previous_triangle = array_triangles_coords[section_org]
        x1, y1 = previous_triangle['x1'], previous_triangle['y1']
        x2, y2 = previous_triangle['x2'], previous_triangle['y2']
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

   

    fill_color = (0, 0, 0) if b_o_w == 0 else (255, 255, 255)
    
    outline_color = (255, 255, 255) if b_o_w == 0 else (0, 0, 0)

    line_width = 2


    def get_triangle_coordinates(array_triangles_coords):
        triangle = array_triangles_coords[section_org]
        x1, y1 = triangle['x1'], triangle['y1']
        x2, y2 = triangle['x2'], triangle['y2']
        x3, y3 = triangle['x3'], triangle['y3']
        
        return [(x1, y1), (x2, y2), (x3, y3)]
    
    def get_triangle_coordinates_text(array_triangles_coords):
        triangle = array_triangles_coords[section_org]
        x1, y1 = triangle['x1'], triangle['y1']

        return x1, y1 - 20

    print(array_triangles_coords[section_org])

    # print(get_triangle_coordinates(array_triangles_coords))

    draw.text(get_triangle_coordinates_text(array_triangles_coords), exact_char, fill=(0, 0, 0))

    coordinates_triangle = [(x1, y1), (x2, y2), (x3, y3)]

    # print(coordinates_triangle)

    # Draw the triangle
    draw.polygon(get_triangle_coordinates(array_triangles_coords), outline=outline_color, width=line_width, fill=fill_color)
    
    array_triangles_coords[section_org] = triangle_corners2

    # array_triangles_coords[section_org] = [(x1, y1), (x2, y2), (x3, y3)]

    # array_triangles_coords[section_org] = {
    #     "x1": x1,
    #     "y1": y1,
    #     "x2": x2,
    #     "y2": y2,
    #     "x3": x3,
    #     "y3": y3
    # }


# Text to be represented
text = "cryptographycryptographyy"


# Create and display an image representing each character
for i, char in enumerate(text):
    create_triangle(image, i, char)

# Save the final image
image.save("logogram.png")
image.show()
