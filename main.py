import os
import cv2
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
OUTPUT_IMG = os.path.join(OUTPUT_DIR, "out.png")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "out.mp4")

SIZE = (2000, 2000)
DEFAULT_BACKGROUND = (255, 255, 255)


def gen_img(i):
    img = np.zeros((SIZE[0], SIZE[1], 3), np.uint8)
    # img.fill(255)
    cv2.circle(img, (1000, 1000), i*4+1, (120, 50, 150), thickness=-1)
    return img


def main():
    video = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*"mp4v"), 20, SIZE)

    for i in range(20*10):
        if (i+1) % 20 == 0:
            print(f"\rRendering frame {i+1}/{20*10}", end="")
        video.write(gen_img(i))

    print(f"\nDone")

    video.release()


if __name__ == '__main__':
    main()
