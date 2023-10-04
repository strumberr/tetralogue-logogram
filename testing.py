def transform_input(input_value):
    if input_value < 1 or input_value > 26:
        return None  # Handle invalid input
    else:
        # Calculate the output based on the desired mapping that is divisible by 13
        output_value = 101 - input_value * 3
        remainder = output_value % 13
        if remainder != 0:
            output_value -= remainder

        # Determine black (2) or white (1) based on the alternating pattern
        b_o_w = (input_value + 1) // 2 % 2

        return output_value, b_o_w

# Test the function with various input values
for input_value in range(1, 27):
    output_value, b_o_w = transform_input(input_value)
    print(f"Input: {input_value}, Output: ({output_value}, {b_o_w}) (Black=2, White=1)")
