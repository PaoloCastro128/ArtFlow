import os
import cv2
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
OUTPUT_IMG = os.path.join(OUTPUT_DIR, "out.png")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "out.mp4")

SIZE = (2000, 2000)
DEFAULT_BACKGROUND = (255, 255, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (np.nan, np.nan, np.nan)


class Video:
    def __init__(self, output_file, frames_per_second, dimensions, file_format="mp4v", background_color=BLACK):
        self.dimensions = dimensions
        self.video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*file_format), frames_per_second, dimensions)
        self.empty_frame = self._get_empty_frame_template(dimensions, background_color)
        self.frames = []

    @staticmethod
    def _get_empty_frame_template(dimensions, background_color):
        frame = np.zeros((dimensions[0], dimensions[1], 3), np.uint8)
        if background_color != BLACK:
            frame[:] = background_color
        return frame

    def render(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                for frame in reversed(self.frames):
                    pass


class Frame:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.initial_frame = self._get_initial_frame(dimensions)

    @staticmethod
    def _get_initial_frame(dimensions):
        frame = np.zeros((dimensions[0], dimensions[1], 3), np.uint8)
        frame[:] = TRANSPARENT
        return frame

    def render(self, x, y):
        return self.initial_frame[x][y]


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
