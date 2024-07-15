def rgb_to_hex(r: int, g: int, b: int) -> str:
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


def hex_to_rgb(hex_color: str) -> tuple[int, ...]:
    """
    Simple Converts a hex code (string) into a RGB value (Tuple (R, G, B))
    Args:
        hex_color: A string of the hex code.

    Returns:
        RGB of the hex code.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def calculate_luminance(rgb_color):
    """Calculates the luminance of an RGB color."""
    r, g, b = rgb_color
    return 0.2126*r + 0.7152*g + 0.0722*b


def hex_color_brightness(hex_color):
    """Determines the brightness of a hex color on a scale of 1 to 255."""
    rgb_color = hex_to_rgb(hex_color)
    luminance = calculate_luminance(rgb_color)
    # Scale the luminance to a range of 1 to 255
    scaled_luminance = round(luminance * 255 / 100)
    return scaled_luminance


color_palette = {
    "main_bg": rgb_to_hex(55, 79, 78),
    "second_bg": rgb_to_hex(45, 69, 68),
    "third_bg": rgb_to_hex(76, 115, 113),
    "foreground": rgb_to_hex(245, 250, 250),
    "active_ground": rgb_to_hex(255, 0, 255),
    "stock_color": rgb_to_hex(51, 255, 58),
    "grid_color": rgb_to_hex(255, 51, 51),
    "border_color": rgb_to_hex(0, 0, 0)
}
