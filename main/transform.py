from flask import request,jsonify
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import base64
from PIL import Image
from io import BytesIO
import json


def decodeURI(data):
    image_data = data.split(',')[1]

    # Decode the Base64 data
    image_bytes = base64.b64decode(image_data)
    
    # Open the image using PIL
    image = Image.open(BytesIO(image_bytes))
    
    return np.array(image);

def plot_to_base64_uri(plot):
        # Capture the plot as a BytesIO object
    buffer = BytesIO()
    plot.savefig(buffer, format='jpeg')
    buffer.seek(0)

    # Encode the BytesIO object as Base64
    base64_image_uri = base64.b64encode(buffer.read()).decode()
    
    
    # Close the plot
    plt.close(plot)
    
    
    # Return the Base64 image URI
    return f'data:image/jpeg;base64,{base64_image_uri}'

def intensity_histogram(image_path):
    
    image = decodeURI(image_path)
    
    
    if image is not None:
        # Continue with histogram calculations
        hist = cv2.calcHist([image], [0], None, [256 if image.max() > 1 else 2], [0, 256] if image.max() > 1 else [0, 1])
        hist = np.ravel(hist)
        # Create the histogram plot
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.hist(hist, bins=256 if image.max() > 1 else 2, range=(0, 256) if image.max() > 1 else (0, 1), density=True, color='#FBAF00', alpha=0.7)
        plt.xlabel('Pixel Value')
        plt.ylabel('Normalized Frequency')
        plt.xlim([0, 256] if image.max() > 1 else [0, 1])

        # Remove the grid and plot box
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.grid(False)
        
        return fig
    
def generate_custom_plot(image_data, x_label='X Spatial Location', y_label='Y Spatial Location', x_label_color='white', y_label_color='white'):
    font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
    font_props = FontProperties(fname=font_path)

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Customize the plot based on the provided data
    im = ax.imshow(image_data, cmap='gray')

    cbar = plt.colorbar(im)
    tick_labels = cbar.ax.get_yticklabels()
    for label in tick_labels:
        label.set_color('white')
    cbar.outline.set_edgecolor('white')

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.set_xlabel(x_label, color=x_label_color, fontproperties=font_props)
    ax.set_ylabel(y_label, color=y_label_color, fontproperties=font_props)

    return fig



class TRANSFORM:
    
    def __init__(self, image, param):
        self.data = image
        self.param = param
        
    
    
    def fourier(self):
            # Decode the image data
            image = decodeURI(self.data)
            
            # Calculate the Fourier Transform
            f_transform = np.fft.fft2(image)
            
            # Calculate the magnitude spectrum
            magnitude_spectrum = np.log(np.abs(f_transform) + 1)
            
            # Calculate the phase spectrum
            phase_spectrum = np.angle(f_transform)
            
            magnitude_spectrum_fig = generate_custom_plot(magnitude_spectrum)
            phase_spectrum_fig = generate_custom_plot(phase_spectrum)
            
                       
            
            # Convert the magnitude and phase spectra to base64 URIs
            magnitude_spectrum_uri = plot_to_base64_uri(magnitude_spectrum_fig)
            phase_spectrum_uri = plot_to_base64_uri(phase_spectrum_fig)
            
            print(magnitude_spectrum_uri)
            print(phase_spectrum_uri)
            # Create a dictionary containing both results
            result_dict = {
                "primary": magnitude_spectrum_uri,
                "intensity_histogram": phase_spectrum_uri,
            }
            json_result = json.dumps(result_dict)
            return json_result
