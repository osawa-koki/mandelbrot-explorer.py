import os

import numpy as np
from PIL import Image
import dotenv


dotenv.load_dotenv()


width_raw = os.getenv("WIDTH")
height_raw = os.getenv("HEIGHT")
max_iter_raw = os.getenv("MAX_ITER")
num_frames_raw = os.getenv("NUM_FRAMES")
x_center_raw = os.getenv("X_CENTER")
y_center_raw = os.getenv("Y_CENTER")
zoom_factor_raw = os.getenv("ZOOM_FACTOR")
x_range_raw = os.getenv("X_RANGE")
y_range_raw = os.getenv("Y_RANGE")

if width_raw is None:
    raise ValueError("WIDTH is not set")
if height_raw is None:
    raise ValueError("HEIGHT is not set")
if max_iter_raw is None:
    raise ValueError("MAX_ITER is not set")
if num_frames_raw is None:
    raise ValueError("NUM_FRAMES is not set")
if x_center_raw is None:
    raise ValueError("X_CENTER is not set")
if y_center_raw is None:
    raise ValueError("Y_CENTER is not set")
if zoom_factor_raw is None:
    raise ValueError("ZOOM_FACTOR is not set")
if x_range_raw is None:
    raise ValueError("X_RANGE is not set")
if y_range_raw is None:
    raise ValueError("Y_RANGE is not set")

width = int(width_raw)
height = int(height_raw)
max_iter = int(max_iter_raw)
num_frames = int(num_frames_raw)
x_center = float(x_center_raw)
y_center = float(y_center_raw)
zoom_factor = float(zoom_factor_raw)
x_range = float(x_range_raw)
y_range = float(y_range_raw)

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
    "mandelbrot.gif",
    save_all=True,
    append_images=frames[1:],
    duration=50,
    loop=0,
)
