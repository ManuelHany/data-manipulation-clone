import cv2
import numpy as np
from werkzeug.datastructures import FileStorage
from flask import send_file
import matplotlib.pyplot as plt
import io
import json


def generate_color_histogram(image_path):
    # Load the image
    image = cv2.imread(image_path)
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Calculate histograms for each color channel
    colors = ('r', 'g', 'b')
    plt.figure()
    plt.title('Color Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')

    for i, color in enumerate(colors):
        hist = cv2.calcHist([image_rgb], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    # Save the plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()  # Close the figure to free up memory
    buf.seek(0)  # Rewind the buffer to the beginning

    return send_file(buf, mimetype='image/png', as_attachment=False, download_name='color_histogram.png')

def generate_segmentation_mask(image_path, lower_bound, upper_bound, mask_type):

    # Load the image
    image = cv2.imread(image_path)
    # Convert BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_bound = np.array(lower_bound)
    upper_bound = np.array(upper_bound)

    # Create a mask based on the provided bounds
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # Apply different mask types based on mask_type
    if mask_type == "bitwise_and":
        result = cv2.bitwise_and(image, image, mask=mask)
    elif mask_type == "bitwise_or":
        result = cv2.bitwise_or(image, image, mask=mask)
    elif mask_type == "bitwise_xor":
        result = cv2.bitwise_xor(image, image, mask=mask)
    elif mask_type == "bitwise_not":
        result = cv2.bitwise_not(image, mask=mask)
    else:
        raise ValueError(f"Unsupported mask type: {mask_type}")

    success, buffer = cv2.imencode('.png', result)
    if not success:
        raise RuntimeError("Failed to encode image")

    # Convert buffer to bytes
    io_buf = io.BytesIO(buffer.tobytes())

    return send_file(io_buf, mimetype='image/png')

def resize(image_path, width, height):
    """Resize the image to the specified width and height."""
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (width, height))
    is_success, buffer = cv2.imencode('.png', resized_image)
    return send_file(io.BytesIO(buffer), mimetype='image/png')

def crop(image_path, x, y, width, height):
    """Crop the image to the specified rectangle."""
    image = cv2.imread(image_path)
    cropped_image = image[y:y + height, x:x + width]
    is_success, buffer = cv2.imencode('.png', cropped_image)
    return send_file(io.BytesIO(buffer), mimetype='image/png')

def format(image_path, output_format):
    """Convert the image to a different format."""
    image = cv2.imread(image_path)
    is_success, buffer = cv2.imencode(f'.{output_format}', image)
    result = io.BytesIO(buffer)
    return send_file(result, mimetype=f'image/{output_format}')

def get_width_height(image_path):
    image = cv2.imread(image_path)

    height, width, channels = image.shape

    return width, height


def get_file_from_server(file_path, file_name, file_extension):
    try:
        with open(file_path, 'rb') as file:
            image_file_storage = FileStorage(
                stream=file,
                filename=file_name + '.' + file_extension,
                content_type=f'image/{file_extension}'
            )

            return image_file_storage

    except FileNotFoundError:
        return {"message": "File not found on the server."}, 404

def send_file_for_download(image_file_storage):
    # Example: returning it as a file download response in Flask
    return send_file(
        image_file_storage.stream,
        as_attachment=True,
        download_name=image_file_storage.filename,
        mimetype=image_file_storage.content_type
    )
