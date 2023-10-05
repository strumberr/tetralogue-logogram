from PIL import Image, ImageDraw, ImageFont
import math
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python logogram_comb.py <message>")
        return

    # Retrieve the message from the command-line argument
    message = sys.argv[1]

    def distance(ax, ay, bx, by):
        return math.sqrt((by - ay)**2 + (bx - ax)**2)

    def rotated_about(ax, ay, bx, by, angle):
        radius = distance(ax, ay, bx, by)
        angle += math.atan2(ay - by, ax - bx)
        return (
            round(bx + radius * math.cos(angle)),
            round(by + radius * math.sin(angle))
        )

    WIDTH, HEIGHT = 1000, 1000
    BACKGROUND_COLOR = (255, 255, 255)

    triangle_size = 50
    triangle_height = int(triangle_size * (3 ** 0.5) / 2)

    num_triangles = 13

    total_width = num_triangles * triangle_size

    total_height = triangle_height

    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - total_height) // 2

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    array_triangles_coords = {}

    horizontal_spacing = triangle_size

    radius = min(WIDTH, HEIGHT) / 6

    angle_between_triangles = 360 / num_triangles

    start_angle = 120

    def rotate_point(point, angle, origin):
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return (qx, qy)

    iteration_degrees = -27.692307692307693

    rotation_center = (WIDTH // 2, HEIGHT // 2)

    for i in range(num_triangles):
        rotation_angle = math.radians(iteration_degrees)
        angle = math.radians(start_angle - i * angle_between_triangles)

        x1 = rotation_center[0] + radius * math.cos(angle) - (triangle_size // 2)
        y1 = rotation_center[1] - radius * math.sin(angle) - triangle_height
        x2 = x1 + triangle_size
        y2 = y1
        x3 = x1 + (triangle_size // 2)
        y3 = y1 + triangle_height

        center_x = (x1 + x2 + x3) / 3
        center_y = (y1 + y2 + y3) / 3

        x1, y1 = rotate_point((x1, y1), rotation_angle, (center_x, center_y))
        x2, y2 = rotate_point((x2, y2), rotation_angle, (center_x, center_y))
        x3, y3 = rotate_point((x3, y3), rotation_angle, (center_x, center_y))

        draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], outline="black")

        triangle_name = f"triangle{i}"

        array_triangles_coords[i] = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "x3": x3,
            "y3": y3,
        }

        iteration_degrees += (360 / num_triangles)


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

        char_value = alphabet_dict[char][0]

        b_o_w = alphabet_dict[char][1]

        alphabet_char_value = char_value

        grouping_alphabet = map_input_to_output(char_value)

        exact_char = map_input_to_output(char_value)[b_o_w]

        section_org = (map_input_to_output_sections(char_value)) - 1
        
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        draw = ImageDraw.Draw(image)

        triangle_size = 50
        triangle_height = int(triangle_size * (3 ** 0.5) / 2)

        if not array_triangles_coords[section_org]:

            center_x, center_y = WIDTH // 2, HEIGHT // 2
            x1 = center_x - triangle_size / 2
            y1 = center_y - triangle_height / 2
            x2 = x1 + triangle_size
            y2 = y1
            x3 = center_x
            y3 = center_y + triangle_height
        else:
            previous_triangle = array_triangles_coords[section_org]

            x1 = previous_triangle['x1']
            y1 = previous_triangle['y1']
            x2 = previous_triangle['x2']
            y2 = previous_triangle['y2']
            x3 = x1 + (x2 - x1) / 2
            y3 = y1 + triangle_height

            angle = math.atan2(y2 - y1, x2 - x1)

        if left_or_right == 0:
            rotation_angle = math.radians(60)
            x2 = x1 + triangle_size * math.cos(angle - rotation_angle)
            y2 = y1 + triangle_size * math.sin(angle - rotation_angle)
            x3 = x2 + triangle_size * math.cos(angle + rotation_angle)
            y3 = y2 + triangle_size * math.sin(angle + rotation_angle)

        else:
            rotation_angle = math.radians(60)
            x2 = x1 + triangle_size * math.cos(angle + rotation_angle)
            y2 = y1 + triangle_size * math.sin(angle + rotation_angle)
            x3 = x2 + triangle_size * math.cos(angle - rotation_angle)
            y3 = y2 + triangle_size * math.sin(angle - rotation_angle)

    
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

        triangle_coordinates = new_get_triangle_coordinates(array_triangles_coords)

        x1, y1, x2, y2, x3, y3 = triangle_coordinates

        center_x = (x1 + x2 + x3) / 3
        center_y = (y1 + y2 + y3) / 3

        font_path = "assets/Oxanium-Regular.ttf"
        font = ImageFont.truetype(font_path, 20)

        draw.polygon(get_triangle_coordinates(array_triangles_coords), outline=outline_color, width=line_width, fill=fill_color)
        
        draw.text([center_x - 10, center_y - 10], str(counter), fill=outline_color, font=font)

        array_triangles_coords[section_org] = triangle_corners2

    text = message.lower().replace(' ', '')

    text_array = {}

    segments_array = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 
                    6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                    11: 0, 12: 0, 13: 0}


    for i, char in enumerate(text):
        left_or_right = 0
        if char in text_array:
            text_array[char] += 1
            if text_array[char] % 2 == 0:
                left_or_right = 0
            else:
                left_or_right = 1
        else:
            text_array[char] = 1

        create_triangle(image, i, char, left_or_right)

    image.save("logogram.png")
    image.show()


if __name__ == "__main__":
    main()