import os

import numpy
import moderngl
import PIL.Image

import gui


class Mandelbrot(gui.GUI):
    title = 'Fractal Shader: Mandelbrot'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader = '''
                #version 460

                in vec2 in_vert;
                out vec2 v_text;

                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                    v_text = in_vert;
                }
            ''',
            fragment_shader = '''
                #version 460

                in vec2 v_text;
                out vec4 f_color;

                uniform sampler2D Texture;
                uniform vec2 Center;
                uniform float Scale;
                uniform float Ratio;
                uniform int Iter;

                void main() {
                    vec2 c;
                    int i;
                    c.x = Ratio * v_text.x * Scale - Center.x;
                    c.y = v_text.y * Scale - Center.y;
                    vec2 z = c;
                    for (i = 0; i < Iter; i++) {
                        float x = (z.x * z.x - z.y * z.y) + c.x;
                        float y = (z.y * z.x + z.x * z.y) + c.y;
                        if ((x * x + y * y) > 4.0) {
                            break;
                        }
                        z.x = x;
                        z.y = y;
                    }
                    f_color = texture(Texture, vec2((i == Iter ? 0.0 : float(i)) / 100.0, 0.0));
                }
            ''',
        )

        self.center = self.prog['Center']
        self.center.value = (0.5, 0.0)
        self.scale = self.prog['Scale']
        self.scale_counter = 0.125
        self.scale.value = (1 / (self.scale_counter ** 2 + 1))
        self.ratio = self.prog['Ratio']        
        self.ratio.value = self.aspect_ratio
        self.iter = self.prog['Iter']
        self.iter.value = 100

        self.texture = self.load_texture_2d('mandelbrot_00.png')

        vertices = numpy.array([-1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0])
        self.vbo = self.ctx.buffer(vertices.astype('f4'))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, 'in_vert')

        self.image_counter = 0
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(self.window_size, 4)]
        )


    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                self.fbo.use()
                self.vao.render(moderngl.TRIANGLE_STRIP)
                image = PIL.Image.frombytes('RGBA', self.fbo.size, self.fbo.read(components=4))
                image = image.transpose(PIL.Image.Transpose.FLIP_TOP_BOTTOM)
                output_file_path = self.output_pattern.format(str(self.image_counter).zfill(2))
                image.save(output_file_path)
                self.image_counter += 1
                print(f'image written to {output_file_path} ...')


    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.scale_counter = self.scale_counter + (y_offset / 4)
        if self.scale_counter < 0.125:
            self.scale_counter = 0.125
        self.scale.value = (1 / (self.scale_counter ** 2 + 1))


    def mouse_press_event(self, x, y, button):
        if button == 1:
            self.iter.value += 1
        else:
            self.iter.value -= 1


    def mouse_drag_event(self, x, y, dx, dy):
        self.center.value =  (self.center.value[0] + (dx / self.window_size[0]) * self.scale.value , self.center.value[1] + (-dy / self.window_size[1]) * self.scale.value)


    def render(self, time, frame_time):
        self.ctx.clear(1., 1., 1.)
        self.texture.use()
        self.vao.render(moderngl.TRIANGLE_STRIP)


if __name__ == '__main__':
    Mandelbrot.run(output_pattern=os.path.join('..', 'data', 'output', 'mandelbrot_{0}.png'))