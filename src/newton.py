import os

import numpy
import moderngl
import PIL.Image

import gui


class Newton(gui.GUI):
    title = 'Fractal Shader: Newton'


    def _scale_function(self, x):
        return 2 ** x


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

                // implementation following the pseudo-code from https://en.wikipedia.org/wiki/Newton_fractal
                in vec2 v_text;
                out vec4 f_color;
                uniform sampler2D Texture;
                uniform float Ratio;
                uniform float Scale;
                uniform vec2 Center;
                uniform int Iter;

                vec2 ComplexProduct(vec2 a, vec2 b) {
                    return vec2(a.x*b.x - a.y*b.y, a.x*b.y + a.y*b.x);
                }

                vec2 ComplexQuotient(vec2 a, vec2 b) {
                    return vec2(((a.x*b.x+a.y*b.y)/(b.x*b.x+b.y*b.y)),((a.y*b.x-a.x*b.y)/(b.x*b.x+b.y*b.y)));
                } 

                vec2 f(vec2 x) {
                    return ComplexProduct(ComplexProduct(x, x), x) - vec2(1, 0);
                }
                
                vec2 fPrime(vec2 x) {
                    return 3 * ComplexProduct(x, x);
                }

                void main() {
                    vec2 z = vec2((((v_text.x * Scale * Ratio + 1) / 2.) * 3.5) - 2.5 + Center.x, (((v_text.y * Scale + 1) / 2.) * 3) - 2. + Center.y);
                    f_color = vec4(z.x, z.y, 0., 0.);

                    int i;
                    int root = 0;
                    float threshold = 0.000001;
                    for (i = 0; i < Iter; i++) {
                        z = z - ComplexQuotient(f(z), fPrime(z));
                        if(abs(z.x - 1) < threshold && abs(z.y - 0) < threshold) {
                            root = 0;
                            break;
                        }
                        if(abs(z.x + 0.5) < threshold && abs(z.y - sqrt(3) / 2.) < threshold) {
                            root = 1;
                            break;
                        }
                        if(abs(z.x + 0.5) < threshold && abs(z.y + sqrt(3) / 2.) < threshold) {
                            root = 2;
                            break;
                        }
                    }
                    f_color =  texture(Texture, vec2((1./3.) * root + float(i) / float(Iter) / 3., 0.0));
                }
            ''',
        )

        self.texture = self.load_texture_2d(f'{self.colormap}.png')

        self.center = self.prog['Center']
        self.center.value = (0, 0)

        self.ratio = self.prog['Ratio']        
        self.ratio.value = self.aspect_ratio

        self.scale = self.prog['Scale']
        self.scale.value = 1.

        self.iter = self.prog['Iter']
        self.iter.value = 7

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

    def mouse_drag_event(self, x, y, dx, dy):
        self.center.value =  (self.center.value[0] + (-dx / self.window_size[0]) * self.scale.value, self.center.value[1] + (dy / self.window_size[1]) * self.scale.value)


    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.scale.value += 0.01 * y_offset

    def mouse_press_event(self, x, y, button):
        if button == 1:
            self.iter.value += 1
        else:
            self.iter.value -= 1

    def render(self, time, frame_time):
        self.ctx.clear(1., 1., 1.)
        self.texture.use()
        self.vao.render(moderngl.TRIANGLE_STRIP)


if __name__ == '__main__':
    Newton.run(output_pattern=os.path.join('..', 'data', 'output', 'newton_{0}.png'))