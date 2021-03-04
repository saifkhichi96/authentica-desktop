from abc import ABCMeta, abstractmethod
from PIL import Image


class Activity:
    __metaclass__ = ABCMeta

    @abstractmethod
    def display(self, app, args=None):
        pass

    def resize(self, source, canvas_size):
        src_w, src_h = source.size
        dest_w, dest_h = canvas_size
        if src_w == 0 or src_h == 0:
            output = Image.fromarray(np.ones(canvas_size).transpose() * 255.0)

        else:
            aspect_source = src_w / float(src_h)
            aspect_canvas = dest_w / float(dest_h)

            if aspect_source > aspect_canvas:
                new_w = int(dest_w)
                new_h = int(src_h * float(dest_w) / src_w)
            else:
                new_w = int(src_w * float(dest_h) / src_h)
                new_h = int(dest_h)

            output = source.resize((new_w, new_h), Image.ANTIALIAS)

        return output
