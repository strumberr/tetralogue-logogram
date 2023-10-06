from PIL import Image, ImageDraw, ImageFont
import math
import time
import numpy as np
import cv2
import sys

def main():
    if len(sys.argv) != 2:
        print('Usage: python logogram_generation_command.py "Your Message Here"')
        print("or")
        print('Usage: python3 logogram_generation_command.py "Your Message Here"')
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



    WIDTH, HEIGHT = 1400, 1400
    BACKGROUND_COLOR = (255, 255, 255)  # Got some white background lol

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


    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    array_triangles_coords = {}

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

    # Angle by which you want to rotate the triangles
    iteration_degrees = -27.692307692307693

    # Center of rotation (the center of the circle)
    rotation_center = (WIDTH // 2, HEIGHT // 2)

    # Loop to create and place the 13 triangles in a circle way or whatever with the edge/point facing the center
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

        # Here we are calculating the center point of the triangle
        center_x = (x1 + x2 + x3) / 3
        center_y = (y1 + y2 + y3) / 3

        # Here we rotate the entire triangle around its center point
        x1, y1 = rotate_point((x1, y1), rotation_angle, (center_x, center_y))
        x2, y2 = rotate_point((x2, y2), rotation_angle, (center_x, center_y))
        x3, y3 = rotate_point((x3, y3), rotation_angle, (center_x, center_y))

        # Draw the rotated triangle on the image
        draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], outline="black")


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
        


    def create_triangle(image, counter, char, left_or_right_2, number_char_appear):


        # result = (math.exp(char_value) + math.sin(char_value)) / (math.sqrt(char_value) + math.log10(char_value + 2))

        char_value = alphabet_dict[char][0]

        b_o_w = alphabet_dict[char][1]

        alphabet_char_value = char_value

        grouping_alphabet = map_input_to_output(char_value)

        exact_char = map_input_to_output(char_value)[b_o_w]

        section_org = (map_input_to_output_sections(char_value)) - 1



        center_x, center_y = WIDTH // 2, HEIGHT // 2
        draw = ImageDraw.Draw(image)




        triangle_size = 80
        triangle_height = int(triangle_size * (3 ** 0.5) / 2)

        if not array_triangles_coords[section_org]:
            # If there are no previous triangles in this section, initialize the coordinates
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            x1 = center_x - triangle_size / 2
            y1 = center_y - triangle_height / 2
            x2 = x1 + triangle_size
            y2 = y1
            x3 = center_x
            y3 = center_y + triangle_height
        else:
            # If there are previous triangles in this section, connect the new triangle to the top-left and top-right edges of the previous one
            previous_triangle = array_triangles_coords[section_org]

            # Calculate the coordinates for the new triangle based on the previous triangle
            x1 = previous_triangle['x1']
            y1 = previous_triangle['y1']
            x2 = previous_triangle['x2']
            y2 = previous_triangle['y2']
            x3 = x1 + (x2 - x1) / 2
            y3 = y1 + triangle_height

            angle = math.atan2(y2 - y1, x2 - x1)

        if left_or_right_2 == 0:
            
            rotation_angle = math.radians(60)  # 60 degrees for equilateral triangle
            x2 = x2 + triangle_size * math.cos(angle + rotation_angle)
            y2 = y2 + triangle_size * math.sin(angle + rotation_angle)
            x1 = x1 + triangle_size * math.cos(angle + rotation_angle)
            y1 = y1 + triangle_size * math.sin(angle + rotation_angle)
            
            x3 = x1 + (x2 - x1) * math.cos(rotation_angle) - (y2 - y1) * math.sin(rotation_angle)
            y3 = y1 + (x2 - x1) * math.sin(rotation_angle) + (y2 - y1) * math.cos(rotation_angle)

            #flip the x3 and y3 to the other side
            x3 = x1 + (x2 - x1) * math.cos(rotation_angle) + (y2 - y1) * math.sin(rotation_angle)
            y3 = y1 - (x2 - x1) * math.sin(rotation_angle) + (y2 - y1) * math.cos(rotation_angle)

            

        else:

            rotation_angle = math.radians(-60)
            x2 = x1 + triangle_size * math.cos(angle + rotation_angle)
            y2 = y1 + triangle_size * math.sin(angle + rotation_angle)
            x3 = x2 + triangle_size * math.cos(angle - rotation_angle)
            y3 = y2 + triangle_size * math.sin(angle - rotation_angle)



        
        if number_char_appear == 3:
            #use x3, y3 as the point to rotate around. Then rotate x2, y2 and x1, y1 around x3, y3, 180 degrees
            x1, y1 = rotated_about(x1, y1, x3, y3, math.radians(180))
            x2, y2 = rotated_about(x2, y2, x3, y3, math.radians(180))
            x3, y3 = rotated_about(x3, y3, x3, y3, math.radians(180))

            x1, y1, x2, y2 = x2, y2, x1, y1
        elif number_char_appear == 5:
            x1, y1 = rotated_about(x1, y1, x3, y3, math.radians(180))
            x2, y2 = rotated_about(x2, y2, x3, y3, math.radians(180))
            x3, y3 = rotated_about(x3, y3, x3, y3, math.radians(180))

            x1, y1, x2, y2 = x2, y2, x1, y1

        elif number_char_appear == 7:
            x1, y1 = rotated_about(x1, y1, x3, y3, math.radians(180))
            x2, y2 = rotated_about(x2, y2, x3, y3, math.radians(180))
            x3, y3 = rotated_about(x3, y3, x3, y3, math.radians(180))

            x1, y1, x2, y2 = x2, y2, x1, y1

        elif number_char_appear == 9:

            x1, y1 = rotated_about(x1, y1, x3, y3, math.radians(180))
            x2, y2 = rotated_about(x2, y2, x3, y3, math.radians(180))
            x3, y3 = rotated_about(x3, y3, x3, y3, math.radians(180))

            x1, y1, x2, y2 = x2, y2, x1, y1




        # draw some points on the edges of the triangle

        # draw.ellipse((x1 - 5, y1 - 5, x1 + 5, y1 + 5), fill='red')
        # draw.ellipse((x2 - 5, y2 - 5, x2 + 5, y2 + 5), fill='blue')
        # draw.ellipse((x3 - 5, y3 - 5, x3 + 5, y3 + 5), fill='green')



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

        line_width = 4


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
        

        coordinates_triangle = [(x1, y1), (x2, y2), (x3, y3)]


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
    text = message.lower().replace(' ', '')



    segment_counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                    6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                    11: 0, 12: 0, 13: 0}


    segment_amount = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                    6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                    11: 0, 12: 0, 13: 0}


    triangle_count = 0

    left_or_right = 0

    for i, char in enumerate(text):

        print(char, segment_amount[map_input_to_output_sections(alphabet_dict[char][0])])

        number_char_appear = segment_amount[map_input_to_output_sections(alphabet_dict[char][0])]

        if segment_amount[map_input_to_output_sections(alphabet_dict[char][0])] <= 1:
            left_or_right = 1

        else:
            left_or_right = 0 


        print("left_or_right: ", left_or_right)


        create_triangle(image, i, char, left_or_right, number_char_appear)

        # image_np = np.array(image)
        # cv2.imshow("Image", image_np)
        
        # key = cv2.waitKey(1) & 0xFF
        # if key == 27:  # Press 'ESC' key to exit the loop
        #     break

        # time.sleep(0.3)

        segment_amount[map_input_to_output_sections(alphabet_dict[char][0])] += 1
        left_or_right = 0
        

        # print("segment_amount", segment_amount[map_input_to_output_sections(alphabet_dict[char][0])])



    image.save("logogram.png")
    image.show()

    



if __name__ == "__main__":
    main()