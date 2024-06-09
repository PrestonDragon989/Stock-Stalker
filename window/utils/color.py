def rgb_to_hex(r, g, b):
    """
    Converts RGB values to a hexadecimal color code.

    Args:
    - r (int): The red value (0-255).
    - g (int): The green value (0-255).
    - b (int): The blue value (0-255).

    Returns:
    - str: The hexadecimal color code.
    """
    return "#{:02x}{:02x}{:02x}".format(r, g, b)
