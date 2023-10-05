from PIL import Image, ImageDraw, ImageFont
import math


def distance(ax, ay, bx, by):
    return math.sqrt((by - ay)**2 + (bx - ax)**2)

def rotated_about(ax, ay, bx, by, angle):
    radius = distance(ax, ay, bx, by)
    angle += math.atan2(ay - by, ax - bx)
    return (
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle))
    )



WIDTH, HEIGHT = 1200, 1200
BACKGROUND_COLOR = (255, 255, 255)  # White

triangle_size = 80
triangle_height = int(triangle_size * (3 ** 0.5) / 2)  # Height of the equilateral triangle

num_triangles = 13

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

# Calculate the radius of the circle
radius = min(WIDTH, HEIGHT) / 6

# Calculate the angle between each triangle
angle_between_triangles = 360 / num_triangles

start_angle = 120

# Define a function to rotate a point about another point by a given angle
def rotate_point(point, angle, origin):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return (qx, qy)

# Angle by which you want to rotate the triangles (in radians)
iteration_degrees = -27.692307692307693


# Center of rotation (the center of the circle)
rotation_center = (WIDTH // 2, HEIGHT // 2)

# Loop to create and place the triangles in a circle with the edge/point facing the center
for i in range(num_triangles):
    rotation_angle = math.radians(iteration_degrees)  # Adjust as needed
    angle = math.radians(start_angle - i * angle_between_triangles)

    # Calculate the coordinates of the triangle vertices
    x1 = rotation_center[0] + radius * math.cos(angle) - (triangle_size // 2)
    y1 = rotation_center[1] - radius * math.sin(angle) - triangle_height
    x2 = x1 + triangle_size
    y2 = y1
    x3 = x1 + (triangle_size // 2)
    y3 = y1 + triangle_height

    # Calculate the center point of the triangle
    center_x = (x1 + x2 + x3) / 3
    center_y = (y1 + y2 + y3) / 3

    # Rotate the entire triangle around its center point
    x1, y1 = rotate_point((x1, y1), rotation_angle, (center_x, center_y))
    x2, y2 = rotate_point((x2, y2), rotation_angle, (center_x, center_y))
    x3, y3 = rotate_point((x3, y3), rotation_angle, (center_x, center_y))

    # Draw the rotated triangle on the image
    draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], outline="black")

    # Get the name of the triangle
    triangle_name = f"triangle{i}"

    # draw.text([x1 - 20, y1 + 40], triangle_name, fill=(0, 0, 0))

    # Store the triangle coordinates in the dictionary
    array_triangles_coords[i] = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "x3": x3,
        "y3": y3,
    }

    iteration_degrees += (360 / num_triangles)





print(array_triangles_coords)



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
    



def create_triangle(image, counter, char, left_or_right_2):


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





    triangle_size = 80
    triangle_height = int(triangle_size * (3 ** 0.5) / 2)

    if not array_triangles_coords[section_org]:
        # If there are no previous triangles in this section, initialize the coordinates
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        x1 = center_x - triangle_size / 2
        y1 = center_y - triangle_height / 2  # Adjusted for the point to face outward
        x2 = x1 + triangle_size
        y2 = y1
        x3 = center_x  # Adjust the third vertex position to the center
        y3 = center_y + triangle_height  # Adjusted for the point to face outward
    else:
        # If there are previous triangles in this section, connect the new triangle to the top-left and top-right edges of the previous one
        previous_triangle = array_triangles_coords[section_org]

        # Calculate the coordinates for the new triangle based on the previous triangle
        x1 = previous_triangle['x1']    # top left
        y1 = previous_triangle['y1']    # top left
        x2 = previous_triangle['x2']    # top right
        y2 = previous_triangle['y2']    # top right
        x3 = x1 + (x2 - x1) / 2  # Adjust the third vertex position (middle of the base)
        y3 = y1 + triangle_height  # Adjusted for the point to face outward

        angle = math.atan2(y2 - y1, x2 - x1)

    if left_or_right == 0:

        # Rotate the equilateral triangle by the calculated angle
        rotation_angle = math.radians(60)  # 60 degrees for equilateral triangle
        x2 = x1 + triangle_size * math.cos(angle - rotation_angle)
        y2 = y1 + triangle_size * math.sin(angle - rotation_angle)
        x3 = x2 + triangle_size * math.cos(angle + rotation_angle)
        y3 = y2 + triangle_size * math.sin(angle + rotation_angle)


    else:

        # Rotate the equilateral triangle by the calculated angle
        rotation_angle = math.radians(60)  # 60 degrees for equilateral triangle
        x2 = x1 + triangle_size * math.cos(angle - rotation_angle)
        y2 = y1 + triangle_size * math.sin(angle - rotation_angle)
        x1 = x2 + triangle_size * math.cos(angle + rotation_angle)
        y1 = y2 + triangle_size * math.sin(angle + rotation_angle)
        
        x3 = x1 + (x2 - x1) * math.cos(rotation_angle) - (y2 - y1) * math.sin(rotation_angle)
        y3 = y1 + (x2 - x1) * math.sin(rotation_angle) + (y2 - y1) * math.cos(rotation_angle)



   

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
    
    def new_get_triangle_coordinates(array_triangles_coords):
        triangle = array_triangles_coords[section_org]
        x1, y1 = triangle['x1'], triangle['y1']
        x2, y2 = triangle['x2'], triangle['y2']
        x3, y3 = triangle['x3'], triangle['y3']
        
        return x1, y1, x2, y2, x3, y3
    
    def get_triangle_coordinates_text(array_triangles_coords):
        triangle = array_triangles_coords[section_org]
        x1, y1 = triangle['x1'], triangle['y1']

        return x1, y1

    print(array_triangles_coords[section_org])

    # print(get_triangle_coordinates(array_triangles_coords))
    triangle_coordinates = new_get_triangle_coordinates(array_triangles_coords)

    x1, y1, x2, y2, x3, y3 = triangle_coordinates

    # Calculate the center of the triangle
    center_x = (x1 + x2 + x3) / 3
    center_y = (y1 + y2 + y3) / 3


    font_path = "assets/Oxanium-Regular.ttf"
    font = ImageFont.truetype(font_path, 20)


    

    coordinates_triangle = [(x1, y1), (x2, y2), (x3, y3)]

    # print(coordinates_triangle)

    # Draw the triangle
    draw.polygon(get_triangle_coordinates(array_triangles_coords), outline=outline_color, width=line_width, fill=fill_color)
    
    draw.text([center_x - 10, center_y - 10], str(counter), fill=outline_color, font=font)

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
text = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz".lower().replace(' ', '')


# create a dict with how many times each character appears in the text
text_array = {}

# Initialize the segment counter
segment_counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                   6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                   11: 0, 12: 0, 13: 0}

triangle_count = 0



for i, char in enumerate(text):
    left_or_right = 0

    if segment_counter[map_input_to_output_sections(alphabet_dict[char][0])] == 0:
        left_or_right = 0
        segment_counter[map_input_to_output_sections(alphabet_dict[char][0])] = 1
    else:
        left_or_right = 1
        segment_counter[map_input_to_output_sections(alphabet_dict[char][0])] = 0


    create_triangle(image, i, char, left_or_right)



# Save the final image
image.save("logogram.png")
image.show()
