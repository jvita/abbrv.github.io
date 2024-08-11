from flask import Flask, render_template, request, jsonify
import numpy as np
import json
from scipy.interpolate import CubicSpline, BSpline

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import io
import base64

app = Flask(__name__)

# def load_char_splines(filename='char_splines.json'):
#     with open(filename, 'r') as file:
#         data = json.load(file)

#     # Convert data to numpy arrays
#     char_splines = {char: np.array(points, dtype=np.float32) for char, points in data.items()}
#     return char_splines

# # Load spline knot points from JSON file
# char_splines = load_char_splines()

data = {
"a": [[0.0, 0.0], [0.29, 0.0]],
"b": [[0.0, 0.0], [0.21, 0.21], [0.14, 0.64], [0.07, 0.21], [0.29, 0.0]],
"c": [[0.0, 0.0], [-0.13999999999999999, 0.0], [-0.21, -0.14999999999999997], [-0.13999999999999999, -0.29], [0.07999999999999999, -0.29]],
"d": [[0.0, 0.0], [0.5, -0.29], [1.0, 0.0]],
"e": [[0.0, 0.0], [0.29, 0.29]],
"f": [[0.0, 0.0], [0.13999999999999999, 0.0], [0.21999999999999997, -0.14999999999999997], [0.13999999999999999, -0.29], [-0.07, -0.29]],
"g": [[0.0, 0.0], [-0.29, -0.29000000000000004], [-0.29, -0.71], [0.0, -1.0]],
"h": [[0.0, 0.0], [0.15, 0.0], [0.29000000000000004, 0.07], [0.36, 0.21], [0.36, 0.43], [0.29000000000000004, 0.57], [0.15, 0.64], [0.0, 0.64], [-0.13999999999999999, 0.57], [-0.21, 0.43], [-0.21, 0.21], [-0.13999999999999999, 0.07], [0.0, 0.0], [0.29000000000000004, 0.0]],
"i": [[0.0, 0.0], [0.29, 0.29]],
"j": [[0.0, 0.0], [0.0, -0.64], [-0.14, -0.35000000000000003], [0.06999999999999998, -0.14]],
"k": [[0.0, 0.0], [0.29, -0.29000000000000004], [0.29, -0.71], [0.0, -1.0]],
"l": [[0.0, 0.0], [0.13999999999999999, 0.0], [0.21999999999999997, -0.07999999999999999], [0.21999999999999997, -0.21999999999999997], [0.13999999999999999, -0.29], [0.0, -0.29], [-0.07, -0.21999999999999997], [-0.07, -0.07999999999999999], [0.0, 0.0], [0.21999999999999997, 0.0]],
"m": [[0.0, 0.0], [0.5, 0.29], [1.0, 0.0]],
"n": [[0.0, 0.0], [0.0, 0.21], [0.07, 0.29], [0.21, 0.29], [0.29, 0.21], [0.29, 0.0]],
"o": [[0.0, 0.0], [1.0, 0.0]],
"p": [[0.0, 0.0], [-0.29, -1.0]],
"q": [[0.0, 0.0], [-0.29, -0.5], [0.0, -1.0], [0.27999999999999997, -0.5], [0.0, 0.0]],
"r": [[0.0, 0.0], [0.13999999999999999, 0.0], [0.21999999999999997, 0.07], [0.21999999999999997, 0.21], [0.13999999999999999, 0.29], [0.0, 0.29], [-0.07, 0.21], [-0.07, 0.07], [0.0, 0.0], [0.21999999999999997, 0.0]],
"s": [[0.0, 0.0], [-0.14, -0.29]],
"t": [[0.0, 0.0], [0.0, -0.21999999999999997], [0.07, -0.29], [0.21, -0.29], [0.29, -0.21999999999999997], [0.29, 0.0]],
"u": [[0.0, 0.0], [1.0, 0.29]],
"v": [[0.0, 0.0], [0.29, -1.0], [0.57, 0.0]],
"w": [[0.0, 0.0], [-0.13999999999999999, 0.0], [-0.21, 0.14], [-0.13999999999999999, 0.29], [0.07999999999999999, 0.29]],
"x": [[0.0, 0.0], [-0.29, -0.14], [0.0, -0.29], [-0.29, -0.43]],
"y": [[0.0, 0.0], [0.29, -0.29]],
"z": [[0.0, 0.0], [-0.07999999999999999, -0.21999999999999997], [-0.29, -0.29]],
}
# Convert data to numpy arrays
char_splines = {char: np.array(points, dtype=np.float32) for char, points in data.items()}


