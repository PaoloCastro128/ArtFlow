import os
from PIL import Image, ImageDraw

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "out.png")

SIZE = (1000, 1000)
DEFAULT_BACKGROUND = (255, 255, 255)


def main():
    img = Image.new("RGB", SIZE, DEFAULT_BACKGROUND)
    draw = ImageDraw.Draw(img)

    draw.ellipse([(400, 400), (600, 600)], fill=(120, 50, 150))
    print(img.getpixel((500, 500)))
    print(img.getpixel((0, 500)))
    draw.point((0, 500), (0, 0, 0))
    print(img.getpixel((0, 500)))

    img.save(OUTPUT_FILE)


if __name__ == '__main__':
    main()
