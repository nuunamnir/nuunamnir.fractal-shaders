import os

import moderngl_window


class GUI(moderngl_window.WindowConfig):
    gl_version = (4, 6)
    title = "Fractal Shader"
    window_size = (1024, 1024)
    aspect_ratio = window_size[0] / window_size[1]
    resizable = False

    resource_dir = os.path.normpath(os.path.join('..', 'resources'))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument('output', type=str, help='the destination to which the visualizations are saved, must contain {0}')
        parser.add_argument('-f', '--fractal', type=str, default='mandelbrot', help='the fractal to be visualized', choices=['mandelbrot', 'julia'])
        parser.add_argument('-m', '--map', type=str, default='mandelbrot_00', help='the color mapping used to visualize the fractal', choices=['mandelbrot_00', 'julia_00', 'julia_01'])
   

    @classmethod
    def run(cls, output_pattern, colormap=None):
        cls.output_pattern = output_pattern
        if colormap is None:
            cls.colormap = 'mandelbrot_00'
        else:
            cls.colormap = colormap
        moderngl_window.run_window_config(cls)


if __name__ == '__main__':
    pass