# Define spline knot points for each character
def interpolate_points(points, method='linear', num_points=100):
    if len(points) < 2:
        return np.array([]), np.array([])  # Return empty arrays if there are not enough points

    x = points[:, 0]
    y = points[:, 1]
    t = np.linspace(0, 1, len(points))

    # if (method == 'linear') or len(points) < 8:
    if method == 'linear':
        x_spline = np.interp(np.linspace(0, 1, num_points), t, x)
        y_spline = np.interp(np.linspace(0, 1, num_points), t, y)
    elif method == 'cubic':
        x_spline = CubicSpline(t, x, bc_type='natural')(np.linspace(0, 1, num_points))
        y_spline = CubicSpline(t, y, bc_type='natural')(np.linspace(0, 1, num_points))
        # x_spline = CubicSpline(t, x, bc_type=((1, 0), (1, 0)))(np.linspace(0, 1, num_points))
        # y_spline = CubicSpline(t, y, bc_type=((1, 0), (1, 0)))(np.linspace(0, 1, num_points))
    elif method == 'bspline':
        k = 4  # Cubic B-spline
        tck_x = BSpline(t, x, k, extrapolate=False)
        tck_y = BSpline(t, y, k, extrapolate=False)
        x_spline = tck_x(np.linspace(0, 1, num_points))
        y_spline = tck_y(np.linspace(0, 1, num_points))

    return x_spline, y_spline

def text_to_splines(text, interpolation_method='linear'):
    char_width = 0.29  # Default width

    lines = text.split('\n')
    splines = []
    knot_points = []
    y_offset = 0
    max_width = 15
    line_height = 2
    word_space = 2  # Space between words
    currentY = 0

    for line_index, line in enumerate(lines):
        x_offset = 0

        words = line.split(' ')
        for word in words:
            if word:
                points = []
                total_width = 0  # To calculate the total width of the word

                # Collect points for the entire word
                for char in word:
                    if char not in char_splines:
                        raise RuntimeError(f"Char '{char}' does not exist in spline dict.")

                    if total_width == 0:  # first char
                        char_points = char_splines[char]
                        currentY = char_points[-1, 1]  # for handling vertical shifts
                        adjusted_points = char_points.copy()
                    else:
                        # remove first knot of new char to avoid duplicates
                        char_points = char_splines[char][1:]

                        # Adjust x-coordinates by shifting for the character's position within the word
                        adjusted_points = char_points.copy()
                        adjusted_points[:, 0] += total_width

                        adjusted_points[:, 1] += currentY
                        currentY = adjusted_points[-1, 1]

                    points.extend(adjusted_points)
                    total_width += char_points[-1, 0]

                # Rescale x-coordinates for the entire word
                scale = char_width * len(word) / (total_width or 1)  # Avoid division by zero
                rescaled_points = np.array(points)

                # Interpolate for the entire word
                x_spline, y_spline = interpolate_points(rescaled_points, method=interpolation_method)
                splines.append((x_spline, y_spline))
                knot_points.append(rescaled_points)

                x_offset += total_width + word_space  # Adjust x_offset for each word

        y_offset -= line_height  # Fixed line height between lines of text

    return splines, knot_points

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_splines', methods=['POST'])
def generate_splines():
    text = request.form['text']
    interpolation_method = request.form['interpolation_method']
    show_knot_points = 'show_knot_points' in request.form
    splines, knot_points = text_to_splines(text, interpolation_method)

    # Plotting
    plt.figure(figsize=(9, 3))
    for x_spline, y_spline in splines:
        plt.plot(x_spline, y_spline, 'k')

    if show_knot_points:
        for points in knot_points:
            x, y = zip(*points)
            plt.plot(x, y, 'ro')  # Plot knot points as red dots

    plt.gca().set_aspect('equal', adjustable='box')
    # plt.axis('off')

    # Save plot to a PNG image in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return jsonify({'image': img_base64})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
