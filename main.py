import abc
import math
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
        self.frames_per_second = frames_per_second
        self.video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*file_format),
                                     self.frames_per_second, self.dimensions)
        self.empty_frame = self._get_empty_frame_template(dimensions, background_color)
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    @staticmethod
    def _get_empty_frame_template(dimensions, background_color):
        frame = np.zeros((dimensions[0], dimensions[1], 3), np.uint8)
        if background_color != BLACK:
            frame[:] = background_color
        return frame

    def render_frame(self, frame_count):
        current_frame = self.empty_frame.copy()
        for layer in self.layers:
            current_frame = layer.render(current_frame, frame_count)
        return current_frame

    def render(self, length_frames=None, length_seconds=None, verbose_frames=None):
        if length_frames is None and length_seconds is None:
            raise RuntimeError("Must provide length_frames or length_seconds.")
        if length_frames is None and length_seconds:
            length_frames = int(length_seconds * self.frames_per_second)
        if verbose_frames is None:
            verbose_frames = self.frames_per_second

        print("Starting render...")
        for i in range(length_frames):
            if verbose_frames > 0 and i % verbose_frames:
                print(f"\rRendering: frame={i}/{length_frames} -- "
                      f"seconds={round(i/self.frames_per_second, 2)}/{round(length_frames/self.frames_per_second, 2)}", end="")
            self.video.write(self.render_frame(i))
        print(f"\rRendering: frame={length_frames}/{length_frames} -- "
              f"seconds={round(length_frames / self.frames_per_second, 2)}/"
              f"{round(length_frames/self.frames_per_second, 2)}", end="")
        print("\nRender done!")
        self.video.release()


class Layer:
    def __init__(self, opacity=1, gamma=0):
        self.opacity = opacity
        self.gamma = gamma

    @abc.abstractmethod
    def get_overlay(self, base_frame, frame_count):
        pass

    @staticmethod
    def get_dynamic_value(val):
        if isinstance(val, DynamicValue):
            return val
        return DynamicValue(val)

    def render(self, base_frame, frame_count):
        overlay = self.get_overlay(base_frame.copy(), frame_count)
        return cv2.addWeighted(overlay, self.opacity, base_frame, 1 - self.opacity, self.gamma)


class Circle(Layer):
    def __init__(self, center_x, center_y, radius, color, opacity=1):
        self.center_x = self.get_dynamic_value(center_x)
        self.center_y = self.get_dynamic_value(center_y)
        self.radius = self.get_dynamic_value(radius)
        self.color = self.get_dynamic_value(color)
        super().__init__(opacity=opacity)

    def get_overlay(self, base_frame, frame_count):
        center = (self.center_x.get(frame_count), self.center_y.get(frame_count))
        cv2.circle(base_frame, center, self.radius.get(frame_count), self.color.get(frame_count), thickness=-1)
        return base_frame


class DynamicValue:
    def __init__(self, base_value):
        self.base_value = base_value
        self.setter = None
        self.updaters = []

    def add_setter(self, setter):
        self.setter = setter

    def add_updater(self, updater):
        self.updaters.append(updater)

    def get(self, frame_count):
        if self.setter:
            value = self.setter(frame_count)
        else:
            value = self.base_value
        for updater in self.updaters:
            value = updater(value, frame_count)
        return value


def main():
    video = Video(OUTPUT_VIDEO, 20, SIZE)
    radius = DynamicValue(1)
    radius.add_updater(lambda val, frame_count: val + frame_count*4)
    center_x = DynamicValue(500)
    center_x.add_updater(lambda val, frame_count: val - 4 * math.cos(frame_count/3))
    circle = Circle(center_x, 1000, radius, (120, 200, 20))
    video.add_layer(circle)
    video.render(length_seconds=5)


if __name__ == '__main__':
    main()
