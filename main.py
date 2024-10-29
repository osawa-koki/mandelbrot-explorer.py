import numpy as np
from PIL import Image

width, height = 800, 800
max_iter = 256
num_frames = 200
x_center, y_center = -0.743643887037151, 0.13182590420533
zoom_factor = 1.05

x_range = 0.015
y_range = 0.015

frames = []

for i in range(num_frames):
    zoom_multiplier = zoom_factor**i
    x_min = x_center - x_range / (2 * zoom_multiplier)
    x_max = x_center + x_range / (2 * zoom_multiplier)
    y_min = y_center - y_range / (2 * zoom_multiplier)
    y_max = y_center + y_range / (2 * zoom_multiplier)

    x, y = np.linspace(x_min, x_max, width), np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    Z = np.zeros_like(C)
    output = np.zeros(C.shape, dtype=int)

    for j in range(max_iter):
        mask = np.abs(Z) < 2
        Z[mask] = Z[mask] ** 2 + C[mask]
        output[mask] = j

    red = (output * 8 % 256).astype(np.uint8)
    green = (output * 4 % 256).astype(np.uint8)
    blue = (output * 2 % 256).astype(np.uint8)
    rgb_array = np.stack((red, green, blue), axis=2)

    img = Image.fromarray(rgb_array, mode="RGB")
    frames.append(img)

frames[0].save(
    "mandelbrot.gif", save_all=True, append_images=frames[1:], duration=50, loop=0
)
