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
    def run(cls, output_pattern):
        cls.output_pattern = output_pattern
        moderngl_window.run_window_config(cls)


if __name__ == '__main__':
    pass