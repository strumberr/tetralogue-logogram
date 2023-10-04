from PIL import Image, ImageDraw

WIDTH, HEIGHT = 800, 800

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
        "y3": y3
    }

# Save the image
image.save("triangles_centered.png")

# Print the dictionary
print(array_triangles_coords)
