from PIL import Image, ImageDraw, ImageFont


def color(image, hex_color, input_dir, text):
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
    image = Image.open(f"{input_dir}/{image}")
    draw = ImageDraw.Draw(image)
    rgb = hex_to_rgb(hex_color)
    width, height = image.size

    draw.text((width - 275, height - 90), text, font=font, fill=rgb)
    return image


def hex_to_rgb(hex_color):
    hex_value = hex_color.lstrip('#')
    return tuple(int(hex_value[i: i + 2], 16) for i in (0, 2, 4))
