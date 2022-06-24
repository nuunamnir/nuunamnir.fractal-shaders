import argparse

import mandelbrot
import julia
import newton


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize different famous fractals. You can zoom into the fractal using the mouse wheel. You can pan using left mouse button drag. You can increase and decrease fractal detail (iterations) using left or right mouse button click respectively. You can save the current view of the the fractal by pressing spacebar to the specified output location.')
    parser.add_argument('output', type=str, help='the destination to which the visualizations are saved, must contain {0}')
    parser.add_argument('-f', '--fractal', type=str, default='mandelbrot', help='the fractal to be visualized', choices=['mandelbrot', 'julia', 'newton'])
    parser.add_argument('-m', '--map', type=str, default='mandelbrot_00', help='the color mapping used to visualize the fractal', choices=['mandelbrot_00', 'julia_00', 'julia_01', 'newton_00'])
    args = parser.parse_args()

    if args.fractal == 'mandelbrot':
        g = mandelbrot.Mandelbrot
    elif args.fractal == 'julia':
        g = julia.Julia
    elif args.fractal == 'newton':
        g = newton.Newton
    else:
        raise NotImplementedError

    g.run(output_pattern=args.output, colormap=args.map)
